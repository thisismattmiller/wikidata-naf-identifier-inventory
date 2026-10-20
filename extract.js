// Runs inside the rendered page (via AppleScript "execute javascript") and returns a JSON
// string describing what the page exposes. Inventory only: nothing here judges the data.
(function () {
  var out = {};
  try {
    var abs = function (h) {
      try { return new URL(h, document.baseURI).href; } catch (e) { return h; }
    };
    var clip = function (s, n) {
      s = String(s == null ? '' : s).replace(/\s+/g, ' ').trim();
      return s.length > n ? s.slice(0, n) + '…' : s;
    };
    var all = function (sel) { return Array.prototype.slice.call(document.querySelectorAll(sel)); };

    out.final_url = location.href;
    out.title = document.title;
    out.content_type = document.contentType;
    out.lang = document.documentElement.getAttribute('lang');
    out.charset = document.characterSet;
    out.ready_state = document.readyState;
    // "hidden" means Chrome considered the window occluded; some pages render less when hidden
    out.visibility = document.visibilityState;

    var nav = performance.getEntriesByType('navigation')[0];
    out.http_status = nav && nav.responseStatus ? nav.responseStatus : null;
    out.redirect_count = nav ? nav.redirectCount : null;

    // Response headers of the page itself (Link: rel=alternate etc.), fetched by prefetch.js
    out.response_headers = window.__invHead || null;

    // <link> elements, minus the ones that are only about presentation/performance
    out.link_elements = all('link[rel]').filter(function (l) {
      return !/stylesheet|icon|preload|prefetch|preconnect|modulepreload|manifest|apple-touch|mask-icon/i
        .test(l.getAttribute('rel'));
    }).map(function (l) {
      return {
        rel: l.getAttribute('rel'),
        type: l.getAttribute('type'),
        href: abs(l.getAttribute('href')),
        title: l.getAttribute('title'),
        hreflang: l.getAttribute('hreflang')
      };
    });

    // Embedded structured data
    out.jsonld = all('script[type="application/ld+json"]').map(function (s) {
      var raw = s.textContent || '';
      var types = [];
      try {
        var walk = function (n) {
          if (Array.isArray(n)) { n.forEach(walk); return; }
          if (n && typeof n === 'object') {
            if (n['@type']) types = types.concat(n['@type']);
            if (n['@graph']) walk(n['@graph']);
          }
        };
        walk(JSON.parse(raw));
      } catch (e) { types.push('(unparseable)'); }
      return { types: types, length: raw.length, content: raw.length > 50000 ? raw.slice(0, 50000) : raw };
    });
    out.data_scripts = all('script[type]').filter(function (s) {
      var t = (s.getAttribute('type') || '').toLowerCase();
      return t && !/javascript|ecmascript|module|ld\+json|importmap|speculationrules|template|x-tmpl/.test(t);
    }).map(function (s) {
      return { type: s.getAttribute('type'), id: s.id || null, src: s.src || null, length: (s.textContent || '').length };
    });
    var itemtypes = {};
    all('[itemtype]').forEach(function (e) { itemtypes[e.getAttribute('itemtype')] = 1; });
    var typeofs = {};
    all('[typeof]').forEach(function (e) { typeofs[e.getAttribute('typeof')] = 1; });
    out.microdata = { itemscope_count: all('[itemscope]').length, itemtypes: Object.keys(itemtypes) };
    out.rdfa = {
      typeof_count: all('[typeof]').length,
      typeofs: Object.keys(typeofs).slice(0, 50),
      property_count: all('[property]:not(meta)').length,
      vocab: all('[vocab]').map(function (e) { return e.getAttribute('vocab'); }).slice(0, 10),
      prefix: all('[prefix]').map(function (e) { return e.getAttribute('prefix'); }).slice(0, 10)
    };

    out.meta = all('meta[name], meta[property], meta[itemprop]').slice(0, 150).map(function (m) {
      return {
        key: m.getAttribute('name') || m.getAttribute('property') || m.getAttribute('itemprop'),
        content: clip(m.getAttribute('content'), 500)
      };
    });

    // Links/buttons that look like a machine-readable view, export, or API
    var EXT = /\.(json|jsonld|json-ld|geojson|rdf|xml|ttl|nt|n3|nq|trig|owl|marcxml|mrc|marc|mrk|mods|mads|csv|tsv|yaml|yml|bib|ris|ead|eac|tei|atom|rss)$/i;
    var QUERY = /[?&;](format|fmt|output|outputformat|type|mode|view|export|wt|recordschema|metadataprefix|accept|_format|f|style|render)=[^&;#]*(json|xml|rdf|ttl|turtle|n3|ntriples|marc|mods|mads|csv|skos|dc\b|bibtex|ris|ead|eac|tei|unimarc|bibframe)/i;
    var SEGMENT = /\/(api|sparql|oai|oai-pmh|sru|export|download|rdf|json|xml|marcxml|lod|iiif|graphql|opensearch|linked-data|linkeddata|data)(\/|\.|$)/i;
    var TEXT = /\b(JSON(-LD)?|RDF(\/XML)?|XML|MARC[- ]?(XML|21)?|UNIMARC|Turtle|N-?Triples|N3|TTL|API|Linked (Open )?Data|LOD|SPARQL|OAI(-PMH)?|SRU|Dublin Core|MODS|MADS|SKOS|BIBFRAME|EAC(-CPF)?|EAD|TEI|CSV|BibTeX|RIS|IIIF|schema\.org|permalink|export\w*|esporta|download\w*|télécharger|herunterladen|descargar|scarica)\b/i;
    var seen = {};
    out.machine_links = [];
    all('a[href], area[href], button, [role="button"], input[type="submit"], input[type="button"], option').forEach(function (el) {
      if (out.machine_links.length >= 400) return;
      var rawHref = el.getAttribute('href');
      var href = rawHref && !/^(javascript:|mailto:|tel:|#)/i.test(rawHref) ? abs(rawHref) : null;
      var text = clip(el.textContent || el.value || '', 160);
      var label = [text, el.getAttribute('title'), el.getAttribute('aria-label')].filter(Boolean).join(' | ');
      var reasons = [];
      if (href) {
        try {
          var u = new URL(href);
          if (EXT.test(u.pathname)) reasons.push('extension');
          if (QUERY.test(u.search)) reasons.push('query');
          if (SEGMENT.test(u.pathname)) reasons.push('path');
        } catch (e) {}
      }
      if (label.length < 200 && TEXT.test(label)) reasons.push('text');
      if (!reasons.length) return;
      var key = (href || '') + '|' + text;
      if (seen[key]) return;
      seen[key] = 1;
      out.machine_links.push({
        tag: el.tagName.toLowerCase(), href: href, text: text,
        title: el.getAttribute('title'), type: el.getAttribute('type'),
        rel: el.getAttribute('rel'), reasons: reasons
      });
    });

    // Background requests the page made while rendering: often the JSON API behind the page
    out.xhr_requests = performance.getEntriesByType('resource').filter(function (r) {
      return r.initiatorType === 'fetch' || r.initiatorType === 'xmlhttprequest';
    }).slice(0, 150).map(function (r) {
      return { url: r.name, initiator: r.initiatorType, status: r.responseStatus || null, content_type: r.contentType || null };
    });

    // Everything the page loaded (scripts, iframes, images, trackers, ad networks...)
    var hosts = {};
    out.resources = performance.getEntriesByType('resource').slice(0, 600).map(function (r) {
      try { var h = new URL(r.name).host; if (h !== location.host) hosts[h] = (hosts[h] || 0) + 1; } catch (e) {}
      return { url: r.name.length > 500 ? r.name.slice(0, 500) : r.name, initiator: r.initiatorType,
        status: r.responseStatus || null, content_type: r.contentType || null, bytes: r.transferSize || null };
    });
    out.third_party_hosts = hosts;
    out.scripts = all('script[src]').map(function (s) { return s.src; }).slice(0, 200);

    out.iframes = all('iframe[src]').map(function (f) { return f.src; }).slice(0, 30);
    // Content of same-origin frames (old <frameset> sites keep the actual record in a child frame)
    out.frames = all('frame, iframe').slice(0, 20).map(function (f) {
      var entry = { name: f.name || null, src: f.src || null, same_origin: false };
      try {
        var d = f.contentDocument;
        if (d && d.documentElement) {
          entry.same_origin = true;
          entry.title = d.title;
          entry.url = d.location.href;
          entry.text = d.body ? (d.body.innerText || '') : '';
          entry.text_length = entry.text.length;
          entry.html = d.documentElement.outerHTML;
        }
      } catch (e) { /* cross-origin */ }
      return entry;
    });
    out.forms = all('form').slice(0, 30).map(function (f) {
      return { action: abs(f.getAttribute('action') || ''), method: f.getAttribute('method'), id: f.id || null };
    });

    // Signals only; the crawler (and later, a human) decides what they mean
    var text = document.body ? (document.body.innerText || '') : '';
    var words = function (re) {
      var found = {};
      var m = text.slice(0, 30000).match(re) || [];
      m.forEach(function (w) { found[w.toLowerCase()] = 1; });
      return Object.keys(found);
    };
    var CHALLENGE_SEL = ['#challenge-form', '#challenge-running', '#cf-challenge-running', '#challenge-error-text',
      '.cf-turnstile', 'iframe[src*="challenges.cloudflare.com"]', 'iframe[src*="recaptcha"]', 'iframe[src*="hcaptcha"]',
      '.g-recaptcha', '.h-captcha', '#px-captcha', 'iframe[src*="captcha-delivery"]', '#anubis-challenge', 'script[src*="_Incapsula_"]',
      'iframe[src*="_Incapsula_"]', 'iframe[src*="/cdn-cgi/challenge-platform"]', 'script[src*="/cdn-cgi/challenge-platform"]', 'form[action*="/cdn-cgi/"]'];
    out.signals = {
      challenge_title: /just a moment|attention required|checking (your|the) browser|verifying your browser|checking (your )?connection|not to be a robot|verif(y|ying) (you are|that you are|you're) (a )?human|are you a (robot|human)|security check|pardon our interruption|human verification|bot (verification|check)|access denied|request (blocked|rejected)|ddos|making sure you(’|')re not a bot|un momento|einen moment/i.test(document.title || ''),
      challenge_elements: CHALLENGE_SEL.filter(function (s) { return document.querySelector(s); }),
      challenge_words: words(/verify you are human|checking your browser|unusual traffic|enable javascript and cookies|you have been blocked|are you a robot|complete the security check|please complete the captcha|solve the captcha/gi),
      password_inputs: all('input[type="password"]').length,
      access_words: words(/subscribe|subscription|subscribers? only|sign in|sign up|log ?in|institutional access|purchase|paywall|free trial|members? only|register to|access denied|not authorized|unauthorized|forbidden/gi),
      not_found_words: words(/page not found|not found|no (results|records?|matches) (found|were found)|does not exist|no longer available|404|error/gi)
    };

    out.text_length = text.length;
    out.text = text;
    var doctype = document.doctype ? new XMLSerializer().serializeToString(document.doctype) + '\n' : '';
    out.html = doctype + document.documentElement.outerHTML;
    out.html_length = out.html.length;
  } catch (e) {
    out.extract_error = String(e && e.stack ? e.stack : e);
  }
  return JSON.stringify(out);
})();
