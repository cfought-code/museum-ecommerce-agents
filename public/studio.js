const $ = id => document.getElementById(id);
const message = text => { $('message').textContent = text; };
let identity, inviteToken, recovery = false, kind = 'product', offset = 0, total = 0, selected, items = [], dirty = false, busy = false, signedIn = false;
const fieldLabels = { title: 'Title', short_description: 'Short description / biography', long_description: 'Product description', meta_description: 'SEO meta description', artist_story: 'Artist story', collection_introduction: 'Collection introduction' };
function el(tag, text, cls) { const node = document.createElement(tag); if (text !== undefined) node.textContent = text; if (cls) node.className = cls; return node; }
async function api(path, options = {}) {
  await identity?.getUser();
  const response = await fetch(path, { ...options, headers: { 'Content-Type': 'application/json', ...options.headers } });
  const data = await response.json();
  if (!response.ok || data.error) throw new Error(data.error || 'The request could not finish.');
  return data;
}
function safeLink(url) {
  try { const u = new URL(url); return u.origin === 'https://store.toledomuseum.org' ? u.href : null; } catch { return null; }
}
function sourceLink(url) { const href = safeLink(url); if (!href) return el('span', 'Unrecognized source'); const a = el('a', url); a.href = href; a.target = '_blank'; a.rel = 'noopener noreferrer'; return a; }
async function loadStatus() {
  const { run, counts } = await api('/api/status');
  signedIn = true; $('auth').hidden = true; $('workspace').hidden = false; $('logout').hidden = false;
  const count = test => counts.filter(test).reduce((n, row) => n + row.count, 0);
  $('product-count').textContent = count(row => row.kind === 'product');
  $('artist-count').textContent = count(row => row.kind === 'artist');
  $('draft-count').textContent = count(row => row.status === 'draft');
  $('run-state').textContent = run ? `${run.status.charAt(0).toUpperCase() + run.status.slice(1)} · ${run.phase === 'discover' ? 'Catalog discovery' : run.phase === 'product' ? 'Product drafts' : 'Artist drafts'}` : 'No run yet';
  $('run-detail').textContent = run ? `Started ${new Date(run.createdAt).toLocaleString()} · ${run.phase === 'discover' ? `Next catalog page: ${run.page}. ` : ''}Unverified artist identities and missing facts remain flagged for review.` : 'Start a run to discover public products and prepare source-backed drafts.';
  $('run-error').textContent = run?.error || ''; $('run-error').hidden = !run?.error;
  $('start').disabled = !!run && ['running', 'paused', 'blocked'].includes(run.status);
  $('step').hidden = run?.status !== 'running'; $('pause').hidden = run?.status !== 'running';
  $('continue').hidden = run?.status !== 'paused'; $('retry').hidden = run?.status !== 'blocked'; $('export').hidden = !run;
}
async function loadList() {
  const data = await api(`/api/drafts?kind=${kind}&offset=${offset}`); items = data.items; total = data.total;
  $('list-count').textContent = `${total} ${kind === 'product' ? 'products' : 'artists'}`;
  $('page-label').textContent = total ? `${offset + 1}–${Math.min(offset + items.length, total)} of ${total}` : 'No entries yet';
  $('previous').disabled = offset === 0; $('next').disabled = offset + items.length >= total;
  $('draft-list').replaceChildren();
  if (!items.length) $('draft-list').append(el('p', kind === 'artist' ? 'Artists appear after product sources identify them. A vendor name alone is not treated as an artist.' : 'Catalog entries appear as public products are discovered.', 'muted'));
  for (const item of items) {
    const button = el('button', item.name, selected === item.id ? 'current' : '');
    button.append(el('small', `${item.status} · ${item.review.replaceAll('_', ' ')}`));
    button.onclick = () => {
      if (dirty) { message('Save your review before opening another entry.'); return; }
      selected = item.id; renderEditor(item); for (const b of $('draft-list').children) b.classList.toggle('current', b === button);
    };
    $('draft-list').append(button);
  }
}
function renderEditor(item) {
  const editor = $('editor'); editor.replaceChildren(el('span', item.kind, 'tag'), el('h3', item.name));
  if (item.error) editor.append(el('p', item.error, 'error'));
  if (!item.result) { editor.append(el('p', item.status === 'failed' ? 'This entry could not be generated. Retry the blocked run after it finishes the remaining entries.' : 'Source gathering and generation have not completed for this entry.', 'muted')); return; }
  for (const warning of item.result.warnings) editor.append(el('p', warning, 'warning'));
  const sources = el('details'); sources.append(el('summary', 'Extracted workflow inputs & evidence'));
  for (const input of item.result.inputs) {
    const fact = el('div', undefined, 'fact'); fact.append(el('b', input.field), el('span', input.value ?? 'Missing — needs source information', input.value === null ? 'warning' : ''));
    for (const evidence of input.evidence) fact.append(el('blockquote', evidence.quote), sourceLink(evidence.url));
    sources.append(fact);
  }
  editor.append(sources);
  const originals = el('details'); originals.append(el('summary', 'Original AI draft & generation details'), el('p', `Model: ${item.model} · Generated: ${new Date(item.updatedAt).toLocaleString()}`, 'muted'));
  for (const [field, value] of Object.entries(item.result.draft)) if (value) originals.append(el('b', fieldLabels[field]), el('p', value));
  editor.append(originals);
  const form = el('form', undefined, 'editor-fields'); const values = item.edited || item.result.draft;
  for (const [key, label] of Object.entries(fieldLabels)) {
    if (item.kind === 'product' && ['artist_story', 'collection_introduction'].includes(key)) continue;
    if (item.kind === 'artist' && key === 'long_description') continue;
    const wrapper = el('label', label); const textarea = el('textarea'); textarea.name = key; textarea.value = values[key] || ''; textarea.rows = key === 'long_description' || key === 'artist_story' ? 7 : 3; wrapper.append(textarea); form.append(wrapper);
  }
  const notesLabel = el('label', 'Review notes'); const notes = el('textarea'); notes.name = 'notes'; notes.value = item.notes; notesLabel.append(notes); form.append(notesLabel);
  const row = el('div', undefined, 'save-row'); const reviewLabel = el('label', 'Review status'); const select = el('select'); select.name = 'review';
  for (const [value, label] of [['unreviewed', 'Unreviewed'], ['needs_changes', 'Needs changes'], ['approved', 'Approved draft']]) { const option = el('option', label); option.value = value; option.selected = item.review === value; select.append(option); }
  reviewLabel.append(select); const save = el('button', 'Save review ↗', 'primary'); save.type = 'submit'; row.append(reviewLabel, save); form.append(row, el('p', 'Draft approval does not publish content. Export when your review is complete.', 'muted'));
  form.oninput = () => { dirty = true; };
  form.onsubmit = async event => {
    event.preventDefault(); save.disabled = true;
    try {
      const data = new FormData(form); const edited = { ...values };
      for (const key of Object.keys(fieldLabels)) if (data.has(key)) edited[key] = data.get(key);
      await api(`/api/drafts/${item.id}`, { method: 'PATCH', body: JSON.stringify({ review: data.get('review'), notes: data.get('notes'), edited }) });
      item.edited = edited; item.review = data.get('review'); item.notes = data.get('notes'); dirty = false; message('Review saved. Nothing has been published.'); await loadStatus(); await loadList();
    } catch (error) { message(error.message); } finally { save.disabled = false; }
  };
  editor.append(form); dirty = false;
}
async function action(path, button) {
  if (busy) return; busy = true; button.disabled = true; message('Saving progress…');
  try { const data = await api(path, { method: 'POST' }); message(data.message || 'Run updated.'); await loadStatus(); await loadList(); }
  catch (error) { message(error.message); } finally { busy = false; button.disabled = false; }
}
for (const [id, path] of [['start', '/api/runs'], ['step', '/api/step'], ['pause', '/api/pause'], ['continue', '/api/continue'], ['retry', '/api/retry']]) $(id).onclick = () => action(path, $(id));
for (const [id, value] of [['products', 'product'], ['artists', 'artist']]) $(id).onclick = async () => {
  if (dirty) return message('Save your review before changing tabs.');
  kind = value; offset = 0; selected = null; $('products').classList.toggle('selected', kind === 'product'); $('artists').classList.toggle('selected', kind === 'artist');
  $('editor').replaceChildren(el('h3', 'Choose an entry to review.'));
  try { await loadList(); } catch (error) { message(error.message); }
};
for (const [id, direction] of [['previous', -1], ['next', 1]]) $(id).onclick = async () => {
  if (dirty) return message('Save your review before changing pages.');
  offset = Math.max(0, offset + direction * 25); try { await loadList(); } catch (error) { message(error.message); }
};
$('export').onclick = async () => {
  try {
    const data = await api('/api/export'); const href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }));
    const a = el('a'); a.href = href; a.download = 'museum-catalog-drafts.json'; a.click(); setTimeout(() => URL.revokeObjectURL(href), 1000);
  } catch (error) { message(error.message); }
};
$('login').onsubmit = async event => {
  event.preventDefault(); const form = event.currentTarget; const button = form.querySelector('button'); button.disabled = true;
  try { const data = new FormData(form); await identity.login(data.get('email'), data.get('password')); form.reset(); message(''); await loadStatus(); await loadList(); }
  catch (error) { message(error.message); } finally { button.disabled = false; }
};
$('logout').onclick = async () => { try { await identity.logout(); location.reload(); } catch (error) { message(error.message); } };
$('recover').onclick = async () => {
  const email = new FormData($('login')).get('email'); if (!email) return message('Enter your email above, then choose Reset password.');
  try { await identity.requestPasswordRecovery(email); message('Check your email for the password reset link.'); } catch (error) { message(error.message); }
};
$('set-password').onsubmit = async event => {
  event.preventDefault(); const password = new FormData(event.currentTarget).get('password');
  try {
    if (inviteToken) await identity.acceptInvite(inviteToken, password); else if (recovery) await identity.updateUser({ password });
    inviteToken = null; recovery = false; event.currentTarget.reset(); $('set-password').hidden = true; message('Password saved.'); await loadStatus(); await loadList();
  } catch (error) { message(error.message); }
};
window.addEventListener('beforeunload', event => { if (dirty) event.preventDefault(); });
try {
  identity = await import('https://esm.sh/@netlify/identity@2.0.1');
  const callback = await identity.handleAuthCallback();
  if (callback?.type === 'invite' || callback?.type === 'recovery') {
    inviteToken = callback.type === 'invite' ? callback.token : null; recovery = callback.type === 'recovery';
    $('login').hidden = true; $('set-password').hidden = false; message('Choose a password to finish setting up your account.');
  } else {
    try { await loadStatus(); await loadList(); } catch (error) { if (!error.message.includes('Sign in')) message(error.message); }
  }
} catch { message('Sign-in could not load. Check your connection and that Identity is enabled for this site.'); }
setInterval(async () => { if (signedIn && !busy && !document.hidden) { try { await loadStatus(); if (!dirty) await loadList(); } catch (error) { message(error.message); } } }, 20000);
