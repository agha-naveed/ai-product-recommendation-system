const CACHE_NAME = "ai-recommendation-cache-v1";
const IMAGE_REGEX = /\.(png|jpg|jpeg|gif|webp|svg)$/i;
const API_REGEX = /\/products|\/recommend/;

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME));
  console.log("[ServiceWorker] Installed");
});

self.addEventListener("fetch", (event) => {
  const { request } = event;

  if (IMAGE_REGEX.test(request.url) || API_REGEX.test(request.url)) {
    event.respondWith(
      caches.match(request).then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }

        return fetch(request)
          .then((networkResponse) => {
            return caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, networkResponse.clone());
              return networkResponse;
            });
          })
          .catch(() => cachedResponse || new Response("Offline"));
      })
    );
  }
});
