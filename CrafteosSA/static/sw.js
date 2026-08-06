/* =====================================================
   Service Worker — CrafteosSA PWA
   Estrategia: Cache First para estáticos,
               Network First para páginas Django
===================================================== */

const CACHE_NAME    = 'crafteos-v1';
const OFFLINE_URL   = '/';

/* Recursos que se cachean en la instalación */
const PRECACHE_URLS = [
    '/',
    '/showobras/',
    '/dashboard/',
    '/showavance/',
    '/static/assets/css/bootstrap.min.css',
    '/static/assets/js/vendor/jquery-1.12.4.min.js',
    '/static/assets/js/bootstrap.min.js',
];

/* ── Instalación: pre-cachear recursos clave ── */
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(PRECACHE_URLS).catch(function(err) {
                console.warn('[SW] Pre-cache parcial, algunos recursos no disponibles:', err);
            });
        }).then(function() {
            return self.skipWaiting();
        })
    );
});

/* ── Activación: limpiar caches antiguas ── */
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames
                    .filter(function(name) { return name !== CACHE_NAME; })
                    .map(function(name)   { return caches.delete(name); })
            );
        }).then(function() {
            return self.clients.claim();
        })
    );
});

/* ── Fetch: Network First para HTML, Cache First para estáticos ── */
self.addEventListener('fetch', function(event) {
    /* Solo interceptar GETs del mismo origen */
    if (event.request.method !== 'GET') return;
    if (!event.request.url.startsWith(self.location.origin)) return;

    var url = new URL(event.request.url);

    /* Estáticos → Cache First */
    if (url.pathname.startsWith('/static/') || url.pathname.startsWith('/media/')) {
        event.respondWith(
            caches.match(event.request).then(function(cached) {
                return cached || fetch(event.request).then(function(response) {
                    var clone = response.clone();
                    caches.open(CACHE_NAME).then(function(cache) {
                        cache.put(event.request, clone);
                    });
                    return response;
                });
            })
        );
        return;
    }

    /* Páginas Django → Network First, fallback a caché */
    event.respondWith(
        fetch(event.request).then(function(response) {
            var clone = response.clone();
            caches.open(CACHE_NAME).then(function(cache) {
                cache.put(event.request, clone);
            });
            return response;
        }).catch(function() {
            return caches.match(event.request).then(function(cached) {
                return cached || caches.match(OFFLINE_URL);
            });
        })
    );
});
