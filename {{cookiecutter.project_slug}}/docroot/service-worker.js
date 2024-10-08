const name = 'project_name';

self.addEventListener('install', function(e) {
    /* Cache offline dependencies */
    e.waitUntil(
        caches
        .open(name)
        .then((cache) => cache.addAll([
            '/static/images/logo.svg',
            '/static/images/icons.svg',
            '/static/build/module.js',
            '/static/build/module.css'
        ]))
    );
});

self.addEventListener('fetch', function(e) {
    // A bug in Chrome means redirected GET requests are borked:
    // https://bugs.chromium.org/p/chromium/issues/detail?id=573937
    //
    // As a workaround, we recreate the request, as described
    // https://gist.github.com/jakearchibald/aff93cad208bd56a02ea70f9f0d01c99
    // https://adactio.com/journal/10204
    //if (e.request.headers.get('Accept').indexOf('text/html') !== -1) {
    if (e.request.method == 'GET') {
        console.log('[Service Worker] Recreating request');
    }

    const request = e.request.method == 'GET' ? new Request(e.request.url, {
        method: 'GET',
        headers: e.request.headers,
        mode: e.request.mode == 'navigate' ? 'cors' : e.request.mode,
        credentials: e.request.credentials,
        redirect: e.request.redirect
    }) : e.request ;

    e.respondWith(
        fetch(request).catch(() => new Response('I think you are offline.'))

        /*
        // Hit the cache first
        caches
        .match(request)
        .then((response) => {
            console.log('[Service Worker] Fetching resource: ' + request.url);
            // If the cache don't have it, fetch it
            return response || fetch(request)
            .then((response) => {
                return caches
                .open(name)
                .then((cache) => {
                    console.log('[Service Worker] Caching new resource: ' + request.url);
                    cache.put(e.request, response.clone());
                    return response;
                });
            });
        })
        */
    );
});
