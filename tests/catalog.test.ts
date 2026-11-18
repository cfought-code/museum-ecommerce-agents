import { test, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { storeURL, STORE, feedSchema, productDocument, relatedLinks, fetchStore, productSources, checkRobots, SourceError } from '../lib/source.ts';
import { validateEvidence, productFields, artistFields, type DraftResult } from '../lib/generate.ts';

const originalFetch = globalThis.fetch;
afterEach(() => { globalThis.fetch = originalFetch; });
const product = { id: 3, handle: 'blue-vase', title: 'Blue Vase', vendor: 'Museum Editions', product_type: 'Vase', body_html: '<p>Hand-blown glass.</p><script>bad()</script>', variants: [{ price: '42.50' }] };
const doc = productDocument(product);
function result(kind = 'product'): DraftResult {
  return {
    inputs: (kind === 'product' ? productFields : artistFields).map(field => ({ field, value: null, evidence: [] })),
    artist: { name: null, identity_evidence: [] },
    draft: { title: 'Draft', short_description: '', long_description: '', meta_description: '', artist_story: '', collection_introduction: '' }, warnings: [],
  };
}
test('crawl URLs stay on the fixed public store and cannot reach transactional or external endpoints', () => {
  for (const url of ['https://evil.test/products/x', '//127.0.0.1/products/x', 'http://store.toledomuseum.org/products/x', 'https://user:pass@store.toledomuseum.org/products/x', '/admin', '/cart', '/products/../../admin']) assert.throws(() => storeURL(url));
  assert.equal(storeURL('/products/blue-vase#details').href, `${STORE}/products/blue-vase`);
});
test('feed validation rejects malformed catalog responses and unsafe handles', () => {
  assert.throws(() => feedSchema.parse({ products: [{ ...product, handle: '../../admin' }] }));
  assert.throws(() => feedSchema.parse({ error: 'challenge' }));
  assert.equal(feedSchema.parse({ products: [product] }).products.length, 1);
});
test('product evidence distinguishes vendors from artists and strips scripts', () => {
  assert.match(doc.text, /Vendor \(not necessarily an artist\): Museum Editions/);
  assert.match(doc.text, /Hand-blown glass\./);
  assert.doesNotMatch(doc.text, /bad\(\)/);
});
test('only same-store relevant artist pages are followed, without query traps', () => {
  const links = relatedLinks('<a href="https://evil.test/pages/artists">x</a><a href="/pages/our-artists?sort=1">Artist</a><a href="/cart">Cart</a><a href="/collections/vases">vases</a><a href="/pages/our-artists">Again</a>');
  assert.deepEqual(links, [`${STORE}/pages/our-artists`]);
});
test('source failures stop processing rather than creating catalog entries', async () => {
  globalThis.fetch = async () => new Response('Challenge', { status: 403 });
  await assert.rejects(fetchStore('/products.json?page=1', 'json'), error => error instanceof SourceError && /HTTP 403/.test(error.message));
});
test('redirects are rejected instead of following to another destination', async () => {
  globalThis.fetch = async (_url, options) => {
    assert.equal(options?.redirect, 'manual');
    return new Response('', { status: 302, headers: { Location: 'http://169.254.169.254/' } });
  };
  await assert.rejects(fetchStore('/products.json', 'json'), /HTTP 302/);
});
test('robots exclusions are enforced before a product page request', async () => {
  let calls = 0;
  globalThis.fetch = async () => { calls++; return new Response('User-agent: *\nDisallow: /products/'); };
  await assert.rejects(productSources(product, AbortSignal.timeout(2000)), /robots policy/);
  assert.equal(calls, 1);
});
test('discovery may proceed when the public feed is allowed by robots', async () => {
  globalThis.fetch = async () => new Response('User-agent: *\nAllow: /');
  const allowed = await checkRobots(AbortSignal.timeout(2000));
  assert.doesNotThrow(() => allowed(`${STORE}/products.json?page=1`));
});
test('non-null inputs require an exact quote from an actual supplied source', () => {
  const data = result(); data.inputs[0] = { field: 'PRODUCT_NAME', value: 'Blue Vase', evidence: [{ url: doc.url, quote: 'Product title: Blue Vase' }] };
  assert.equal(validateEvidence(data, [doc], 'product').inputs[0].value, 'Blue Vase');
  data.inputs[0].evidence[0].quote = 'Invented source';
  assert.throws(() => validateEvidence(data, [doc], 'product'), /source evidence/);
  data.inputs[0].evidence = [{ url: 'https://evil.test/products/blue-vase', quote: 'Product title: Blue Vase' }];
  assert.throws(() => validateEvidence(data, [doc], 'product'), /source evidence/);
});
test('missing inputs remain null and are flagged rather than filled with invented facts', () => {
  const data = validateEvidence(result(), [doc], 'product');
  assert.equal(data.inputs.find(x => x.field === 'MATERIALS')?.value, null);
  assert.ok(data.warnings.includes('Missing source information: MATERIALS'));
});
test('duplicate, missing, or wrong workflow fields are rejected', () => {
  const data = result(); data.inputs[1] = data.inputs[0];
  assert.throws(() => validateEvidence(data, [doc], 'product'), /input fields/);
  assert.throws(() => validateEvidence(result('artist'), [doc], 'product'), /input fields/);
});
test('artist identity evidence must quote the identified name from a supplied source', () => {
  const data = result(); data.artist = { name: 'Unverified Person', identity_evidence: [{ url: doc.url, quote: 'Hand-blown glass.' }] };
  assert.throws(() => validateEvidence(data, [doc], 'product'), /Artist identity/);
});
test('a canonical source URL can serve as evidence for the product URL input', () => {
  const data = result();
  const input = data.inputs.find(i => i.field === 'PRODUCT_URL')!;
  input.value = doc.url; input.evidence = [{ url: doc.url, quote: doc.url }];
  assert.equal(validateEvidence(data, [doc], 'product').inputs.find(i => i.field === 'PRODUCT_URL')?.value, doc.url);
});
