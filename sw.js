self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open('sleep-tracker-v5').then((cache) => {
      return cache.addAll([
        './',
        './index.html',
        './manifest.json',
        './icon.png'
      ]);
    })
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(clients.claim());
  e.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== 'sleep-tracker-v5') {
          return caches.delete(key);
        }
      }));
    })
  );
});

self.addEventListener('fetch', (e) => {
  // Use a Network-First strategy for the HTML/root to ensure latest auth logic
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request).catch(() => {
        return caches.match(e.request);
      })
    );
    return;
  }

  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});
