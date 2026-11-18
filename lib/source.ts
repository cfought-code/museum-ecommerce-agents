import { load } from 'cheerio';
import { z } from 'zod';
import { createRequire } from 'node:module';
const robotsParser = createRequire(import.meta.url)('robots-parser') as (url: string, text: string) => { isAllowed(url: string, agent: string): boolean | undefined };

export const STORE = 'https://store.toledomuseum.org';
export type Document = { url: string; text: string };
export class SourceError extends Error {}
export function storeURL(path: string): URL {
  const url = new URL(path, STORE);
  if (url.origin !== STORE || url.username || url.password || url.port) throw new SourceError('Only the public Toledo Museum store is allowed.');
  if (!/^\/(products(?:\.json|\/)|pages\/|collections\/|robots\.txt$)/.test(url.pathname)) throw new SourceError('Unsupported store path.');
  url.hash = '';
  return url;
}
export async function fetchStore(path: string, format: 'text' | 'json' = 'text', signal: AbortSignal = AbortSignal.timeout(20000)) {
  const url = storeURL(path);
  const response = await fetch(url, { redirect: 'manual', signal, headers: { 'User-Agent': 'MuseumCatalogDrafts/1.0', Accept: format === 'json' ? 'application/json' : 'text/html,text/plain' } });
  if (!response.ok) throw new SourceError(`Store returned HTTP ${response.status} for ${url.pathname}. No content was invented. Retry after public access is restored.`);
  const reader = response.body?.getReader();
  if (!reader) throw new SourceError('Store returned an empty response.');
  const chunks: Uint8Array[] = []; let size = 0;
  while (true) {
    const { done, value } = await reader.read(); if (done) break;
    size += value.length;
    if (size > 8_000_000) { await reader.cancel(); throw new SourceError('Store response exceeded the size limit.'); }
    chunks.push(value);
  }
  const body = Buffer.concat(chunks).toString('utf8');
  if (format === 'json') {
    try { return JSON.parse(body); } catch { throw new SourceError('Store did not return a valid product feed.'); }
  }
  return body;
}
export function plain(html: string): string {
  const $ = load(html); $('script,style,nav,footer,header,noscript').remove();
  return $.root().text().replace(/\s+/g, ' ').trim();
}
export const productSchema = z.object({
  id: z.union([z.number(), z.string()]), handle: z.string().regex(/^[a-zA-Z0-9_-]+$/), title: z.string().min(1),
  vendor: z.string().default(''), product_type: z.string().default(''), body_html: z.string().nullish(),
  tags: z.union([z.string(), z.array(z.string())]).optional(),
  variants: z.array(z.object({ price: z.union([z.string(), z.number()]) })).default([]),
});
export const feedSchema = z.object({ products: z.array(productSchema) });
export type Product = z.infer<typeof productSchema>;
export function productDocument(product: Product): Document {
  return { url: `${STORE}/products/${product.handle}`, text: `Product title: ${product.title}\nVendor (not necessarily an artist): ${product.vendor}\nProduct category: ${product.product_type}\nVariant prices (currency not verified): ${product.variants.map(v => v.price).join(', ')}\nDescription: ${plain(product.body_html || '')}` };
}
export function relatedLinks(html: string): string[] {
  const $ = load(html); const links = new Set<string>();
  $('a[href]').each((_, element) => {
    try { const url = storeURL($(element).attr('href')!); if (/^\/(pages|collections)\//.test(url.pathname) && /artist|maker|designer|about/i.test(`${url.pathname} ${$(element).text()}`)) { url.search = ''; links.add(url.href); } } catch { /* Ignore external and unsupported links. */ }
  });
  return [...links].slice(0, 3);
}
export async function checkRobots(signal: AbortSignal) {
  const text = await fetchStore('/robots.txt', 'text', signal) as string;
  const robots = robotsParser(`${STORE}/robots.txt`, text);
  return (url: string) => {
    if (robots.isAllowed(url, 'MuseumCatalogDrafts') === false) throw new SourceError('Store robots policy disallows this catalog source.');
  };
}
export async function productSources(product: Product, signal: AbortSignal): Promise<Document[]> {
  const docs = [productDocument(product)];
  const allowed = await checkRobots(signal);
  allowed(docs[0].url);
  // A denied product page stops generation rather than silently dropping source evidence.
  const url = docs[0].url;
  const html = await fetchStore(url, 'text', signal) as string;
  docs.push({ url, text: plain(html).slice(0, 25000) });
  for (const link of relatedLinks(html)) {
    allowed(link);
    const text = plain(await fetchStore(link, 'text', signal) as string).slice(0, 20000);
    if (text) docs.push({ url: link, text });
  }
  return docs;
}
