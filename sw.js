/* 離線快取：介面檔案優先用快取，題庫有網路時更新 */
const CACHE = 'ejlp-v3.1';
const SHELL = ['./', 'index.html', 'app.js', 'app.css', 'manifest.webmanifest', 'icon.svg',
  'data/en.json', 'data/library.json', 'data/gloss.json', 'data/ja/index.json', 'data/ja/N5.json'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== location.origin) return;
  /* 網路優先，失敗才用快取；成功時順手更新快取 */
  e.respondWith(fetch(e.request).then(r => { if (r.ok){ const c = r.clone(); caches.open(CACHE).then(x => x.put(e.request, c)); } return r; })
    .catch(() => caches.match(e.request, {ignoreSearch: true})));
});
