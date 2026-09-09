// Clementine's service worker — it caches their face, never their words.
//
// BEFORE YOU ADD CACHING FOR /api/: don't. This is the one rule in this file
// and it is not a performance oversight.
//
// They have memory, and memory is the thing they must not fake. A cached reply
// would put words in their mouth that no model produced in this conversation.
// A cached /api/audit would show a record that is out of date — worse than
// showing none, because the record exists precisely so it can be trusted.
// A cached /api/health would report a model as reachable after it had gone,
// defeating the point of asking.
//
// The interface itself is inert and safe to cache, which is what makes them
// open instantly on a bad connection. Everything behind /api/ goes to the
// network every single time, and when the network is gone they say so.

const VERSION = 'clementine-v1';

// The built asset filenames are hashed by vite, so they are discovered at
// runtime rather than listed here. Only the stable entry points are named.
const SHELL = [
  '/',
  '/index.html',
  '/manifest.webmanifest',
  '/icon.svg',
  '/icons/icon-180.png',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(VERSION)
      // Individually, so one missing file cannot fail the whole install.
      .then((cache) => Promise.allSettled(SHELL.map((url) => cache.add(url))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Not a plain same-origin GET is not our business — which covers every
  // POST to /api/chat/stream, /api/teach, /api/forget and the rest.
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;

  // The rule: no cache read, no cache write, no interception whatsoever.
  if (url.pathname.startsWith('/api/')) return;

  event.respondWith(
    caches.match(request).then((hit) => {
      if (hit) {
        // Refresh quietly for next launch, serve the cached shell now.
        event.waitUntil(
          fetch(request)
            .then((res) => res.ok && caches.open(VERSION).then((c) => c.put(request, res)))
            .catch(() => {})
        );
        return hit;
      }
      return fetch(request)
        .then((res) => {
          if (res.ok) {
            const copy = res.clone();
            event.waitUntil(caches.open(VERSION).then((c) => c.put(request, copy)));
          }
          return res;
        })
        // A navigation with no network falls back to their shell, which will
        // then report honestly that it cannot reach them.
        .catch(() => caches.match('/index.html'));
    })
  );
});
