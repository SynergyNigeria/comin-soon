// Service Worker for COVU PWA
const CACHE_NAME = 'covu-v1.1.0';

// Static assets to cache (using Django's static file URLs)
const staticAssets = [
  '/static/script.js',
  '/static/manifest.json',
  '/static/logo/covu.png',
  '/static/logo/covu-market.png',
  '/static/logo/covu192.png',
  '/static/logo/covu520.png',
  '/static/covu-favicon/favicon.ico',
  '/static/covu-favicon/favicon-32x32.png',
  '/static/covu-favicon/favicon-16x16.png',
  '/static/covu-favicon/apple-touch-icon.png',
  '/static/findthepro-thrift-clothes-1.jpg'
];

// Install Service Worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Caching static assets');
        // Cache static assets individually to handle failures gracefully
        return Promise.allSettled(
          staticAssets.map(url => 
            cache.add(url).catch(err => console.log('Failed to cache:', url, err))
          )
        );
      })
  );
  // Activate immediately
  self.skipWaiting();
});

// Fetch Event with network-first strategy for HTML, cache-first for static assets
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Network-first strategy for HTML pages (Django-rendered content)
  if (request.headers.get('accept').includes('text/html')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          // Clone the response and cache it
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(request, responseClone);
          });
          return response;
        })
        .catch(() => {
          // Fallback to cache if offline
          return caches.match(request).then(cachedResponse => {
            return cachedResponse || caches.match('/');
          });
        })
    );
  } 
  // Cache-first strategy for static assets
  else if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(request)
        .then(cachedResponse => {
          if (cachedResponse) {
            return cachedResponse;
          }
          return fetch(request).then(response => {
            // Cache the fetched static asset
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(request, responseClone);
            });
            return response;
          });
        })
    );
  }
  // Default: network-first for everything else
  else {
    event.respondWith(
      fetch(request)
        .catch(() => caches.match(request))
    );
  }
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