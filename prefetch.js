// Runs right after the page loads: asks the server (same origin, HEAD) for the page's own
// response headers so extract.js can report Link/Content-Type/etc. Result lands in window.__invHead.
(function () {
  try {
    window.__invHead = null;
    fetch(location.href, { method: 'HEAD', credentials: 'include' }).then(function (r) {
      var h = {};
      r.headers.forEach(function (v, k) { h[k] = v; });
      window.__invHead = { status: r.status, url: r.url, headers: h };
    }).catch(function (e) { window.__invHead = { error: String(e) }; });
  } catch (e) {
    window.__invHead = { error: String(e) };
  }
  return 'ok';
})();
