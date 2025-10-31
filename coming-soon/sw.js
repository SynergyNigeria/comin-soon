// Service Worker for COVU PWA
const CACHE_NAME = 'covu-v1.0.0';
const urlsToCache = [
  '/coming-soon/main.html',
  '/coming-soon/script.js',
  '/coming-soon/style.css',
  '/coming-soon/manifest.json',
  '/coming-soon/logo/covu.png'
];

// Install Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
      .catch(error => {
        console.log('Cache addAll failed, caching individually:', error);
        // Fallback: cache items individually
        return caches.open(CACHE_NAME).then(cache => {
          return Promise.allSettled(
            urlsToCache.map(url => cache.add(url).catch(err => console.log('Failed to cache:', url, err)))
          );
        });
      })
  );
});

// Fetch Event
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Return cached version or fetch from network
        return response || fetch(event.request);
      })
  );
});

// Activate Event - Clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});