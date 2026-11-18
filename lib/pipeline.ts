import { randomUUID } from 'node:crypto';
import { and, eq, sql, desc, or, isNull, lt } from 'drizzle-orm';
import { db } from '../db/index.ts';
import { runs, drafts } from '../db/schema.ts';
import { checkRobots, fetchStore, feedSchema, productSources, STORE, SourceError, type Document, type Product } from './source.ts';
import { generate, MODEL, type DraftResult } from './generate.ts';

const active = () => db.select().from(runs).where(eq(runs.status, 'running')).limit(1);
export async function startRun() {
  const [existing] = await active(); if (existing) return existing;
  const [run] = await db.insert(runs).values({ id: randomUUID() }).onConflictDoNothing().returning();
  return run || (await active())[0];
}
export async function latestRun() { return (await db.select().from(runs).orderBy(desc(runs.createdAt)).limit(1))[0] || null; }
export async function resumeRun(id: string) {
  // Serialize resume against an already running job through the unique active-run index.
  await db.update(runs).set({ status: 'running', error: null, phase: sql`case when ${runs.phase} = 'discover' then 'discover' else 'product' end`, updatedAt: new Date() }).where(and(eq(runs.id, id), eq(runs.status, 'blocked')));
  await db.update(drafts).set({ status: 'pending', error: null }).where(and(eq(drafts.runId, id), eq(drafts.status, 'failed')));
}
export async function pauseRun(id: string) {
  await db.update(runs).set({ status: 'paused', updatedAt: new Date() }).where(and(eq(runs.id, id), eq(runs.status, 'running')));
}
export async function continueRun(id: string) {
  await db.update(runs).set({ status: 'running', updatedAt: new Date() }).where(and(eq(runs.id, id), eq(runs.status, 'paused')));
}
export async function step() {
  const [candidate] = await active(); if (!candidate) return { message: 'No active run.' };
  const token = randomUUID();
  const [run] = await db.update(runs).set({ leaseToken: token, leaseUntil: new Date(Date.now() + 90000) }).where(and(eq(runs.id, candidate.id), eq(runs.status, 'running'), or(isNull(runs.leaseUntil), lt(runs.leaseUntil, new Date())))).returning();
  if (!run) return { message: 'A batch is already running.' };
  const ownsLease = and(eq(runs.id, run.id), eq(runs.leaseToken, token));
  const signal = AbortSignal.timeout(23000);
  try {
    if (run.phase === 'discover') {
      const path = `/products.json?limit=100&page=${run.page}`;
      const allowed = await checkRobots(signal); allowed(`${STORE}${path}`);
      const { products } = feedSchema.parse(await fetchStore(path, 'json', signal));
      if (!products.length) {
        const [count] = await db.select({ n: sql<number>`count(*)::int` }).from(drafts).where(eq(drafts.runId, run.id));
        if (!count.n) throw new SourceError('The public feed returned no products. Catalog coverage could not be established.');
        await db.update(runs).set({ phase: 'product', updatedAt: new Date() }).where(ownsLease);
      } else {
        const inserted = await db.insert(drafts).values(products.map(p => ({ id: randomUUID(), runId: run.id, kind: 'product', sourceKey: p.handle, name: p.title, source: { product: p } }))).onConflictDoNothing().returning({ id: drafts.id });
        if (!inserted.length) throw new SourceError('The feed repeated a page. Stopped to avoid an endless catalog crawl.');
        await db.update(runs).set({ page: run.page + 1, updatedAt: new Date() }).where(ownsLease);
      }
    } else {
      const [item] = await db.select().from(drafts).where(and(eq(drafts.runId, run.id), eq(drafts.kind, run.phase), eq(drafts.status, 'pending'))).orderBy(drafts.createdAt, drafts.id).limit(1);
      if (!item) {
        if (run.phase === 'product') await db.update(runs).set({ phase: 'artist', updatedAt: new Date() }).where(ownsLease);
        else {
          const [failed] = await db.select({ n: sql<number>`count(*)::int` }).from(drafts).where(and(eq(drafts.runId, run.id), eq(drafts.status, 'failed')));
          await db.update(runs).set({ status: failed.n ? 'blocked' : 'complete', error: failed.n ? `${failed.n} items need retry. Completed drafts are saved.` : null, updatedAt: new Date() }).where(ownsLease);
        }
      } else {
        try {
          const source = item.source as { product?: Product; documents?: Document[] };
          const docs = item.kind === 'product' ? await productSources(source.product!, signal) : source.documents!;
          const result = await generate(item.kind, item.name, docs, signal);
          await db.update(drafts).set({ result, source: { ...source, documents: docs }, status: 'draft', model: MODEL, updatedAt: new Date() }).where(eq(drafts.id, item.id));
          if (item.kind === 'product' && result.artist.name) await enqueueArtist(run.id, result, docs);
        } catch (error) {
          if (error instanceof SourceError || signal.aborted || [401, 403, 429, 500, 502, 503, 504].includes((error as {status?: number}).status || 0)) throw error;
          await db.update(drafts).set({ status: 'failed', error: 'Draft generation or evidence validation failed. Retry this run to try again.', updatedAt: new Date() }).where(eq(drafts.id, item.id));
        }
      }
    }
    return { message: 'Batch saved.' };
  } catch (error) {
    const message = error instanceof SourceError ? error.message : signal.aborted ? 'This batch timed out. Progress is saved; retry to continue.' : 'Catalog processing stopped. Check source access and AI Gateway availability, then retry.';
    await db.update(runs).set({ status: 'blocked', error: message, updatedAt: new Date() }).where(ownsLease);
    return { message };
  } finally {
    await db.update(runs).set({ leaseToken: null, leaseUntil: null }).where(ownsLease);
  }
}
async function enqueueArtist(runId: string, result: DraftResult, documents: Document[]) {
  const name = result.artist.name!;
  const key = name.normalize('NFKC').toLowerCase().replace(/\s+/g, ' ').trim();
  const [existing] = await db.select().from(drafts).where(and(eq(drafts.runId, runId), eq(drafts.kind, 'artist'), eq(drafts.sourceKey, key))).limit(1);
  if (existing) {
    const previous = (existing.source as { documents: Document[] }).documents;
    const merged = [...previous];
    for (const doc of documents) if (!merged.some(d => d.url === doc.url && d.text === doc.text) && merged.length < 12) merged.push(doc);
    await db.update(drafts).set({ source: { documents: merged } }).where(eq(drafts.id, existing.id));
  } else await db.insert(drafts).values({ id: randomUUID(), runId, kind: 'artist', sourceKey: key, name, source: { documents } }).onConflictDoNothing();
}
