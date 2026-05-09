self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('sleep-tracker-v3').then((cache) => {
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
  e.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== 'sleep-tracker-v3') {
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
