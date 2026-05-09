self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open('sleep-tracker-v4').then((cache) => {
      return cache.addAll([
        './',
        './index.html',
        './manifest.json',
        './icon.svg'
      ]);
    })
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(clients.claim());
  e.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== 'sleep-tracker-v4') {
          return caches.delete(key);
        }
      }));
    })
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});
