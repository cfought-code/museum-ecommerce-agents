import { getUser } from '@netlify/identity';
import { getContext } from '@netlify/server';
import { and, eq, gt, sql } from 'drizzle-orm';
import { z } from 'zod';
import { db } from '../db/index.ts';
import { drafts, runs } from '../db/schema.ts';
import { latestRun, startRun, resumeRun, pauseRun, continueRun, step } from './pipeline.ts';

const reviewSchema = z.object({
  review: z.enum(['unreviewed', 'approved', 'needs_changes']),
  notes: z.string().max(10000),
  edited: z.object({ title: z.string().max(1000), short_description: z.string().max(15000), long_description: z.string().max(20000), meta_description: z.string().max(1000), artist_story: z.string().max(20000), collection_introduction: z.string().max(10000) }),
});
const json = (value: unknown, status = 200) => Response.json(value, { status, headers: { 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' } });
export default async function api(req: Request): Promise<Response> {
  try {
    const user = await getUser();
    const teamUser = getContext().user;
    if (!teamUser && !user) return json({ error: 'Sign in to access the catalog workspace.' }, 401);
    if (!teamUser && !user?.roles?.includes('admin')) return json({ error: 'An administrator must grant your account the admin role before you can use this workspace.' }, 403);
    const url = new URL(req.url);
    if (!['GET', 'HEAD'].includes(req.method) && req.headers.get('origin') !== url.origin) return json({ error: 'Request origin was not accepted.' }, 403);
    if (req.method === 'GET' && url.pathname === '/api/status') {
      const run = await latestRun();
      const counts = run ? await db.select({ kind: drafts.kind, status: drafts.status, review: drafts.review, count: sql<number>`count(*)::int` }).from(drafts).where(eq(drafts.runId, run.id)).groupBy(drafts.kind, drafts.status, drafts.review) : [];
      // Never expose the worker lease capability through the API.
      const safeRun = run && { id: run.id, status: run.status, phase: run.phase, page: run.page, error: run.error, createdAt: run.createdAt, updatedAt: run.updatedAt };
      return json({ run: safeRun, counts });
    }
    if (req.method === 'POST' && url.pathname === '/api/runs') { const run = await startRun(); return json({ id: run.id }, 201); }
    if (req.method === 'POST' && url.pathname === '/api/step') {
      // Send headers immediately; one bounded batch may exceed the server's header deadline.
      const encoder = new TextEncoder();
      return new Response(new ReadableStream({ async start(controller) {
        controller.enqueue(encoder.encode(' '));
        try { controller.enqueue(encoder.encode(JSON.stringify(await step()))); }
        catch { controller.enqueue(encoder.encode(JSON.stringify({ error: 'Batch could not finish. Refresh the run status.' }))); }
        finally { controller.close(); }
      } }), { headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
    }
    if (req.method === 'POST' && ['/api/retry', '/api/pause', '/api/continue'].includes(url.pathname)) {
      const run = await latestRun(); if (!run) return json({ error: 'No run exists.' }, 404);
      if (url.pathname === '/api/retry') await resumeRun(run.id);
      if (url.pathname === '/api/pause') await pauseRun(run.id);
      if (url.pathname === '/api/continue') await continueRun(run.id);
      return json({ ok: true });
    }
    if (req.method === 'GET' && ['/api/drafts', '/api/export'].includes(url.pathname)) {
      const run = await latestRun(); if (!run) return json({ items: [], total: 0 });
      if (url.pathname === '/api/export') {
        const encoder = new TextEncoder();
        const body = new ReadableStream({ async start(controller) {
          controller.enqueue(encoder.encode(JSON.stringify({ exportedAt: new Date().toISOString(), run: { id: run.id, status: run.status }, notice: 'Reviewable drafts only. Nothing has been published to Shopify.' }).slice(0, -1) + ',"items":['));
          let cursor = ''; let first = true;
          try {
            while (true) {
              const batch = await db.select().from(drafts).where(and(eq(drafts.runId, run.id), gt(drafts.id, cursor))).orderBy(drafts.id).limit(50);
              if (!batch.length) break;
              for (const item of batch) { controller.enqueue(encoder.encode((first ? '' : ',') + JSON.stringify(item))); first = false; }
              cursor = batch[batch.length - 1].id;
            }
            controller.enqueue(encoder.encode(']}')); controller.close();
          } catch { controller.error(new Error('Export was interrupted. Download it again.')); }
        } });
        return new Response(body, { headers: { 'Content-Type': 'application/json', 'Content-Disposition': 'attachment; filename="museum-catalog-drafts.json"', 'Cache-Control': 'no-store' } });
      }
      const kind = url.searchParams.get('kind') === 'artist' ? 'artist' : 'product';
      const offset = Math.max(0, Math.min(1000000, Number(url.searchParams.get('offset')) || 0));
      const filter = and(eq(drafts.runId, run.id), eq(drafts.kind, kind));
      const items = await db.select().from(drafts).where(filter).orderBy(drafts.name, drafts.id).limit(25).offset(offset);
      const [total] = await db.select({ n: sql<number>`count(*)::int` }).from(drafts).where(filter);
      return json({ items, total: total.n });
    }
    const match = url.pathname.match(/^\/api\/drafts\/([a-f0-9-]{36})$/);
    if (req.method === 'PATCH' && match) {
      const body = reviewSchema.parse(await req.json());
      const [item] = await db.update(drafts).set({ ...body, updatedAt: new Date() }).where(and(eq(drafts.id, match[1]), eq(drafts.status, 'draft'))).returning({ id: drafts.id });
      return item ? json({ ok: true }) : json({ error: 'A completed draft was not found.' }, 404);
    }
    return json({ error: 'Route not found.' }, 404);
  } catch (error) {
    if (error instanceof z.ZodError || error instanceof SyntaxError) return json({ error: 'The request contained invalid fields.' }, 400);
    // Provider errors may contain request headers; never return or log raw exceptions.
    return json({ error: 'The operation could not finish. Check database provisioning and retry.' }, 503);
  }
}
