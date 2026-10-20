# Source quality report - Q7245

416 pages crawled for 315 identifier properties (sites). Counts below are per **site** unless they say pages; a site counts as having a property if any of its pages did.

## 1. Did the page resolve?

| status | pages | share |
|---|---|---|
| ok | 318 | 76% |
| load_failed | 58 | 14% |
| wrong_page | 22 | 5% |
| http_error | 13 | 3% |
| challenge_suspected | 2 | 0% |
| blocked | 2 | 0% |
| login_wall_suspected | 1 | 0% |

Status meanings: `ok` rendered normally; `login_wall_suspected` the page has a password box (the record itself may still be public); `http_error` 4xx/5xx; `load_failed` the browser never got a usable page (DNS, connection reset, site down); `blocked` an explicit refusal page; `wrong_page` the browser rendered a page, but not the entity's record (a Wayback calendar, a redirector that never forwarded, a challenge page the crawler did not recognise, or a page that never mentions the entity and yielded no data about them).

Wrong-page sites (18):

| prop | site | why |
|---|---|---|
| P213 | ISNI | '(Spirit)' heading: a library record for books channelled through a medium, not him |
| P8902 | Archives at Yale agent ID | '(Spirit)' heading: a library record for books channelled through a medium, not him |
| P4657 | The Numbers person ID (archived) | Wayback calendar page, not an archived snapshot |
| P5019 | Brockhaus Enzyklopädie online ID | not-found wording on a short page that never mentions the entity |
| P1017 | Vatican Library ID (former scheme) | page heading is not him (another of this property's values is his record) |
| P14178 | Obálky knih ID | page heading is not him (another of this property's values is his record) |
| P1430 | Open Plaques subject ID | page heading is not him (another of this property's values is his record) |
| P3065 | RERO ID (legacy) | page heading is not him (another of this property's values is his record) |
| P3348 | National Library of Greece ID | page heading is not him (another of this property's values is his record) |
| P691 | NL CR AUT ID | page heading is not him (another of this property's values is his record) |
| P11137 | Reddit topic ID (obsolete) | page rendered but never mentions the entity |
| P13437 | Chtyvo author ID | page rendered but never mentions the entity |
| P3569 | Cultureel Woordenboek ID | page rendered but never mentions the entity |
| P6868 | Hoopla artist ID | page rendered but never mentions the entity |
| P7369 | National Library of Chile ID | page rendered but never mentions the entity |
| P7574 | Swedish Royal Theater Archive | page rendered but never mentions the entity |
| P8445 | Our Campaigns candidate ID | page rendered but never mentions the entity |
| P9522 | Biblioteca di Santa Sabina ID | record for a different person ('Muguet, Christian (Nomi di persona)') |

- pages crawled at an overridden URL (`url_overrides.json`): 8 (P1017, P1580, P2089, P2924, P5068, P8034, P9001)
- sites with at least one page rendering normally: **278 (88%)**
- pages that hit the 45 s load timeout: 9 (2%) (dspace.wbpublibnet.gov.in, feb-web.ru, kopkatalogs.lv, nationallibraryopac.nvli.in, webservices.nlr.ru, www.muziekweb.nl)
- pages redirected to another host: 48 (12%)
- pages served over https: 408 (98%)
- median load time: 6.2 s; slowest 5: viaf.org 1834s, ixtheo.de 1822s, viaf.org 1822s, www.europeana.eu 135s, nationallibraryopac.nvli.in 49s

Failures by host: nationallibraryopac.nvli.in ×44, viaf.org ×4, dspace.wbpublibnet.gov.in ×3, kopkatalogs.lv ×2, webservices.nlr.ru ×2, armunicat.nla.am ×2, id.bnportugal.gov.pt ×1, data.bibliotheken.nl ×1, library.trikalacity.gr ×1, www.bbc.co.uk ×1

## 2. Walls: challenges, logins, consent

- sites that loaded a human-verification widget (reCAPTCHA, hCaptcha, Turnstile, Incapsula...): 52 (17%)
- sites where the crawl actually paused for a human: 18 (6%)
- sites with a password box on the page: 34 (11%)
- sites with a cookie-consent manager: 96 (30%)
- pages with access wording (subscribe, members, log in...): 139 (33%)
- pages with not-found wording: 28 (7%)

## 3. Advertising and tracking

| ads | sites | share |
|---|---|---|
| none | 255 | 81% |
| ads served | 58 | 18% |
| ad slots in markup, nothing loaded | 2 | 1% |

"ads served" = the rendered page requested at least one ad-network host (DoubleClick, Google Ad Manager, PubMatic, Criteo, Rubicon, Amazon ads, prebid partners...). Analytics (Google Analytics, Tag Manager, Clarity, New Relic...) are counted separately.

- sites with analytics/tracking scripts: 180 (57%)
- sites with social widgets/pixels: 41 (13%)
- sites with **no** third-party hosts at all: 48 (15%)
- sites with 20+ third-party hosts: 38 (12%)

Sites serving ads (ad hosts contacted):

| property | label | ad_hosts | third_party_hosts | analytics_hosts |
|---|---|---|---|---|
| P11194 | Famous Birthdays ID | 86 | 111 | 0 |
| P3478 | Songkick artist ID | 77 | 106 | 0 |
| P12153 | FilmAffinity person or company ID | 67 | 97 | 4 |
| P10757 | Personality Database profile ID | 64 | 106 | 5 |
| P535 | Find a Grave memorial ID | 58 | 103 | 6 |
| P5905 | Comic Vine ID | 56 | 80 | 4 |
| P2373 | Genius artist ID | 54 | 106 | 11 |
| P6262 | Fandom article ID | 47 | 90 | 5 |
| P5421 | Trading Card Database name ID | 42 | 61 | 3 |
| P7553 | Sinemalar person ID | 42 | 79 | 5 |
| P3630 | Babelio author ID | 40 | 71 | 4 |
| P1417 | Encyclopædia Britannica Online ID | 38 | 75 | 9 |
| P2605 | ČSFD person ID | 38 | 73 | 2 |
| P5408 | Fantastic Fiction author ID | 36 | 62 | 3 |
| P6706 | De Agostini ID | 34 | 69 | 5 |
| P11227 | AniList staff ID | 33 | 68 | 3 |
| P3219 | Encyclopædia Universalis ID | 31 | 49 | 0 |
| P3365 | Treccani ID | 31 | 41 | 3 |
| P4084 | MyAnimeList people ID | 24 | 34 | 0 |
| P4223 | Treccani's Enciclopedia Italiana ID | 23 | 33 | 3 |
| P12098 | Kinobox person ID | 22 | 59 | 10 |
| P345 | IMDb ID | 22 | 42 | 3 |
| P10400 | CBDB.cz author ID | 20 | 44 | 4 |
| P4666 | CineMagia person ID | 19 | 42 | 2 |
| P11449 | TV Maze person ID | 18 | 28 | 0 |
| P1953 | Discogs artist ID | 17 | 21 | 1 |
| P10387 | Databazeknih.cz author ID | 16 | 37 | 3 |
| P9995 | MYmovies person ID | 13 | 36 | 3 |
| P2963 | Goodreads author ID | 10 | 22 | 0 |
| P12040 | J. Paul Getty Museum agent ID | 7 | 23 | 5 |
| P245 | Union List of Artist Names ID | 7 | 23 | 4 |
| P9802 | Penguin Random House author ID | 7 | 41 | 10 |
| P13772 | Harper's tag | 5 | 15 | 5 |
| P4159 | WeRelate person ID | 5 | 13 | 3 |
| P5617 | Evene ID | 5 | 16 | 1 |
| P9196 | BookBub author ID | 5 | 28 | 8 |
| P1296 | Gran Enciclopèdia Catalana ID (former scheme) | 4 | 11 | 0 |
| P3368 | Prabook ID | 4 | 9 | 3 |
| P5343 | Poets.org poet ID | 4 | 17 | 9 |
| P5705 | Los Angeles Review of Books author ID | 4 | 12 | 7 |
| P7769 | Australian National Maritime Museum person ID | 4 | 15 | 4 |
| P8969 | CINE21 person ID | 4 | 18 | 3 |
| P3984 | subreddit | 3 | 17 | 1 |
| P5618 | LOA ID | 3 | 8 | 4 |
| P646 | Freebase ID | 3 | 14 | 1 |
| P13255 | L'Humanité topic ID | 2 | 25 | 4 |
| P5341 | Poetry Foundation ID | 2 | 10 | 4 |
| P5562 | Tebeosfera ID | 2 | 10 | 4 |
| P8189 | J9U entity ID | 2 | 29 | 9 |
| P9459 | Rekhta author ID | 2 | 24 | 8 |
| P12385 | Gran Enciclopèdia Catalana ID | 1 | 8 | 0 |
| P13204 | Wellcome Collection concept ID | 1 | 8 | 2 |
| P1816 | National Portrait Gallery (London) person ID | 1 | 6 | 2 |
| P2435 | PORT person ID | 1 | 24 | 5 |
| P3417 | Quora topic ID | 1 | 10 | 1 |
| P650 | RKDartists ID | 1 | 3 | 2 |
| P6645 | Stedelijk Museum Amsterdam ID | 1 | 9 | 2 |
| P11394 | Internet Sacred Text Archive ID | 0 | 3 | 1 |

Most common ad hosts: ad.doubleclick.net (22), ep1.adtrafficquality.google (18), ep2.adtrafficquality.google (17), googleads.g.doubleclick.net (17), c.amazon-adsystem.com (17), cm.g.doubleclick.net (16), a.ad.gt (15), pagead2.googlesyndication.com (14), ads.pubmatic.com (13), cdn.id5-sync.com (13), ad-delivery.net (10), ad.360yield.com (10)

## 4. Page weight

- rendered HTML: median 83, 90th pct 510, max 2358 KB
- visible text: median 2330, 90th pct 10553, max 311231 characters
- resources loaded: median 47, 90th pct 131, max 359
- scripts: median 14, 90th pct 38, max 101
- third-party hosts: median 5, 90th pct 28, max 111
- pages with under 500 characters of visible text (thin or empty): 16 (4%)

## 5. Machine-readable data

- sites where at least one structured file was retrieved (any content, including page plumbing like consent configs): 274 (87%)
- sites whose files contained **data about the entity** (profiled in step 6): **283 (90%)**
- sites whose entity data came as RDF (JSON-LD, RDF/XML, Turtle, N-Triples, RDFa): 94 (30%)
- sites with a library format (MARC, MADS, EAC-CPF): 9 (3%)

### Serialisations (sites offering each, any route)

| format | sites retrieved | share | carried entity data | share |
|---|---|---|---|---|
| rdfa | 237 | 75% | 42 | 13% |
| json | 168 | 53% | 48 | 15% |
| opengraph | 133 | 42% | 0 | 0% |
| json-ld | 94 | 30% | 46 | 15% |
| microdata | 39 | 12% | 26 | 8% |
| rdf-xml | 30 | 10% | 14 | 4% |
| feed | 23 | 7% | 0 | 0% |
| xml | 18 | 6% | 0 | 0% |
| turtle | 16 | 5% | 7 | 2% |
| n-triples | 6 | 2% | 0 | 0% |
| marcxml | 6 | 2% | 4 | 1% |
| marc-binary | 2 | 1% | 1 | 0% |
| eac-cpf | 2 | 1% | 2 | 1% |
| csv | 1 | 0% | 0 | 0% |
| mads | 1 | 0% | 1 | 0% |

"retrieved" counts any file of that format, including page plumbing (cookie-consent configs, xhtml-vocab RDFa, OpenGraph cards); "carried entity data" counts only files the step-6 profile actually took values about the person from. `json` and `xml` are ad-hoc API payloads; `opengraph` is page metadata only (title/description/image).

### How the data was reachable

| mechanism | sites retrieved | share | carried entity data | share |
|---|---|---|---|---|
| embedded rdfa | 237 | 75% | 42 | 13% |
| page XHR/API | 159 | 50% | 27 | 9% |
| embedded opengraph | 133 | 42% | 0 | 0% |
| embedded json-ld | 66 | 21% | 37 | 12% |
| content negotiation | 40 | 13% | 19 | 6% |
| embedded microdata | 39 | 12% | 26 | 8% |
| link rel=alternate | 30 | 10% | 9 | 3% |
| export link | 30 | 10% | 22 | 7% |
| replayed API call | 1 | 0% | 1 | 0% |

### Programmatic access to the entity data

Based on which files the step-6 profile actually took values from. `plain HTTP` = a Python client gets everything (including markup that the probe found in the server-sent HTML); `browser` = the data only came back from fetches run inside the logged-in, bot-cleared browser session or replayed in-page API calls; `js-rendered page` = the only data is markup that appears after JavaScript runs; `rendered page (unprobed)` = embedded markup not re-checked with Python.

| access | sites | share of all sites | share of data sites |
|---|---|---|---|
| page text only (page served to plain HTTP) | 93 | 30% | 33% |
| none | 32 | 10% |  |
| page text only (page blocked for plain HTTP) | 16 | 5% | 6% |
| plain HTTP | 8 | 3% | 3% |
| plain HTTP + page text for 6/10 values | 2 | 1% | 1% |
| plain HTTP + page text for 11/31 values | 2 | 1% | 1% |
| page blocked for plain HTTP only + page text for 3/8 values | 1 | 0% | 0% |
| plain HTTP + page text for 43/107 values | 1 | 0% | 0% |
| plain HTTP + page text for 18/40 values | 1 | 0% | 0% |
| plain HTTP + page text for 7/9 values | 1 | 0% | 0% |
| plain HTTP + page text for 21/31 values | 1 | 0% | 0% |
| plain HTTP + page text for 64/78 values | 1 | 0% | 0% |
| plain HTTP, partly (browser) + page text for 46/99 values | 1 | 0% | 0% |
| plain HTTP + page text for 2/28 values | 1 | 0% | 0% |
| plain HTTP + page text for 14/31 values | 1 | 0% | 0% |
| plain HTTP + page text for 16/274 values | 1 | 0% | 0% |
| plain HTTP + page text for 7/21 values | 1 | 0% | 0% |
| plain HTTP + page text for 19/29 values | 1 | 0% | 0% |
| plain HTTP + page text for 4/8 values | 1 | 0% | 0% |
| plain HTTP + page text for 8/10 values | 1 | 0% | 0% |
| plain HTTP + page text for 12/17 values | 1 | 0% | 0% |
| plain HTTP + page text for 3/14 values | 1 | 0% | 0% |
| plain HTTP, partly (page blocked for plain HTTP) + page text for 16/53 values | 1 | 0% | 0% |
| plain HTTP + page text for 22/25 values | 1 | 0% | 0% |
| plain HTTP + page text for 14/61 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 55/60 values | 1 | 0% | 0% |
| plain HTTP + page text for 12/30 values | 1 | 0% | 0% |
| plain HTTP + page text for 38/78 values | 1 | 0% | 0% |
| plain HTTP + page text for 1/13 values | 1 | 0% | 0% |
| plain HTTP + page text for 11/39 values | 1 | 0% | 0% |
| browser only + page text for 20/47 values | 1 | 0% | 0% |
| plain HTTP + page text for 9/52 values | 1 | 0% | 0% |
| plain HTTP + page text for 19/219 values | 1 | 0% | 0% |
| plain HTTP + page text for 6/13 values | 1 | 0% | 0% |
| plain HTTP + page text for 63/66 values | 1 | 0% | 0% |
| browser only + page text for 2/17 values | 1 | 0% | 0% |
| browser only + page text for 13/80 values | 1 | 0% | 0% |
| plain HTTP + page text for 22/47 values | 1 | 0% | 0% |
| plain HTTP + page text for 7/25 values | 1 | 0% | 0% |
| plain HTTP + page text for 25/28 values | 1 | 0% | 0% |
| plain HTTP + page text for 94/160 values | 1 | 0% | 0% |
| plain HTTP + page text for 27/79 values | 1 | 0% | 0% |
| plain HTTP + page text for 12/15 values | 1 | 0% | 0% |
| plain HTTP + page text for 4/5 values | 1 | 0% | 0% |
| plain HTTP + page text for 13/15 values | 1 | 0% | 0% |
| plain HTTP + page text for 32/55 values | 1 | 0% | 0% |
| plain HTTP + page text for 7/12 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 64/77 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 3/13 values | 1 | 0% | 0% |
| plain HTTP + page text for 4/21 values | 1 | 0% | 0% |
| plain HTTP, partly (page blocked for plain HTTP) + page text for 25/73 values | 1 | 0% | 0% |
| plain HTTP + page text for 2/18 values | 1 | 0% | 0% |
| plain HTTP, partly (js-rendered page) + page text for 75/200 values | 1 | 0% | 0% |
| plain HTTP + page text for 11/26 values | 1 | 0% | 0% |
| plain HTTP + page text for 17/23 values | 1 | 0% | 0% |
| plain HTTP + page text for 25/51 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 51/58 values | 1 | 0% | 0% |
| plain HTTP + page text for 58/64 values | 1 | 0% | 0% |
| browser only + page text for 86/170 values | 1 | 0% | 0% |
| browser only + page text for 105/748 values | 1 | 0% | 0% |
| plain HTTP + page text for 19/51 values | 1 | 0% | 0% |
| plain HTTP + page text for 56/329 values | 1 | 0% | 0% |
| plain HTTP + page text for 9/14 values | 1 | 0% | 0% |
| plain HTTP + page text for 25/34 values | 1 | 0% | 0% |
| plain HTTP + page text for 103/1469 values | 1 | 0% | 0% |
| browser only + page text for 33/57 values | 1 | 0% | 0% |
| plain HTTP + page text for 1/3 values | 1 | 0% | 0% |
| js-rendered page only + page text for 64/185 values | 1 | 0% | 0% |
| plain HTTP, partly (js-rendered page) + page text for 53/61 values | 1 | 0% | 0% |
| plain HTTP + page text for 62/99 values | 1 | 0% | 0% |
| plain HTTP + page text for 27/64 values | 1 | 0% | 0% |
| plain HTTP + page text for 56/72 values | 1 | 0% | 0% |
| plain HTTP + page text for 15/27 values | 1 | 0% | 0% |
| plain HTTP, partly (js-rendered page) + page text for 34/65 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 82/92 values | 1 | 0% | 0% |
| plain HTTP + page text for 43/97 values | 1 | 0% | 0% |
| js-rendered page only + page text for 25/33 values | 1 | 0% | 0% |
| plain HTTP + page text for 77/167 values | 1 | 0% | 0% |
| plain HTTP + page text for 46/49 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 28/41 values | 1 | 0% | 0% |
| plain HTTP + page text for 5/9 values | 1 | 0% | 0% |
| browser only + page text for 28/1619 values | 1 | 0% | 0% |
| browser / page blocked for plain HTTP only + page text for 33/46 values | 1 | 0% | 0% |
| plain HTTP + page text for 2/3 values | 1 | 0% | 0% |
| plain HTTP + page text for 17/33 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 30/57 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 26/41 values | 1 | 0% | 0% |
| plain HTTP + page text for 78/112 values | 1 | 0% | 0% |
| plain HTTP + page text for 1/15 values | 1 | 0% | 0% |
| plain HTTP, partly (browser) + page text for 6/39 values | 1 | 0% | 0% |
| plain HTTP + page text for 19/25 values | 1 | 0% | 0% |
| plain HTTP + page text for 5/17 values | 1 | 0% | 0% |
| browser / page blocked for plain HTTP only + page text for 65/81 values | 1 | 0% | 0% |
| plain HTTP + page text for 50/53 values | 1 | 0% | 0% |
| plain HTTP + page text for 32/78 values | 1 | 0% | 0% |
| js-rendered page only + page text for 61/108 values | 1 | 0% | 0% |
| plain HTTP + page text for 11/13 values | 1 | 0% | 0% |
| plain HTTP + page text for 4/13 values | 1 | 0% | 0% |
| plain HTTP + page text for 57/58 values | 1 | 0% | 0% |
| plain HTTP + page text for 6/15 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 30/76 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 11/24 values | 1 | 0% | 0% |
| plain HTTP + page text for 58/80 values | 1 | 0% | 0% |
| plain HTTP + page text for 4/77 values | 1 | 0% | 0% |
| plain HTTP + page text for 1/10 values | 1 | 0% | 0% |
| plain HTTP + page text for 74/77 values | 1 | 0% | 0% |
| plain HTTP + page text for 11/29 values | 1 | 0% | 0% |
| plain HTTP + page text for 41/53 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 87/89 values | 1 | 0% | 0% |
| plain HTTP + page text for 6/7 values | 1 | 0% | 0% |
| plain HTTP + page text for 42/45 values | 1 | 0% | 0% |
| plain HTTP + page text for 53/56 values | 1 | 0% | 0% |
| plain HTTP + page text for 41/68 values | 1 | 0% | 0% |
| plain HTTP + page text for 2/5 values | 1 | 0% | 0% |
| plain HTTP + page text for 24/34 values | 1 | 0% | 0% |
| plain HTTP + page text for 19/31 values | 1 | 0% | 0% |
| plain HTTP + page text for 5/37 values | 1 | 0% | 0% |
| plain HTTP + page text for 4/6 values | 1 | 0% | 0% |
| plain HTTP, partly (page blocked for plain HTTP) + page text for 30/43 values | 1 | 0% | 0% |
| plain HTTP + page text for 60/75 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 38/60 values | 1 | 0% | 0% |
| plain HTTP + page text for 75/128 values | 1 | 0% | 0% |
| plain HTTP + page text for 29/57 values | 1 | 0% | 0% |
| plain HTTP + page text for 22/179 values | 1 | 0% | 0% |
| plain HTTP + page text for 15/26 values | 1 | 0% | 0% |
| plain HTTP + page text for 6/9 values | 1 | 0% | 0% |
| plain HTTP, partly (js-rendered page) | 1 | 0% | 0% |
| plain HTTP + page text for 29/63 values | 1 | 0% | 0% |
| plain HTTP + page text for 128/217 values | 1 | 0% | 0% |
| plain HTTP + page text for 54/127 values | 1 | 0% | 0% |
| plain HTTP + page text for 25/36 values | 1 | 0% | 0% |
| plain HTTP + page text for 41/143 values | 1 | 0% | 0% |
| plain HTTP + page text for 87/98 values | 1 | 0% | 0% |
| plain HTTP + page text for 45/52 values | 1 | 0% | 0% |
| plain HTTP + page text for 7/10 values | 1 | 0% | 0% |
| plain HTTP + page text for 16/36 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 61/75 values | 1 | 0% | 0% |
| plain HTTP + page text for 27/131 values | 1 | 0% | 0% |
| plain HTTP + page text for 323/472 values | 1 | 0% | 0% |
| plain HTTP + page text for 36/139 values | 1 | 0% | 0% |
| plain HTTP + page text for 42/96 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 4/6 values | 1 | 0% | 0% |
| plain HTTP + page text for 38/66 values | 1 | 0% | 0% |
| plain HTTP + page text for 20/25 values | 1 | 0% | 0% |
| plain HTTP + page text for 24/56 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 30/45 values | 1 | 0% | 0% |
| js-rendered page only + page text for 79/92 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 99/107 values | 1 | 0% | 0% |
| plain HTTP + page text for 51/58 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 5/13 values | 1 | 0% | 0% |
| plain HTTP + page text for 1/18 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 36/63 values | 1 | 0% | 0% |
| plain HTTP + page text for 18/70 values | 1 | 0% | 0% |
| plain HTTP + page text for 7/74 values | 1 | 0% | 0% |
| plain HTTP + page text for 33/36 values | 1 | 0% | 0% |
| plain HTTP + page text for 19/30 values | 1 | 0% | 0% |
| browser / page blocked for plain HTTP only + page text for 5/54 values | 1 | 0% | 0% |
| plain HTTP + page text for 4/41 values | 1 | 0% | 0% |
| page blocked for plain HTTP only + page text for 13/23 values | 1 | 0% | 0% |
| plain HTTP + page text for 6/11 values | 1 | 0% | 0% |
| browser / page blocked for plain HTTP only + page text for 37/208 values | 1 | 0% | 0% |
| js-rendered page only + page text for 29/37 values | 1 | 0% | 0% |
| plain HTTP + page text for 4/7 values | 1 | 0% | 0% |
| plain HTTP + page text for 20/48 values | 1 | 0% | 0% |
| browser only + page text for 55/91 values | 1 | 0% | 0% |
| plain HTTP + page text for 60/122 values | 1 | 0% | 0% |
| plain HTTP + page text for 2/32 values | 1 | 0% | 0% |
| plain HTTP + page text for 18/23 values | 1 | 0% | 0% |

### Embedded markup: present for a plain HTTP client?

345 pages with embedded data were re-fetched with Python (no JavaScript, a plain research User-Agent): 199 had the same markup in the server HTML, 36 only had it after JavaScript ran, 71 refused the plain request.

JavaScript-only embedded data: P1017 web.archive.org (rdfa), P1017 web.archive.org (rdfa), P10757 www.personality-database.com (rdfa), P1225 catalog.archives.gov (rdfa), P1225 catalog.archives.gov (rdfa), P12458 parsifal.urbe.it (rdfa), P12458 parsifal.urbe.it (rdfa), P12458 parsifal.urbe.it (rdfa), P1280 plus-legacy.cobiss.net (opengraph, rdfa), P12836 www.douban.com (opengraph), P12854 app.plex.tv (rdfa), P14536 collections.fes.de (rdfa), P1695 dbn.bn.org.pl (json-ld, opengraph, rdfa), P2089 web.archive.org (rdfa), P2600 www.geni.com (microdata, opengraph), P271 ci.nii.ac.jp (rdfa), P2889 ancestors.familysearch.org (json-ld, opengraph, rdfa), P2977 www.lordbyron.org (rdfa), P3219 www.universalis.fr (json-ld, opengraph, rdfa), P3794 dictionaryofsydney.org (rdfa), P3984 www.reddit.com (rdfa), P434 musicbrainz.org (json-ld, rdfa), P4657 web.archive.org (rdfa), P5562 www.tebeosfera.com (opengraph), P5739 catalogo.pusc.it (rdfa), P6441 www.douban.com (opengraph), P646 www.google.com (microdata, rdfa), P650 research.rkd.nl (rdfa), P6698 jpsearch.go.jp (microdata, rdfa), P7293 dbn.bn.org.pl (opengraph, rdfa), P8168 database.factgrid.de (opengraph, rdfa), P8849 plus-legacy.cobiss.net (opengraph, rdfa), P8851 plus-legacy.cobiss.net (opengraph, rdfa), P9556 www.ltit.it (json-ld), P9629 www.armeniapedia.org (rdfa), P9984 cantic.bnc.cat (rdfa)

Refused the Python request (status): P10018 collections.eastman.org (403), P10883 sf-encyclopedia.com (404), P11249 opac.kbr.be (403), P11407 www.ozon.ru (307), P11408 dic.pixiv.net (403), P11496 cir.nii.ac.jp (202), P1185 en.rodovid.org (503), P12098 www.kinobox.cz (403), P1213 opac.nlc.cn (timed out), P12385 www.enciclopedia.cat (503), P1296 www.enciclopedia.cat (503), P13166 oseegenius.unigre.it (403), P1417 www.britannica.com (403), P14211 cisug-usc.primo.exlibrisgroup.com (403), P14225 bukinet-mreza.primo.exlibrisgroup.com (403), P1816 www.npg.org.uk (403), P1953 www.discogs.com (403), P2188 biblionet.gr (500), P244 id.loc.gov (403), P244 id.loc.gov (403), P244 id.loc.gov (403), P244 id.loc.gov (403), P2734 www.unz.com (403), P2949 www.wikitree.com (202), P2966 archives.library.wales (403), P3368 prabook.com (403), P3417 www.quora.com (403), P345 www.imdb.com (202), P3553 www.zhihu.com (403), P3630 www.babelio.com (403), P3762 biblioteche.medialibrary.it (403), P4081 www.biodiversitylibrary.org (403), P4159 www.werelate.org (403), P4399 enciclopedia.itaucultural.org.br (403), P4457 adp.library.ucsb.edu (403), P4666 www.cinemagia.ro (403), P4823 www.anb.org (403), P5034 lod.nl.go.kr (404), P5408 www.fantasticfiction.com (405), P5421 www.tcdb.com (403), P5705 lareviewofbooks.org (404), P5714 reactormag.com (403), P5905 comicvine.gamespot.com (403), P6262 disney.fandom.com (403), P6262 literature.fandom.com (403), P6645 www.stedelijk.nl (202), P6821 www.alvin-portal.org (403), P7400 www.librarything.com (403), P7520 www.filmovyprehled.cz (403), P7689 www.onlinenevada.org (500), P7689 www.onlinenevada.org (500), P7704 www.europeana.eu (403), P7769 collections.sea.museum (403), P8094 en.geneastar.org (403), P8189 www.nli.org.il (403), P8189 www.nli.org.il (403), P8591 www.oxfordmusiconline.com (403), P8795 opac.diamondrda.org (403), P8833 armunicat.nla.am (403), P8833 armunicat.nla.am (403), P8833 armunicat.nla.am (403), P8902 archives.yale.edu (202), P8902 archives.yale.edu (202), P9097 library.aarome.org (429), P9097 library.aarome.org (429), P9178 bfsopac.org (403), P9196 www.bookbub.com (403), P9322 ipac.svkkl.cz (404), P950 datos.bne.es (403), P950 datos.bne.es (403), P9707 www.comics.org (403)

Sites where some format was only retrievable in the browser (24): P10608 FID performing arts ID (rdf-xml), P11496 CiNii Research ID (json-ld), P1185 Rodovid ID (feed), P12483 PMB – Personen der Moderne Basis person ID (json), P12674 Kunstenpunt Knowledge Graph ID (feed, json, json-ld, n-triples, rdf-xml, turtle), P12749 SNARC ID (feed, json, json-ld, n-triples, rdf-xml, turtle), P13030 Münzkabinett ID (csv), P1315 NLA Trove people ID (json), P1417 Encyclopædia Britannica Online ID (xml), P1977 Les Archives du spectacle person ID (feed), P213 ISNI (json-ld, rdf-xml), P214 VIAF cluster ID (rdf-xml), P245 Union List of Artist Names ID (json-ld), P2966 National Library of Wales Authority ID (xml), P3430 SNAC ARK ID (eac-cpf, json), P396 SBN author ID (json), P3984 subreddit (json), P4159 WeRelate person ID (rdf-xml), P4342 Great Norwegian Encyclopedia ID (json), P7400 LibraryThing author ID (xml), P8094 GeneaStar person ID (json), P8980 KANTO ID (json), P950 National Library of Spain SpMaBN ID (json-ld, rdf-xml, turtle), P9807 SNK ID (json)

- sites whose data was ad-hoc JSON/XML that needed an LLM (Opus) to map onto the schema: 281 (89%)

## 6. Richness, languages and vocabularies

- schema elements filled per data site: median 13, max 25
- values per data site: median 31, max 1619
- languages tagged per data site: median 1, max 157; sites with values in 5+ languages: 32
- sites publishing with a standard vocabulary (schema.org, SKOS, FOAF, RDA, MADS, BIBFRAME...): 218 (77%) of data sites

Richest sites (by distinct values about the entity):

| property | label | elements | values | languages | formats_used | entity_data_access |
|---|---|---|---|---|---|---|
| P3430 | SNAC ARK ID | 18 | 1619 | 1 | eac-cpf, html, json, rdfa, unknown | browser only + page text for 28/1619 values |
| P244 | Library of Congress Authorities ID | 25 | 1469 | 12 | html, json, json-ld, mads, marcxml, n-triples, rdf-xml, rdfa | plain HTTP + page text for 103/1469 values |
| P214 | VIAF cluster ID | 17 | 748 | 22 | html, json, rdf-xml, rdfa, svg, text | browser only + page text for 105/748 values |
| P7700 | Slovak National Library (VIAF) ID | 24 | 472 | 12 | html, json, marc-json, rdfa, svg, text, unknown | plain HTTP + page text for 323/472 values |
| P227 | GND ID | 24 | 329 | 6 | html, json-ld, marcxml, rdf-xml, turtle | plain HTTP + page text for 56/329 values |
| P10832 | WorldCat Entities ID | 11 | 274 | 157 | json, json-ld, rdfa, text | plain HTTP + page text for 16/274 values |
| P12597 | museum-digital person/organization ID | 18 | 219 | 35 | json | plain HTTP + page text for 19/219 values |
| P7024 | Flemish Public Libraries ID | 8 | 217 | 6 | html, json, marc-json, rdfa, svg, text, unknown | plain HTTP + page text for 128/217 values |
| P950 | National Library of Spain SpMaBN ID | 17 | 208 | 2 | html, json-ld, opengraph, rdf-xml, rdfa, turtle | browser / page blocked for plain HTTP only + page text for 37/208 values |
| P1695 | NLP ID | 22 | 200 | 3 | html, json, json-ld, opengraph, rdfa, unknown | plain HTTP, partly (js-rendered page) + page text for 75/200 values |
| P2600 | Geni profile ID | 25 | 185 | 5 | json, microdata, opengraph | js-rendered page only + page text for 64/185 values |
| P648 | Open Library ID | 21 | 179 | 5 | html, json, microdata, opengraph, rdf-xml, rdfa | plain HTTP + page text for 22/179 values |
| P10227 | National Library of Ireland ID | 19 | 176 | 1 | html, json, marc-json, rdfa, svg, text, unknown | plain HTTP |
| P213 | ISNI | 20 | 170 | 10 | html, json-ld, rdf-xml, rdfa | browser only + page text for 86/170 values |
| P3280 | BAnQ authority ID | 21 | 167 | 6 | html, json, marc-json, rdfa, svg, text, unknown | plain HTTP + page text for 77/167 values |

## 7. Unique versus repeated information

For every descriptive value (names, dates, places, gender, occupations, nationality, language, descriptions, works, related people) we count on how many sites the same normalised value appears. A value found on only one site is *unique* to that site; record plumbing (identifiers, timestamps, licences) is excluded.

- descriptive values across all data sites: 12304; unique to one site: 5480 (45%); repeated elsewhere: 6824 (55%)
- sites contributing nothing that another site does not also have: 50 (18%) of data sites
- sites where more than half of their descriptive values are unique: 40

Most unique sites (≥10 descriptive values):

| property | label | descriptive_values | unique_values | unique_share | values_not_in_wikidata |
|---|---|---|---|---|---|
| P2191 | Vegetti Catalog of Fantastic Literature NILF ID | 39 | 32 | 0.82 | 33 |
| P1977 | Les Archives du spectacle person ID | 57 | 43 | 0.75 | 22 |
| P2188 | BiblioNet author ID | 58 | 43 | 0.74 | 45 |
| P4514 | Africultures person ID | 11 | 8 | 0.73 | 2 |
| P1309 | EGAXA ID | 81 | 58 | 0.72 | 22 |
| P7024 | Flemish Public Libraries ID | 163 | 128 | 0.72 | 40 |
| P11192 | Piraeus Bank Group Cultural Foundation Library (A) ID | 14 | 10 | 0.71 | 5 |
| P1816 | National Portrait Gallery (London) person ID | 20 | 14 | 0.7 | 0 |
| P2734 | Unz Review author ID | 27 | 18 | 0.67 | 16 |
| P8980 | KANTO ID | 49 | 32 | 0.65 | 6 |
| P1006 | Nationale Thesaurus voor Auteursnamen ID | 90 | 58 | 0.64 | 44 |
| P3430 | SNAC ARK ID | 1415 | 1334 | 0.64 | 31 |
| P1385 | Enciclopédia Açoriana ID | 13 | 8 | 0.62 | 1 |
| P2435 | PORT person ID | 29 | 18 | 0.62 | 17 |
| P5562 | Tebeosfera ID | 49 | 30 | 0.61 | 40 |

Most redundant sites (≥10 descriptive values, lowest unique share):

| property | label | descriptive_values | unique_values | unique_share | wd_match |
|---|---|---|---|---|---|
| P11686 | University of Barcelona authority ID | 20 | 0 | 0.0 | 3 |
| P1207 | NUKAT ID | 12 | 0 | 0.0 | 3 |
| P12451 | Arabic Ontology lexical concept ID | 10 | 0 | 0.0 | 4 |
| P1315 | NLA Trove people ID | 35 | 0 | 0.0 | 3 |
| P13183 | JudaicaLink person (GND) ID | 47 | 0 | 0.0 | 2 |
| P14214 | Foto Atlas taxonomy ID | 13 | 0 | 0.0 | 5 |
| P14536 | FES digital collections entity ID | 11 | 0 | 0.0 | 5 |
| P1890 | CCAB ID | 19 | 0 | 0.0 | 4 |
| P1899 | LibriVox author ID | 11 | 0 | 0.0 | 7 |
| P245 | Union List of Artist Names ID | 29 | 0 | 0.0 | 9 |

## 8. Against Wikidata

- data sites with at least one element matching Wikidata exactly: 280 (99%)
- data sites with a mismatch on some element: 11 (4%)
- data sites offering values Wikidata does not have (after normalisation, before curation): 243 (86%)
- see `beyond_wikidata.md` for the curated list of what those values are, and `review.md` for the judged disagreements

## 8b. Quality by popularity

Sites bucketed by how many bibliographic entities (items with P244) carry their identifier.

| popularity | sites | resolved | entity data | all via plain HTTP | RDF | ads | consent banner | median values |
|---|---|---|---|---|---|---|---|---|
| top 50 | 47 | 41 (87%) | 43 (91%) | 2 (4%) | 21 (45%) | 7 (15%) | 16 (34%) | 53 |
| 51-150 | 63 | 54 (86%) | 57 (90%) | 2 (3%) | 23 (37%) | 18 (29%) | 21 (33%) | 36 |
| 151-300 | 66 | 60 (91%) | 60 (91%) | 2 (3%) | 19 (29%) | 9 (14%) | 21 (32%) | 28 |
| 301+ | 139 | 123 (88%) | 123 (88%) | 2 (1%) | 31 (22%) | 24 (17%) | 38 (27%) | 21 |

## 9. Per-site table

`rank` / `% of P244 items` = how common this identifier is on bibliographic entities (items with a Library of Congress ID), from `data/landscape/landscape.md`. Sorted by property number. Full detail (one row per page, all ad/analytics hosts) is in `quality_records.csv`; this table is `quality_sites.csv`.

| prop | site | rank | % of P244 items | pages | status | load s | challenge | login box | consent | ads | analytics | 3rd-party | HTML KB | files | formats (python) | browser only | embedded | entity data access | elements | values | langs | unique | =WD | ≠WD | not in WD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P213 | ISNI | 3 | 71.95 | 6 | ok×5, wrong_page | 4.2 | False | False | False | none | 0 | 0 | 48 | 16 |  | json-ld, rdf-xml | rdfa | browser only + page text for 86/170 values | 20 | 170 | 10 | 0.22 | 9 | 0 | 50 |
| P214 | VIAF cluster ID | 2 | 95.98 | 4 | ok×4 | 5.1 | False | False | True | none | 4 | 6 | 1348 | 68 | json | rdf-xml | rdfa | browser only + page text for 105/748 values | 17 | 748 | 22 | 0.48 | 8 | 0 | 262 |
| P227 | GND ID | 5 | 56.08 | 5 | ok×5 | 5.6 | False | False | False | none | 0 | 3 | 59 | 30 | json-ld, marcxml, rdf-xml, turtle |  |  | plain HTTP + page text for 56/329 values | 24 | 329 | 6 | 0.19 | 10 | 0 | 134 |
| P244 | Library of Congress Authorities ID | 1 | 100.0 | 4 | ok×4 | 5.2 | False | False | False | none | 1 | 3 | 72 | 112 | json, json-ld, mads, marcxml, n-triples, rdf-xml |  | rdfa | plain HTTP + page text for 103/1469 values | 25 | 1469 | 12 | 0.56 | 10 | 0 | 837 |
| P245 | Union List of Artist Names ID | 69 | 3.82 | 1 | ok | 3.6 | False | False | False | ads served | 4 | 23 | 62 | 2 |  | json-ld |  | browser only + page text for 33/57 values | 20 | 57 | 1 | 0.0 | 9 | 0 | 5 |
| P268 | Bibliothèque nationale de France ID | 10 | 32.5 | 1 | ok | 4.1 | False | False | False | none | 0 | 4 | 83 | 2 |  |  | opengraph, rdfa | page text only (page served to plain HTTP) | 20 | 29 | 1 | 0.0 | 10 | 0 | 2 |
| P269 | IdRef ID | 7 | 43.44 | 1 | ok | 4.1 | False | True | False | none | 1 | 4 | 22 | 6 | json, marcxml, rdf-xml |  |  | plain HTTP + page text for 27/64 values | 21 | 64 | 3 | 0.43 | 11 | 0 | 6 |
| P271 | NACSIS-CAT author ID | 23 | 12.04 | 1 | ok | 4.6 | False | False | False | none | 1 | 1 | 66 | 6 | json-ld, rdf-xml |  | rdfa | plain HTTP + page text for 56/72 values | 9 | 72 | 6 | 0.53 | 3 | 0 | 14 |
| P345 | IMDb ID | 29 | 10.17 | 1 | ok | 4.7 | False | False | True | ads served | 3 | 42 | 2112 | 26 | json |  | json-ld, opengraph, rdfa | browser / page blocked for plain HTTP only + page text for 33/46 values | 16 | 46 | 1 | 0.18 | 5 | 0 | 13 |
| P349 | NDL Authority ID | 41 | 6.41 | 1 | ok | 4.1 | False | False | False | none | 0 | 1 | 15 | 9 | json, json-ld, rdf-xml, turtle |  | rdfa | plain HTTP + page text for 17/33 values | 12 | 33 | 2 | 0.07 | 2 | 0 | 3 |
| P396 | SBN author ID | 22 | 12.54 | 1 | ok | 4.1 | True | False | True | none | 0 | 6 | 249 | 12 | marc-binary | json | opengraph, rdfa | plain HTTP, partly (browser) + page text for 6/39 values | 18 | 39 | 2 | 0.21 | 10 | 0 | 1 |
| P409 | Libraries Australia ID | 46 | 6.1 | 1 | http_error | 1833.7 | True | False | True | none | 4 | 5 | 216 | 6 | json |  | rdfa | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P434 | MusicBrainz artist ID | 37 | 7.29 | 1 | ok | 4.6 | False | False | False | none | 1 | 2 | 58 | 3 | json-ld |  | json-ld, rdfa | js-rendered page only + page text for 61/108 values | 18 | 108 | 4 | 0.47 | 8 | 0 | 25 |
| P535 | Find a Grave memorial ID | 58 | 4.79 | 2 | ok×2 | 6.8 | True | True | False | ads served | 6 | 103 | 1092 | 24 | json |  | microdata, opengraph, rdfa | plain HTTP + page text for 41/53 values | 18 | 53 | 1 | 0.33 | 7 | 0 | 5 |
| P646 | Freebase ID | 9 | 39.76 | 1 | ok | 5.5 | False | False | False | ads served | 1 | 14 | 2358 | 4 | json |  | microdata, rdfa | page text only (page served to plain HTTP) | 15 | 31 | 1 | 0.07 | 8 | 1 | 11 |
| P648 | Open Library ID | 21 | 12.82 | 1 | ok | 5.7 | False | False | False | none | 0 | 3 | 167 | 7 | json, rdf-xml |  | microdata, opengraph, rdfa | plain HTTP + page text for 22/179 values | 21 | 179 | 5 | 0.52 | 8 | 0 | 64 |
| P650 | RKDartists ID | 91 | 2.74 | 1 | ok | 4.1 | False | False | False | ads served | 2 | 3 | 34 | 8 | json, json-ld, turtle |  | rdfa | plain HTTP | 2 | 3 | 2 | 0.0 | 1 | 0 | 0 |
| P691 | NL CR AUT ID | 15 | 22.58 | 2 | wrong_page×2 | 4.7 | False | False | False | none | 0 | 2 | 22 | 2 | json |  |  | page text only (page served to plain HTTP) | 14 | 31 | 1 | 0.0 | 5 | 0 | 4 |
| P723 | DBNL author ID | 243 | 0.88 | 1 | ok | 5.7 | False | False | False | none | 0 | 1 | 26 | 3 |  |  | json-ld, opengraph, rdfa | plain HTTP + page text for 25/36 values | 15 | 36 | 2 | 0.44 | 7 | 1 | 11 |
| P839 | IMSLP ID | 205 | 1.1 | 1 | ok | 3.7 | False | False | False | none | 8 | 10 | 109 | 2 | json |  | rdfa | page text only (page served to plain HTTP) | 13 | 36 | 6 | 0.23 | 7 | 0 | 11 |
| P866 | Perlentaucher ID | 298 | 0.7 | 1 | ok | 5.7 | False | False | False | none | 2 | 4 | 79 | 1 | feed |  |  | page text only (page served to plain HTTP) | 11 | 42 | 2 | 0.38 | 4 | 0 | 24 |
| P906 | SELIBR ID | 70 | 3.7 | 1 | ok | 6.2 | False | False | False | none | 0 | 1 | 386 | 8 | json-ld, marcxml, turtle |  | opengraph, rdfa | plain HTTP + page text for 33/36 values | 14 | 36 | 7 | 0.0 | 4 | 0 | 12 |
| P947 | RSL ID (person) | 1133 | 0.08 | 1 | ok | 5.7 | False | False | False | none | 2 | 2 | 18 | 0 |  |  |  | page text only (page served to plain HTTP) | 4 | 4 | 1 | 0.0 | 1 | 0 | 0 |
| P949 | National Library of Israel ID (old) | 63 | 4.35 | 1 | http_error | 11.3 | False | False | False | none | 1 | 1 | 2 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P950 | National Library of Spain SpMaBN ID | 25 | 11.05 | 2 | ok×2 | 5.7 | True | False | False | none | 3 | 5 | 137 | 22 |  | json-ld, rdf-xml, turtle | json-ld, opengraph, rdfa | browser / page blocked for plain HTTP only + page text for 37/208 values | 17 | 208 | 2 | 0.38 | 5 | 0 | 30 |
| P1005 | National Library of Portugal ID | 74 | 3.49 | 1 | load_failed | 6.1 | False | False | False | none | 0 | 0 | 136 | 1 |  |  | rdfa | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P1006 | Nationale Thesaurus voor Auteursnamen ID | 11 | 29.43 | 2 | ok, http_error | 5.7 | False | False | False | none | 1 | 1 | 235 | 17 | json |  | json-ld, rdfa | plain HTTP + page text for 43/107 values | 15 | 107 | 4 | 0.64 | 5 | 0 | 44 |
| P1015 | BIBSYS ID | 20 | 13.23 | 1 | ok | 5.1 | False | False | False | none | 0 | 0 | 3 | 0 |  |  |  | page text only (page served to plain HTTP) | 13 | 24 | 1 | 0.08 | 5 | 0 | 1 |
| P1017 | Vatican Library ID (former scheme) | 79 | 3.11 | 2 | wrong_page×2 | 8.3 | False | False | True | none | 0 | 4 | 108 | 4 | json |  | rdfa | page text only (page served to plain HTTP) | 13 | 88 | 6 | 0.47 | 4 | 0 | 21 |
| P1185 | Rodovid ID | 202 | 1.12 | 1 | ok | 6.2 | False | False | False | none | 0 | 1 | 30 | 7 | xml | feed | rdfa | page text only (page blocked for plain HTTP) | 13 | 25 | 1 | 0.41 | 6 | 0 | 0 |
| P1207 | NUKAT ID | 12 | 28.94 | 1 | ok | 8.0 | False | False | True | none | 0 | 1 | 54 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 6 | 13 | 1 | 0.0 | 3 | 0 | 3 |
| P1213 | NLC authorities | 525 | 0.27 | 1 | ok | 18.9 | False | False | False | none | 0 | 0 | 27 | 0 |  |  |  | page text only (page blocked for plain HTTP) | 11 | 33 | 8 | 0.23 | 4 | 0 | 14 |
| P1220 | Internet Broadway Database person ID | 229 | 0.94 | 2 | ok×2 | 4.6 | False | False | False | none | 2 | 5 | 49 | 2 |  |  | rdfa | page text only (page served to plain HTTP) | 11 | 25 | 1 | 0.26 | 5 | 0 | 10 |
| P1225 | U.S. National Archives Identifier | 177 | 1.3 | 2 | ok×2 | 4.8 | False | False | False | none | 3 | 5 | 57 | 12 | json |  | rdfa | plain HTTP + page text for 38/78 values | 16 | 78 | 4 | 0.27 | 6 | 0 | 16 |
| P1233 | ISFDB author ID | 169 | 1.39 | 1 | ok | 45.6 | False | False | False | none | 1 | 2 | 56 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 14 | 65 | 1 | 0.28 | 6 | 0 | 40 |
| P1248 | KulturNav-ID | 264 | 0.81 | 1 | ok | 4.6 | False | False | False | none | 2 | 9 | 99 | 8 | json, json-ld, rdf-xml, xml |  | rdfa | plain HTTP + page text for 9/52 values | 21 | 52 | 2 | 0.11 | 8 | 0 | 17 |
| P1260 | Swedish Open Cultural Heritage URI | 506 | 0.29 | 1 | ok | 6.7 | False | False | True | none | 3 | 5 | 102 | 6 | json-ld, rdf-xml |  | opengraph, rdfa | plain HTTP + page text for 6/13 values | 10 | 13 | 1 | 0.0 | 0 | 0 | 2 |
| P1263 | NNDB people ID | 130 | 1.75 | 1 | ok | 4.1 | False | False | False | none | 0 | 0 | 11 | 1 |  |  | opengraph | plain HTTP + page text for 63/66 values | 15 | 66 | 1 | 0.16 | 10 | 0 | 38 |
| P1280 | CONOR.SI ID | 44 | 6.17 | 1 | ok | 39.8 | False | False | False | none | 0 | 1 | 40 | 2 |  |  | opengraph, rdfa | page text only (page served to plain HTTP) | 9 | 20 | 1 | 0.06 | 4 | 0 | 3 |
| P1296 | Gran Enciclopèdia Catalana ID (former scheme) | 88 | 2.82 | 1 | ok | 10.0 | True | True | False | ads served | 0 | 11 | 140 | 2 | json |  | rdfa | page text only (page blocked for plain HTTP) | 14 | 25 | 2 | 0.08 | 8 | 0 | 10 |
| P1309 | EGAXA ID | 364 | 0.5 | 1 | ok | 3.6 | False | False | True | none | 4 | 5 | 348 | 7 | json |  | rdfa | plain HTTP + page text for 94/160 values | 18 | 160 | 4 | 0.72 | 7 | 0 | 22 |
| P1315 | NLA Trove people ID | 43 | 6.35 | 1 | ok | 14.6 | True | False | False | none | 2 | 6 | 61 | 12 |  | json | rdfa | page text only (page served to plain HTTP) | 10 | 41 | 9 | 0.0 | 3 | 0 | 20 |
| P1368 | National Library of Latvia ID | 45 | 6.14 | 2 | load_failed×2 | 48.7 | False | False | False | none | 0 | 0 | 183 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P1375 | NSK (VIAF) ID | 93 | 2.73 | 1 | ok | 3.6 | False | False | True | none | 4 | 5 | 761 | 12 | json |  | rdfa | page text only (page served to plain HTTP) | 18 | 146 | 11 | 0.4 | 9 | 0 | 48 |
| P1385 | Enciclopédia Açoriana ID | 2360 | 0.02 | 1 | ok | 7.2 | False | False | False | none | 3 | 8 | 83 | 2 | json |  | opengraph | page text only (page served to plain HTTP) | 14 | 21 | 2 | 0.62 | 4 | 1 | 1 |
| P1417 | Encyclopædia Britannica Online ID | 60 | 4.63 | 1 | ok | 10.4 | True | False | True | ads served | 9 | 75 | 1063 | 12 | json | xml | json-ld, opengraph, rdfa | page blocked for plain HTTP only + page text for 64/77 values | 15 | 77 | 1 | 0.32 | 8 | 0 | 16 |
| P1430 | Open Plaques subject ID | 554 | 0.25 | 2 | wrong_page, ok | 8.8 | False | False | False | none | 2 | 8 | 31 | 4 |  |  | opengraph, rdfa | page text only (page served to plain HTTP) | 9 | 18 | 1 | 0.47 | 2 | 0 | 0 |
| P1564 | At the Circulating Library ID | 825 | 0.14 | 1 | ok | 4.7 | False | False | False | none | 0 | 1 | 7 | 0 |  |  |  | page text only (page served to plain HTTP) | 14 | 24 | 1 | 0.25 | 5 | 0 | 10 |
| P1580 | University of Barcelona authority ID (former scheme) | 82 | 2.99 | 1 | ok | 8.8 | False | False | False | none | 0 | 4 | 11 | 1 | json |  |  | page text only (page served to plain HTTP) | 13 | 25 | 1 | 0.05 | 9 | 0 | 6 |
| P1617 | BBC Things ID | 110 | 2.24 | 1 | http_error | 3.6 | False | False | False | none | 0 | 1 | 32 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P1695 | NLP ID | 81 | 3.06 | 1 | ok | 32.6 | False | False | False | none | 2 | 5 | 597 | 9 | json |  | json-ld, opengraph, rdfa | plain HTTP, partly (js-rendered page) + page text for 75/200 values | 22 | 200 | 3 | 0.07 | 11 | 0 | 65 |
| P1741 | GTAA ID | 173 | 1.32 | 1 | ok | 4.6 | False | False | False | none | 0 | 1 | 22 | 7 | json-ld, rdf-xml, turtle |  | json-ld | plain HTTP + page text for 11/26 values | 12 | 26 | 2 | 0.2 | 4 | 0 | 2 |
| P1816 | National Portrait Gallery (London) person ID | 150 | 1.52 | 1 | ok | 5.1 | False | False | True | ads served | 2 | 6 | 112 | 4 | json |  | opengraph, rdfa | plain HTTP + page text for 17/23 values | 11 | 23 | 1 | 0.7 | 3 | 0 | 0 |
| P1819 | genealogics.org person ID | 206 | 1.1 | 1 | load_failed | 4.0 | False | False | False | none | 0 | 0 | 0 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P1890 | CCAB ID | 568 | 0.24 | 1 | ok | 4.6 | False | False | False | none | 0 | 0 | 25 | 0 |  |  |  | page text only (page served to plain HTTP) | 13 | 26 | 1 | 0.0 | 4 | 0 | 10 |
| P1899 | LibriVox author ID | 439 | 0.37 | 1 | ok | 19.0 | False | False | False | none | 0 | 2 | 17 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 11 | 13 | 1 | 0.0 | 7 | 0 | 0 |
| P1938 | Project Gutenberg author ID | 221 | 1.01 | 1 | ok | 3.6 | False | False | False | none | 0 | 0 | 18 | 3 | feed |  | opengraph, rdfa | plain HTTP + page text for 25/51 values | 6 | 51 | 1 | 0.15 | 2 | 0 | 20 |
| P1953 | Discogs artist ID | 47 | 6.08 | 1 | ok | 7.6 | True | False | True | ads served | 1 | 21 | 781 | 5 | json |  | json-ld, opengraph, rdfa | page blocked for plain HTTP only + page text for 51/58 values | 14 | 58 | 5 | 0.55 | 6 | 0 | 25 |
| P1977 | Les Archives du spectacle person ID | 231 | 0.92 | 1 | ok | 5.1 | False | False | False | none | 0 | 1 | 61 | 6 |  | feed | json-ld, microdata, opengraph, rdfa | plain HTTP + page text for 58/64 values | 11 | 64 | 2 | 0.75 | 6 | 0 | 22 |
| P2089 | Library of Congress JukeBox ID (former scheme) | 1057 | 0.09 | 1 | ok | 10.4 | False | False | False | none | 0 | 4 | 21 | 2 | json |  | rdfa | page text only (page served to plain HTTP) | 4 | 4 | 1 | 0.0 | 1 | 0 | 1 |
| P2163 | FAST ID | 14 | 26.24 | 1 | ok | 4.1 | True | False | False | none | 3 | 4 | 13 | 7 | marc-binary, marcxml, xml |  |  | plain HTTP + page text for 19/51 values | 16 | 51 | 1 | 0.12 | 5 | 0 | 22 |
| P2188 | BiblioNet author ID | 449 | 0.35 | 1 | ok | 21.1 | True | False | True | none | 0 | 0 | 647 | 1 |  |  | rdfa | page text only (page blocked for plain HTTP) | 10 | 58 | 2 | 0.74 | 5 | 0 | 45 |
| P2191 | Vegetti Catalog of Fantastic Literature NILF ID | 545 | 0.26 | 1 | ok | 7.6 | False | False | False | none | 0 | 3 | 38 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 9 | 42 | 1 | 0.82 | 6 | 0 | 33 |
| P2373 | Genius artist ID | 324 | 0.62 | 1 | ok | 9.5 | True | False | False | ads served | 11 | 106 | 1002 | 23 | json |  | json-ld, microdata, opengraph, rdfa | plain HTTP + page text for 9/14 values | 7 | 14 | 1 | 0.18 | 3 | 0 | 6 |
| P2435 | PORT person ID | 90 | 2.76 | 1 | ok | 10.5 | False | True | True | ads served | 5 | 24 | 242 | 8 | json |  | microdata, opengraph, rdfa | plain HTTP + page text for 25/34 values | 11 | 34 | 1 | 0.62 | 6 | 0 | 17 |
| P2469 | Theatricalia person ID | 970 | 0.11 | 1 | ok | 4.6 | False | False | False | none | 0 | 0 | 6 | 3 | feed |  | microdata, rdfa | plain HTTP + page text for 1/3 values | 2 | 3 | 1 | 0.0 | 1 | 0 | 0 |
| P2581 | BabelNet ID | 197 | 1.15 | 1 | ok | 5.2 | False | False | False | none | 2 | 5 | 303 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 20 | 72 | 1 | 0.22 | 11 | 0 | 19 |
| P2600 | Geni profile ID | 48 | 6.02 | 1 | ok | 5.8 | False | True | True | none | 1 | 7 | 193 | 3 | json |  | microdata, opengraph | js-rendered page only + page text for 64/185 values | 25 | 185 | 5 | 0.32 | 12 | 0 | 57 |
| P2605 | ČSFD person ID | 49 | 5.77 | 1 | ok | 14.5 | False | False | True | ads served | 2 | 73 | 366 | 9 | json |  | json-ld, opengraph, rdfa | plain HTTP, partly (js-rendered page) + page text for 53/61 values | 14 | 61 | 1 | 0.32 | 5 | 0 | 41 |
| P2607 | BookBrainz author ID | 353 | 0.54 | 1 | ok | 5.1 | False | False | False | none | 0 | 1 | 510 | 2 | json |  | rdfa | plain HTTP + page text for 62/99 values | 20 | 99 | 1 | 0.19 | 11 | 0 | 47 |
| P2639 | Filmportal ID | 133 | 1.7 | 1 | ok | 5.1 | False | False | False | none | 0 | 0 | 43 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 9 | 16 | 1 | 0.27 | 3 | 1 | 7 |
| P2734 | Unz Review author ID | 186 | 1.24 | 1 | ok | 6.4 | False | False | False | none | 4 | 9 | 245 | 4 | feed |  | opengraph, rdfa | page text only (page blocked for plain HTTP) | 5 | 28 | 1 | 0.67 | 2 | 0 | 16 |
| P2799 | BVMC person ID | 282 | 0.75 | 1 | ok | 12.3 | False | False | False | none | 3 | 9 | 22 | 6 | json-ld, rdf-xml |  | json-ld, microdata, opengraph, rdfa | plain HTTP + page text for 15/27 values | 18 | 27 | 1 | 0.07 | 8 | 0 | 3 |
| P2889 | FamilySearch person ID | 308 | 0.65 | 1 | ok | 5.4 | False | False | True | none | 3 | 16 | 186 | 16 | json |  | json-ld, opengraph, rdfa | plain HTTP, partly (js-rendered page) + page text for 34/65 values | 19 | 65 | 1 | 0.45 | 8 | 0 | 7 |
| P2924 | Great Russian Encyclopedia Online ID (2017) | 160 | 1.45 | 1 | ok | 24.5 | False | False | False | none | 0 | 4 | 55 | 5 | json |  | json-ld, rdfa | page text only (page served to plain HTTP) | 13 | 35 | 2 | 0.18 | 5 | 0 | 16 |
| P2949 | WikiTree person ID | 52 | 5.55 | 1 | ok | 4.4 | False | False | False | none | 2 | 6 | 117 | 3 |  |  | microdata, opengraph, rdfa | page blocked for plain HTTP only + page text for 82/92 values | 22 | 92 | 1 | 0.32 | 10 | 0 | 13 |
| P2963 | Goodreads author ID | 83 | 2.89 | 1 | ok | 4.6 | True | False | False | ads served | 0 | 22 | 175 | 11 | json, xml |  | microdata, opengraph, rdfa | plain HTTP + page text for 43/97 values | 15 | 97 | 1 | 0.44 | 6 | 0 | 19 |
| P2966 | National Library of Wales Authority ID | 334 | 0.58 | 1 | ok | 5.9 | False | False | False | none | 3 | 6 | 43 | 3 | json | xml | rdfa | page text only (page blocked for plain HTTP) | 5 | 5 | 1 | 0.25 | 1 | 0 | 1 |
| P2977 | LBT person ID | 423 | 0.39 | 1 | ok | 4.0 | False | False | False | none | 1 | 2 | 12 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 12 | 15 | 1 | 0.12 | 6 | 0 | 0 |
| P3065 | RERO ID (legacy) | 28 | 10.47 | 2 | wrong_page, http_error | 9.4 | False | False | True | none | 4 | 5 | 434 | 24 | json |  | rdfa | page text only (page served to plain HTTP) | 16 | 99 | 6 | 0.26 | 6 | 0 | 42 |
| P3154 | Runeberg author ID | 309 | 0.65 | 1 | ok | 4.0 | False | False | False | none | 0 | 0 | 9 | 1 | rdf-xml |  |  | page text only (page served to plain HTTP) | 12 | 27 | 4 | 0.4 | 6 | 0 | 9 |
| P3219 | Encyclopædia Universalis ID | 164 | 1.42 | 1 | ok | 5.9 | False | False | True | ads served | 0 | 49 | 394 | 10 | json |  | json-ld, opengraph, rdfa | js-rendered page only + page text for 25/33 values | 17 | 33 | 1 | 0.34 | 6 | 0 | 5 |
| P3222 | NE.se ID | 113 | 2.18 | 2 | ok×2 | 5.8 | False | False | False | none | 0 | 1 | 201 | 8 | json |  | rdfa | page text only (page served to plain HTTP) | 13 | 21 | 2 | 0.11 | 8 | 0 | 4 |
| P3280 | BAnQ authority ID | 170 | 1.39 | 1 | ok | 3.6 | False | False | True | none | 4 | 5 | 368 | 7 | json |  | rdfa | plain HTTP + page text for 77/167 values | 21 | 167 | 6 | 0.44 | 13 | 0 | 38 |
| P3338 | Encyclopedia of Surfing ID | 3679 | 0.01 | 1 | ok | 4.8 | False | False | False | none | 2 | 8 | 265 | 19 | json |  | opengraph, rdfa | plain HTTP + page text for 11/31 values | 15 | 31 | 4 | 0.59 | 5 | 0 | 4 |
| P3348 | National Library of Greece ID | 98 | 2.56 | 2 | wrong_page×2 | 5.6 | False | True | True | none | 2 | 3 | 101 | 2 |  |  | rdfa | page text only (page served to plain HTTP) | 20 | 47 | 2 | 0.39 | 8 | 0 | 11 |
| P3365 | Treccani ID | 99 | 2.56 | 1 | ok | 4.6 | True | False | True | ads served | 3 | 41 | 304 | 10 | json |  | opengraph, rdfa | plain HTTP + page text for 46/49 values | 16 | 49 | 1 | 0.22 | 8 | 0 | 18 |
| P3368 | Prabook ID | 19 | 14.11 | 1 | ok | 5.5 | True | False | True | ads served | 3 | 9 | 90 | 4 | json |  | json-ld, opengraph, rdfa | page blocked for plain HTTP only + page text for 28/41 values | 18 | 41 | 1 | 0.33 | 7 | 0 | 3 |
| P3417 | Quora topic ID | 66 | 3.91 | 1 | ok | 4.8 | True | False | True | ads served | 1 | 10 | 314 | 2 |  |  | opengraph, rdfa | plain HTTP + page text for 5/9 values | 6 | 9 | 1 | 0.17 | 3 | 0 | 2 |
| P3430 | SNAC ARK ID | 35 | 7.58 | 2 | ok×2 | 9.6 | True | False | False | none | 0 | 9 | 702 | 8 | json | eac-cpf, json | rdfa | browser only + page text for 28/1619 values | 18 | 1619 | 1 | 0.64 | 10 | 0 | 31 |
| P3478 | Songkick artist ID | 125 | 1.86 | 1 | ok | 7.9 | True | False | True | ads served | 0 | 106 | 255 | 18 | json, xml |  | json-ld, rdfa | plain HTTP + page text for 2/3 values | 3 | 3 | 1 | 0.5 | 1 | 0 | 0 |
| P3553 | Zhihu topic ID | 441 | 0.36 | 1 | ok | 7.1 | False | False | False | none | 1 | 13 | 269 | 16 | json |  | microdata, rdfa | page blocked for plain HTTP only + page text for 30/57 values | 12 | 57 | 2 | 0.43 | 7 | 0 | 33 |
| P3569 | Cultureel Woordenboek ID | 560 | 0.24 | 1 | wrong_page | 4.7 | False | False | False | none | 0 | 1 | 32 | 2 |  |  | opengraph, rdfa | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P3630 | Babelio author ID | 92 | 2.74 | 1 | ok | 10.2 | False | False | False | ads served | 4 | 71 | 249 | 11 | json |  | microdata, opengraph, rdfa | page blocked for plain HTTP only + page text for 26/41 values | 16 | 41 | 1 | 0.15 | 8 | 0 | 13 |
| P3762 | openMLOL author ID | 78 | 3.12 | 1 | ok | 7.1 | False | False | True | none | 0 | 14 | 239 | 8 | json, xml |  | opengraph, rdfa | page text only (page blocked for plain HTTP) | 5 | 20 | 3 | 0.47 | 2 | 0 | 12 |
| P3788 | BNMM authority ID | 421 | 0.39 | 4 | ok×4 | 9.6 | False | False | False | none | 2 | 2 | 44 | 8 |  |  | opengraph, rdfa | page text only (page served to plain HTTP) | 20 | 52 | 2 | 0.08 | 9 | 0 | 3 |
| P3794 | Dictionary of Sydney ID | 1302 | 0.06 | 1 | ok | 6.6 | False | False | False | none | 4 | 5 | 35 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 12 | 17 | 1 | 0.56 | 6 | 0 | 1 |
| P3846 | DBC author ID | 185 | 1.24 | 2 | ok×2 | 4.1 | False | False | True | none | 4 | 5 | 613 | 14 | json |  | rdfa | plain HTTP + page text for 78/112 values | 17 | 112 | 5 | 0.42 | 6 | 0 | 42 |
| P3847 | Open Library subject ID | 443 | 0.36 | 1 | ok | 5.3 | False | False | False | none | 0 | 5 | 87 | 4 | json |  | rdfa | plain HTTP + page text for 1/15 values | 7 | 15 | 1 | 0.21 | 2 | 0 | 0 |
| P3984 | subreddit | 394 | 0.44 | 1 | ok | 4.6 | True | False | True | ads served | 1 | 17 | 1225 | 2 |  | json | rdfa | page text only (page served to plain HTTP) | 5 | 12 | 1 | 0.0 | 2 | 0 | 7 |
| P3987 | SHARE Catalogue author ID | 26 | 10.81 | 1 | http_error | 4.1 | False | False | False | none | 0 | 0 | 1 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P4081 | BHL creator ID | 168 | 1.39 | 1 | ok | 4.8 | False | False | True | none | 2 | 3 | 23 | 1 |  |  | rdfa | page text only (page blocked for plain HTTP) | 6 | 17 | 1 | 0.0 | 1 | 0 | 1 |
| P4084 | MyAnimeList people ID | 687 | 0.18 | 1 | ok | 6.7 | True | False | True | ads served | 0 | 34 | 323 | 7 | json |  | microdata, opengraph, rdfa | plain HTTP + page text for 19/25 values | 12 | 25 | 2 | 0.21 | 7 | 0 | 7 |
| P4104 | Carnegie Hall Agent ID | 180 | 1.27 | 1 | ok | 4.5 | False | False | False | none | 2 | 7 | 7 | 5 | json-ld, n-triples, rdf-xml, turtle |  |  | plain HTTP + page text for 5/17 values | 9 | 17 | 1 | 0.0 | 4 | 0 | 4 |
| P4159 | WeRelate person ID | 356 | 0.53 | 1 | ok | 11.1 | True | False | False | ads served | 3 | 13 | 57 | 3 | json | rdf-xml | microdata | browser / page blocked for plain HTTP only + page text for 65/81 values | 24 | 81 | 1 | 0.17 | 10 | 0 | 14 |
| P4223 | Treccani's Enciclopedia Italiana ID | 207 | 1.1 | 1 | ok | 4.5 | True | False | True | ads served | 3 | 33 | 304 | 9 | json |  | opengraph, rdfa | plain HTTP + page text for 50/53 values | 17 | 53 | 2 | 0.31 | 8 | 0 | 15 |
| P4342 | Great Norwegian Encyclopedia ID | 87 | 2.83 | 1 | ok | 5.6 | False | False | False | none | 3 | 5 | 43 | 5 |  | json | json-ld, microdata, opengraph, rdfa | plain HTTP + page text for 32/78 values | 23 | 78 | 2 | 0.13 | 7 | 0 | 15 |
| P4343 | WBPLN author ID | 1550 | 0.04 | 3 | load_failed×3 | 48.7 | False | False | False | none | 0 | 0 | 184 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P4359 | gravsted.dk ID | 537 | 0.26 | 1 | ok | 4.1 | False | False | False | none | 0 | 0 | 9 | 0 |  |  |  | page text only (page served to plain HTTP) | 12 | 18 | 2 | 0.29 | 5 | 0 | 3 |
| P4399 | Itaú Cultural ID | 539 | 0.26 | 1 | ok | 6.1 | True | False | False | none | 3 | 10 | 53 | 3 | json |  | opengraph, rdfa | plain HTTP + page text for 11/13 values | 11 | 13 | 1 | 0.5 | 4 | 0 | 0 |
| P4431 | Google Doodle | 984 | 0.1 | 1 | ok | 5.6 | True | False | False | none | 2 | 9 | 489 | 3 |  |  | json-ld, opengraph, rdfa | page text only (page served to plain HTTP) | 8 | 9 | 1 | 0.38 | 2 | 0 | 0 |
| P4432 | Artists of the World ID | 96 | 2.62 | 1 | ok | 5.8 | False | False | False | none | 4 | 6 | 115 | 8 | json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 4/13 values | 11 | 13 | 1 | 0.29 | 4 | 0 | 2 |
| P4457 | DAHR artist ID | 286 | 0.74 | 1 | ok | 4.6 | False | False | False | none | 2 | 5 | 26 | 2 |  |  | opengraph, rdfa | plain HTTP + page text for 57/58 values | 17 | 58 | 1 | 0.21 | 7 | 0 | 13 |
| P4491 | Isidore scholar ID | 481 | 0.32 | 1 | load_failed | 3.6 | False | False | False | none | 0 | 0 | 183 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P4514 | Africultures person ID | 409 | 0.42 | 1 | ok | 11.7 | True | False | False | none | 6 | 23 | 88 | 7 | feed, json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 6/15 values | 9 | 15 | 1 | 0.73 | 2 | 0 | 2 |
| P4619 | National Library of Brazil ID | 154 | 1.48 | 1 | blocked | 3.7 | False | False | False | none | 0 | 0 | 5 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P4629 | Online Books Page author ID | 203 | 1.1 | 1 | ok | 3.6 | False | False | False | none | 0 | 0 | 301 | 0 |  |  |  | page text only (page served to plain HTTP) | 8 | 55 | 1 | 0.13 | 3 | 0 | 39 |
| P4657 | The Numbers person ID (archived) | 507 | 0.29 | 1 | wrong_page | 4.1 | False | False | False | none | 0 | 4 | 196 | 4 | json |  | rdfa | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P4666 | CineMagia person ID | 145 | 1.58 | 1 | ok | 13.4 | True | False | True | ads served | 2 | 42 | 216 | 14 | feed, json |  | json-ld, opengraph | page blocked for plain HTTP only + page text for 30/76 values | 17 | 76 | 2 | 0.36 | 8 | 0 | 39 |
| P4823 | American National Biography ID | 218 | 1.03 | 1 | ok | 6.1 | False | False | True | none | 2 | 10 | 248 | 3 | json |  | opengraph, rdfa | page blocked for plain HTTP only + page text for 11/24 values | 11 | 24 | 1 | 0.18 | 4 | 0 | 4 |
| P4839 | Wolfram Language entity code | 225 | 0.99 | 1 | ok | 4.1 | False | False | False | none | 0 | 1 | 154 | 3 | json |  | opengraph, rdfa | page text only (page served to plain HTTP) | 1 | 1 | 0 |  | 0 | 0 | 0 |
| P4985 | TMDB person ID | 39 | 6.69 | 1 | ok | 4.1 | False | False | True | none | 3 | 7 | 355 | 10 | json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 58/80 values | 16 | 80 | 2 | 0.38 | 8 | 0 | 49 |
| P5019 | Brockhaus Enzyklopädie online ID | 122 | 1.96 | 2 | wrong_page, ok | 4.6 | False | False | False | none | 1 | 7 | 228 | 10 | json |  | rdfa | page text only (page served to plain HTTP) | 12 | 14 | 1 | 0.08 | 7 | 0 | 2 |
| P5034 | National Library of Korea ID | 57 | 4.81 | 1 | ok | 6.1 | False | False | False | none | 0 | 1 | 59 | 7 | json, n-triples, rdf-xml, turtle |  |  | plain HTTP + page text for 4/77 values | 16 | 77 | 4 | 0.29 | 5 | 0 | 11 |
| P5063 | Interlingual Index ID | 360 | 0.52 | 1 | ok | 3.6 | False | False | False | none | 0 | 0 | 1 | 1 |  |  | microdata | plain HTTP + page text for 1/10 values | 8 | 10 | 1 | 0.0 | 2 | 0 | 0 |
| P5068 | Flanders Arts Institute person ID (former scheme) | 563 | 0.24 | 1 | ok | 8.8 | False | False | False | none | 0 | 4 | 15 | 1 | json |  |  | page text only (page served to plain HTTP) | 9 | 13 | 2 | 0.3 | 5 | 0 | 5 |
| P5341 | Poetry Foundation ID | 703 | 0.18 | 1 | ok | 5.6 | False | False | False | ads served | 4 | 10 | 462 | 4 | json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 74/77 values | 19 | 77 | 1 | 0.23 | 8 | 0 | 23 |
| P5343 | Poets.org poet ID | 942 | 0.11 | 1 | ok | 5.4 | True | False | False | ads served | 9 | 17 | 95 | 6 | json |  | json-ld, microdata, opengraph, rdfa | plain HTTP + page text for 11/29 values | 15 | 29 | 1 | 0.3 | 7 | 0 | 8 |
| P5357 | Encyclopedia of Science Fiction ID | 377 | 0.48 | 1 | ok | 4.6 | False | False | True | none | 2 | 5 | 63 | 0 |  |  |  | page text only (page served to plain HTTP) | 20 | 72 | 1 | 0.15 | 10 | 0 | 40 |
| P5361 | BNB person ID (OBSOLETE) | 106 | 2.4 | 1 | load_failed | 7.6 | False | False | False | none | 0 | 0 | 181 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P5408 | Fantastic Fiction author ID | 619 | 0.21 | 1 | ok | 7.4 | True | False | True | ads served | 3 | 62 | 110 | 3 | json |  | microdata | page blocked for plain HTTP only + page text for 87/89 values | 14 | 89 | 1 | 0.24 | 7 | 0 | 41 |
| P5421 | Trading Card Database name ID | 283 | 0.75 | 1 | ok | 11.4 | True | False | True | ads served | 3 | 61 | 1744 | 20 | json |  | opengraph, rdfa | plain HTTP + page text for 6/7 values | 6 | 7 | 1 | 0.0 | 4 | 0 | 0 |
| P5469 | Latter-day Saint Literature database artist ID (archived) | 1731 | 0.04 | 1 | ok | 6.1 | False | False | True | none | 0 | 4 | 17 | 3 | json |  | rdfa | page text only (page served to plain HTTP) | 12 | 19 | 1 | 0.19 | 4 | 0 | 3 |
| P5478 | RPO poet ID | 1621 | 0.04 | 1 | ok | 4.1 | False | False | False | none | 2 | 3 | 25 | 2 |  |  | opengraph, rdfa | page text only (page served to plain HTTP) | 17 | 29 | 1 | 0.23 | 8 | 0 | 7 |
| P5491 | BD Gest' author ID | 363 | 0.51 | 1 | ok | 4.6 | False | True | False | none | 1 | 3 | 133 | 3 | feed |  | opengraph, rdfa | plain HTTP + page text for 42/45 values | 13 | 45 | 1 | 0.53 | 5 | 0 | 32 |
| P5562 | Tebeosfera ID | 909 | 0.12 | 1 | ok | 5.4 | False | True | False | ads served | 4 | 10 | 241 | 1 |  |  | opengraph | plain HTTP + page text for 53/56 values | 14 | 56 | 1 | 0.61 | 6 | 0 | 40 |
| P5570 | NooSFere author ID | 392 | 0.44 | 1 | ok | 4.6 | False | False | False | none | 2 | 2 | 23 | 0 |  |  |  | page text only (page served to plain HTTP) | 10 | 22 | 2 | 0.4 | 5 | 0 | 13 |
| P5587 | Libris-URI | 68 | 3.86 | 1 | ok | 4.1 | False | False | False | none | 0 | 1 | 386 | 8 | json-ld, marcxml, turtle |  | opengraph, rdfa | plain HTTP + page text for 41/68 values | 18 | 68 | 7 | 0.21 | 6 | 0 | 14 |
| P5613 | Bibliothèque de la Pléiade ID | 1699 | 0.04 | 1 | ok | 5.1 | False | False | False | none | 1 | 2 | 80 | 3 |  |  | json-ld, opengraph, rdfa | plain HTTP + page text for 2/5 values | 5 | 5 | 1 | 0.0 | 2 | 0 | 1 |
| P5617 | Evene ID | 291 | 0.71 | 1 | ok | 4.6 | False | False | False | ads served | 1 | 16 | 253 | 3 |  |  | json-ld, opengraph, rdfa | plain HTTP + page text for 24/34 values | 16 | 34 | 1 | 0.26 | 9 | 0 | 7 |
| P5618 | LOA ID | 3304 | 0.01 | 1 | ok | 4.6 | False | False | False | ads served | 4 | 8 | 63 | 8 | feed, json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 19/31 values | 11 | 31 | 1 | 0.38 | 1 | 0 | 12 |
| P5705 | Los Angeles Review of Books author ID | 1173 | 0.07 | 1 | http_error | 4.9 | True | False | False | ads served | 7 | 12 | 52 | 3 | json |  | rdfa | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P5714 | Tor.com author ID | 1317 | 0.06 | 1 | ok | 4.6 | False | False | True | ad slots in markup, nothing loaded | 0 | 9 | 369 | 11 | feed, json |  | json-ld, rdfa | plain HTTP | 5 | 5 | 1 | 0.0 | 1 | 0 | 1 |
| P5731 | Angelicum ID | 103 | 2.47 | 1 | ok | 4.1 | False | True | True | none | 0 | 0 | 124 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 16 | 114 | 15 | 0.14 | 6 | 0 | 46 |
| P5739 | Pontificia Università della Santa Croce ID | 72 | 3.55 | 1 | ok | 4.2 | False | True | False | none | 0 | 1 | 60 | 4 | json |  | rdfa | plain HTTP + page text for 5/37 values | 20 | 37 | 3 | 0.1 | 10 | 0 | 4 |
| P5859 | Adelphi author ID | 1403 | 0.05 | 1 | ok | 6.3 | False | False | False | none | 0 | 4 | 29 | 4 | json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 4/6 values | 5 | 6 | 1 | 0.6 | 1 | 0 | 1 |
| P5882 | Muziekweb performer ID | 73 | 3.52 | 1 | load_failed | 48.7 | False | False | False | none | 0 | 0 | 0 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P5905 | Comic Vine ID | 361 | 0.52 | 2 | ok×2 | 7.6 | True | False | True | ads served | 4 | 80 | 391 | 36 | json |  | microdata, opengraph, rdfa | plain HTTP, partly (page blocked for plain HTTP) + page text for 30/43 values | 17 | 43 | 1 | 0.11 | 9 | 0 | 9 |
| P6058 | Larousse ID | 422 | 0.39 | 3 | ok×3 | 5.7 | False | False | True | none | 1 | 9 | 200 | 39 | json |  | microdata, opengraph, rdfa | plain HTTP + page text for 60/75 values | 17 | 75 | 2 | 0.26 | 7 | 0 | 31 |
| P6173 | Bitraga author ID | 1256 | 0.06 | 1 | ok | 4.6 | False | False | False | none | 0 | 1 | 45 | 0 |  |  |  | page text only (page served to plain HTTP) | 8 | 16 | 2 | 0.27 | 3 | 0 | 8 |
| P6262 | Fandom article ID | 262 | 0.82 | 2 | ok×2 | 15.8 | True | False | True | ads served | 5 | 90 | 828 | 38 | json |  | json-ld, microdata, opengraph, rdfa | page blocked for plain HTTP only + page text for 38/60 values | 20 | 60 | 1 | 0.2 | 8 | 0 | 20 |
| P6298 | bgm.tv person ID | 598 | 0.22 | 1 | ok | 4.1 | False | False | False | none | 2 | 3 | 49 | 2 | json |  | rdfa | page text only (page served to plain HTTP) | 12 | 24 | 3 | 0.24 | 7 | 0 | 5 |
| P6385 | Krugosvet article (archived) | 328 | 0.6 | 1 | ok | 6.2 | False | False | False | none | 0 | 4 | 61 | 4 | json |  | opengraph, rdfa | page text only (page served to plain HTTP) | 18 | 60 | 2 | 0.08 | 9 | 0 | 20 |
| P6394 | ELNET ID | 217 | 1.03 | 2 | ok, http_error | 3.6 | False | False | True | none | 4 | 5 | 301 | 13 | json |  | rdfa | plain HTTP + page text for 75/128 values | 14 | 128 | 5 | 0.55 | 5 | 0 | 10 |
| P6441 | Douban author ID | 1551 | 0.04 | 1 | ok | 9.1 | False | False | False | none | 0 | 4 | 52 | 5 | json |  | opengraph | plain HTTP + page text for 29/57 values | 18 | 57 | 2 | 0.24 | 8 | 0 | 23 |
| P6573 | Klexikon article ID | 870 | 0.13 | 1 | ok | 5.2 | False | False | True | none | 0 | 2 | 299 | 3 | feed |  | opengraph, rdfa | plain HTTP + page text for 15/26 values | 11 | 26 | 2 | 0.22 | 4 | 0 | 3 |
| P6645 | Stedelijk Museum Amsterdam ID | 707 | 0.17 | 1 | ok | 5.6 | False | False | True | ads served | 2 | 9 | 100 | 5 | json |  | opengraph, rdfa | plain HTTP + page text for 6/9 values | 6 | 9 | 3 | 0.5 | 1 | 0 | 2 |
| P6683 | Alexander Turnbull Library ID | 339 | 0.57 | 1 | ok | 7.6 | True | False | False | none | 1 | 1 | 155 | 0 |  |  |  | page text only (page served to plain HTTP) | 10 | 16 | 1 | 0.47 | 4 | 0 | 0 |
| P6698 | Japan Search name ID | 277 | 0.76 | 1 | ok | 5.7 | False | False | False | none | 0 | 2 | 21 | 33 | json, json-ld, rdf-xml, turtle |  | microdata, rdfa | plain HTTP, partly (js-rendered page) | 12 | 36 | 2 | 0.23 | 4 | 0 | 3 |
| P6706 | De Agostini ID | 155 | 1.47 | 1 | ok | 8.0 | True | False | True | ads served | 5 | 69 | 305 | 13 | json |  | json-ld, microdata, opengraph, rdfa | plain HTTP + page text for 29/63 values | 21 | 63 | 2 | 0.28 | 7 | 0 | 11 |
| P6821 | Alvin ID | 208 | 1.09 | 1 | ok | 6.2 | False | True | False | none | 0 | 0 | 91 | 1 |  |  | rdfa | page text only (page blocked for plain HTTP) | 6 | 7 | 1 | 0.17 | 2 | 0 | 2 |
| P6844 | abART person ID | 117 | 2.05 | 1 | ok | 8.3 | False | False | False | none | 0 | 0 | 45 | 1 | json |  |  | page text only (page served to plain HTTP) | 15 | 19 | 1 | 0.12 | 7 | 0 | 2 |
| P6868 | Hoopla artist ID | 400 | 0.43 | 1 | wrong_page | 7.8 | False | False | True | none | 0 | 9 | 1206 | 10 | json |  | json-ld, opengraph, rdfa | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P6984 | Rupa Publications author ID | 2954 | 0.01 | 1 | http_error | 4.1 | False | False | False | none | 0 | 0 | 6 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P7024 | Flemish Public Libraries ID | 677 | 0.19 | 1 | ok | 3.6 | False | False | True | none | 4 | 5 | 648 | 7 | json |  | rdfa | plain HTTP + page text for 128/217 values | 8 | 217 | 6 | 0.72 | 2 | 0 | 40 |
| P7026 | Lebanese National Library ID | 779 | 0.15 | 1 | ok | 3.6 | False | False | True | none | 4 | 5 | 265 | 7 | json |  | rdfa | plain HTTP + page text for 54/127 values | 17 | 127 | 2 | 0.41 | 7 | 1 | 3 |
| P7029 | National Library of Russia ID | 281 | 0.75 | 2 | load_failed×2 | 49.1 | False | False | False | none | 0 | 0 | 184 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P7039 | National Library of Iceland ID | 1052 | 0.09 | 1 | http_error | 1821.6 | True | False | True | none | 4 | 5 | 216 | 6 | json |  | rdfa | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P7293 | National Library of Poland MMS ID | 18 | 17.13 | 1 | ok | 6.7 | False | False | False | none | 2 | 4 | 571 | 7 | json |  | opengraph, rdfa | plain HTTP + page text for 41/143 values | 19 | 143 | 4 | 0.05 | 7 | 0 | 55 |
| P7305 | Online PWN Encyclopedia ID | 108 | 2.35 | 1 | ok | 13.4 | True | False | False | none | 0 | 4 | 140 | 9 | json |  | opengraph, rdfa | page text only (page served to plain HTTP) | 14 | 29 | 2 | 0.27 | 5 | 0 | 10 |
| P7311 | Aozora Bunko author ID | 1111 | 0.08 | 1 | ok | 5.2 | False | False | False | none | 0 | 0 | 19 | 0 |  |  |  | page text only (page served to plain HTTP) | 7 | 11 | 1 | 0.22 | 4 | 0 | 2 |
| P7369 | National Library of Chile ID | 195 | 1.16 | 1 | wrong_page | 4.6 | False | False | False | none | 0 | 0 | 3 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P7400 | LibraryThing author ID | 192 | 1.18 | 1 | login_wall_suspected | 5.1 | True | True | False | none | 2 | 7 | 58 | 3 |  | xml | opengraph, rdfa | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P7433 | FantLab author ID | 1024 | 0.1 | 1 | ok | 7.2 | True | True | False | none | 2 | 5 | 845 | 5 | json |  | microdata, opengraph, rdfa | plain HTTP + page text for 87/98 values | 21 | 98 | 3 | 0.52 | 11 | 0 | 44 |
| P7502 | Golden ID (archived) | 387 | 0.46 | 1 | ok | 25.4 | False | False | False | none | 0 | 4 | 1017 | 7 | json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 45/52 values | 17 | 52 | 1 | 0.02 | 9 | 0 | 11 |
| P7504 | Jeugdliteratuur ID | 1157 | 0.08 | 1 | ok | 11.8 | False | False | True | none | 0 | 4 | 17 | 2 | json |  |  | page text only (page served to plain HTTP) | 7 | 7 | 1 | 0.0 | 3 | 0 | 0 |
| P7507 | Ben Yehuda author ID | 983 | 0.1 | 1 | ok | 4.6 | False | False | False | none | 3 | 7 | 127 | 2 |  |  | opengraph, rdfa | page text only (page served to plain HTTP) | 13 | 23 | 1 | 0.56 | 3 | 0 | 7 |
| P7509 | Estonian biographical database ID | 1484 | 0.05 | 1 | ok | 4.6 | False | False | False | none | 2 | 2 | 7 | 0 |  |  |  | page text only (page served to plain HTTP) | 8 | 10 | 1 | 0.29 | 3 | 0 | 2 |
| P7520 | Filmový přehled person or company ID | 749 | 0.16 | 1 | ok | 6.4 | False | False | True | none | 0 | 0 | 57 | 2 |  |  | opengraph, rdfa | plain HTTP + page text for 7/10 values | 8 | 10 | 2 | 0.0 | 4 | 0 | 1 |
| P7553 | Sinemalar person ID | 136 | 1.67 | 1 | ok | 9.1 | True | True | True | ads served | 5 | 79 | 369 | 13 | json |  | json-ld, microdata, opengraph, rdfa | plain HTTP + page text for 16/36 values | 12 | 36 | 1 | 0.38 | 7 | 0 | 19 |
| P7574 | Swedish Royal Theater Archive | 1279 | 0.06 | 1 | wrong_page | 5.6 | False | False | True | none | 1 | 7 | 140 | 3 | json |  | opengraph, rdfa | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P7689 | Online Nevada Encyclopedia ID | 3216 | 0.01 | 2 | ok×2 | 4.9 | False | False | False | none | 2 | 7 | 73 | 8 | feed, json |  | rdfa | page blocked for plain HTTP only + page text for 61/75 values | 18 | 75 | 1 | 0.43 | 6 | 0 | 20 |
| P7699 | National Library of Lithuania ID | 65 | 4.0 | 1 | ok | 3.6 | False | False | True | none | 4 | 5 | 281 | 7 | json |  | rdfa | plain HTTP + page text for 27/131 values | 20 | 131 | 3 | 0.34 | 9 | 0 | 17 |
| P7700 | Slovak National Library (VIAF) ID | 390 | 0.45 | 2 | ok×2 | 3.6 | False | False | True | none | 4 | 5 | 864 | 14 | json |  | rdfa | plain HTTP + page text for 323/472 values | 24 | 472 | 12 | 0.51 | 10 | 0 | 57 |
| P7704 | Europeana entity | 51 | 5.55 | 1 | ok | 135.3 | False | False | False | none | 0 | 5 | 308 | 11 | json, json-ld, rdf-xml |  | opengraph, rdfa | plain HTTP + page text for 36/139 values | 12 | 139 | 28 | 0.22 | 6 | 0 | 27 |
| P7753 | Projekt Gutenberg-DE author ID | 978 | 0.1 | 1 | ok | 5.2 | False | False | False | none | 2 | 4 | 105 | 8 | feed, json |  | json-ld, microdata, opengraph, rdfa | plain HTTP + page text for 42/96 values | 14 | 96 | 2 | 0.61 | 7 | 0 | 40 |
| P7769 | Australian National Maritime Museum person ID | 1835 | 0.03 | 1 | ok | 8.3 | False | False | False | ads served | 4 | 15 | 36 | 3 |  |  | microdata, opengraph, rdfa | page blocked for plain HTTP only + page text for 4/6 values | 5 | 6 | 1 | 0.0 | 2 | 0 | 0 |
| P7842 | Vienna History Wiki ID | 405 | 0.42 | 1 | ok | 5.7 | False | False | False | none | 1 | 1 | 68 | 5 | feed, rdf-xml |  | json-ld, opengraph, rdfa | plain HTTP + page text for 38/66 values | 20 | 66 | 2 | 0.46 | 5 | 1 | 8 |
| P7847 | DigitaltMuseum ID | 274 | 0.77 | 1 | ok | 6.2 | True | False | False | none | 4 | 10 | 223 | 6 | json |  | opengraph, rdfa | plain HTTP + page text for 20/25 values | 18 | 25 | 2 | 0.0 | 6 | 0 | 2 |
| P7865 | CoBiS author ID | 214 | 1.04 | 1 | ok | 6.4 | False | False | True | none | 2 | 9 | 104 | 15 | json, rdf-xml, xml |  | opengraph, rdfa | plain HTTP + page text for 24/56 values | 15 | 56 | 2 | 0.17 | 7 | 0 | 6 |
| P7886 | Media Arts Database ID | 680 | 0.19 | 1 | ok | 5.7 | False | False | False | none | 2 | 3 | 34 | 2 | json |  |  | page text only (page served to plain HTTP) | 10 | 12 | 2 | 0.67 | 1 | 1 | 5 |
| P7902 | Deutsche Biographie (GND) ID | 17 | 17.61 | 1 | ok | 5.7 | False | False | False | none | 0 | 0 | 31 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 5 | 5 | 1 | 0.0 | 2 | 0 | 0 |
| P7929 | Roglo person ID | 240 | 0.88 | 1 | ok | 12.3 | False | False | False | none | 0 | 1 | 21 | 0 |  |  |  | page text only (page served to plain HTTP) | 18 | 56 | 2 | 0.46 | 8 | 0 | 12 |
| P7982 | Hrvatska enciklopedija ID | 179 | 1.29 | 1 | ok | 5.7 | True | False | True | none | 2 | 4 | 31 | 2 |  |  | opengraph, rdfa | page text only (page served to plain HTTP) | 14 | 31 | 2 | 0.18 | 7 | 0 | 14 |
| P8034 | Vatican Library VcBA ID | 40 | 6.41 | 1 | ok | 6.2 | False | False | False | none | 2 | 2 | 15 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 7 | 13 | 2 | 0.0 | 3 | 0 | 2 |
| P8094 | GeneaStar person ID | 347 | 0.55 | 1 | ok | 11.7 | False | True | False | none | 1 | 3 | 107 | 3 |  | json | opengraph, rdfa | page blocked for plain HTTP only + page text for 30/45 values | 13 | 45 | 1 | 0.51 | 6 | 0 | 0 |
| P8168 | FactGrid item ID | 56 | 4.84 | 1 | ok | 47.1 | False | False | False | none | 0 | 1 | 258 | 2 |  |  | opengraph, rdfa | js-rendered page only + page text for 79/92 values | 20 | 92 | 1 | 0.2 | 12 | 0 | 2 |
| P8179 | Canadiana Name Authority ID | 32 | 8.33 | 1 | ok | 3.6 | False | False | True | none | 4 | 5 | 217 | 7 | json |  | rdfa | plain HTTP | 14 | 99 | 4 | 0.33 | 4 | 0 | 40 |
| P8189 | J9U entity ID | 8 | 43.2 | 2 | ok×2 | 19.4 | False | False | True | ads served | 9 | 29 | 574 | 10 | json |  | json-ld, opengraph, rdfa | page blocked for plain HTTP only + page text for 99/107 values | 20 | 107 | 6 | 0.13 | 9 | 0 | 44 |
| P8234 | LiederNet author ID | 437 | 0.37 | 1 | ok | 4.1 | False | False | True | none | 2 | 2 | 30 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 8 | 21 | 1 | 0.3 | 2 | 0 | 14 |
| P8313 | Lex ID | 111 | 2.22 | 1 | ok | 7.7 | False | False | True | none | 1 | 5 | 471 | 5 | json |  | json-ld, microdata, rdfa | plain HTTP + page text for 51/58 values | 18 | 58 | 2 | 0.22 | 6 | 0 | 26 |
| P8385 | IDU person ID | 343 | 0.56 | 1 | challenge_suspected | 7.7 | False | False | False | none | 2 | 2 | 123 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P8445 | Our Campaigns candidate ID | 158 | 1.47 | 1 | wrong_page | 3.6 | False | False | False | none | 0 | 0 | 2 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P8496 | Archive Site Trinity College Cambridge ID | 417 | 0.4 | 1 | ok | 5.2 | False | False | False | none | 2 | 3 | 18 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 8 | 12 | 1 | 0.55 | 2 | 0 | 2 |
| P8591 | Grove Music Online ID | 182 | 1.26 | 1 | ok | 16.4 | False | False | True | none | 2 | 10 | 214 | 3 | json |  | opengraph, rdfa | page blocked for plain HTTP only + page text for 5/13 values | 8 | 13 | 1 | 0.5 | 2 | 0 | 1 |
| P8795 | Diamond Catalog ID for persons and organisations | 227 | 0.96 | 1 | ok | 11.2 | False | True | False | none | 2 | 3 | 130 | 2 |  |  | opengraph, rdfa | plain HTTP | 4 | 4 | 0 | 0.0 | 1 | 0 | 0 |
| P8814 | WordNet 3.1 Synset ID | 247 | 0.87 | 1 | ok | 4.1 | False | False | False | none | 0 | 1 | 31 | 4 | json, rdf-xml, turtle, xml |  |  | plain HTTP + page text for 1/18 values | 10 | 18 | 1 | 0.0 | 4 | 0 | 0 |
| P8833 | Union Catalog of Armenian Libraries authority ID | 776 | 0.15 | 3 | http_error×2, ok | 13.7 | False | True | True | none | 3 | 5 | 52 | 3 |  |  | rdfa | page text only (page blocked for plain HTTP) | 14 | 37 | 4 | 0.4 | 7 | 1 | 13 |
| P8849 | CONOR.BG ID | 204 | 1.1 | 1 | ok | 6.2 | False | False | False | none | 0 | 0 | 32 | 2 |  |  | opengraph, rdfa | page text only (page served to plain HTTP) | 9 | 13 | 2 | 0.17 | 4 | 0 | 0 |
| P8851 | CONOR.SR ID | 157 | 1.47 | 1 | ok | 6.2 | False | False | False | none | 0 | 0 | 33 | 2 |  |  | opengraph, rdfa | page text only (page served to plain HTTP) | 13 | 28 | 4 | 0.54 | 6 | 0 | 8 |
| P8902 | Archives at Yale agent ID | 235 | 0.91 | 2 | wrong_page, ok | 4.7 | False | False | False | none | 4 | 7 | 54 | 6 | json |  | json-ld, rdfa | page blocked for plain HTTP only + page text for 36/63 values | 12 | 63 | 5 | 0.25 | 6 | 0 | 17 |
| P8969 | CINE21 person ID | 213 | 1.05 | 1 | ok | 13.4 | False | False | False | ads served | 3 | 18 | 41 | 3 |  |  | json-ld, opengraph, rdfa | page text only (page served to plain HTTP) | 7 | 8 | 2 | 0.14 | 4 | 0 | 1 |
| P8980 | KANTO ID | 190 | 1.21 | 1 | ok | 6.7 | False | False | False | none | 0 | 2 | 48 | 15 | json-ld, rdf-xml, turtle | json | json-ld, opengraph, rdfa | plain HTTP + page text for 18/70 values | 18 | 70 | 2 | 0.65 | 9 | 0 | 6 |
| P9001 | Literary Encyclopedia ID | 1267 | 0.06 | 1 | ok | 49.0 | False | False | False | none | 0 | 0 | 1 | 0 |  |  |  | page text only (page served to plain HTTP) | 11 | 33 | 2 | 0.23 | 3 | 0 | 18 |
| P9037 | BHCL UUID | 121 | 1.97 | 2 | ok×2 | 9.5 | False | False | True | none | 1 | 5 | 210 | 23 | json |  | rdfa | plain HTTP + page text for 7/74 values | 18 | 74 | 1 | 0.33 | 5 | 0 | 7 |
| P9081 | SEARCH on line catalogue ID | 266 | 0.8 | 2 | ok×2 | 6.7 | False | True | True | none | 0 | 0 | 48 | 2 |  |  | rdfa | page text only (page served to plain HTTP) | 9 | 19 | 0 | 0.0 | 3 | 0 | 1 |
| P9097 | American Academy in Rome ID | 107 | 2.37 | 2 | ok×2 | 5.7 | False | True | True | none | 2 | 5 | 90 | 2 |  |  | rdfa | page text only (page blocked for plain HTTP) | 15 | 34 | 1 | 0.0 | 5 | 0 | 3 |
| P9141 | Portal da Literatura ID | 1451 | 0.05 | 1 | ok | 17.2 | True | True | False | none | 5 | 14 | 71 | 4 | json |  | opengraph, rdfa | plain HTTP + page text for 19/30 values | 13 | 30 | 1 | 0.46 | 5 | 0 | 11 |
| P9171 | RILM ID | 210 | 1.08 | 1 | ok | 4.2 | False | False | True | none | 4 | 5 | 218 | 7 | json |  | rdfa | plain HTTP | 11 | 58 | 1 | 0.0 | 5 | 0 | 1 |
| P9178 | Biblioteca Franco Serantini ID | 590 | 0.23 | 1 | ok | 21.9 | False | True | False | none | 1 | 2 | 29 | 1 |  |  | rdfa | page text only (page blocked for plain HTTP) | 9 | 9 | 1 | 0.12 | 5 | 0 | 0 |
| P9196 | BookBub author ID | 2674 | 0.01 | 1 | ok | 6.0 | True | False | True | ads served | 8 | 28 | 228 | 12 | json |  | opengraph, rdfa | browser / page blocked for plain HTTP only + page text for 5/54 values | 13 | 54 | 1 | 0.44 | 6 | 0 | 19 |
| P9223 | Provenio UUID | 438 | 0.37 | 1 | ok | 8.5 | False | False | False | none | 0 | 0 | 162 | 8 | json |  | rdfa | plain HTTP + page text for 4/41 values | 13 | 41 | 1 | 0.0 | 4 | 0 | 4 |
| P9247 | Pontifical University of Salamanca ID | 239 | 0.89 | 1 | ok | 6.7 | False | True | True | none | 0 | 1 | 58 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 9 | 11 | 1 | 0.0 | 3 | 0 | 0 |
| P9251 | Cyprus University of Technology ID | 460 | 0.34 | 1 | ok | 12.7 | False | True | True | none | 2 | 4 | 71 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 7 | 8 | 1 | 0.0 | 1 | 0 | 0 |
| P9307 | Fancyclopedia 3 ID | 1271 | 0.06 | 1 | ok | 4.7 | False | False | False | none | 0 | 1 | 22 | 3 | feed |  | opengraph, rdfa | page text only (page served to plain HTTP) | 15 | 25 | 1 | 0.3 | 8 | 0 | 8 |
| P9322 | SVKKL authority ID | 62 | 4.37 | 2 | ok, load_failed | 8.1 | False | False | False | none | 0 | 1 | 181 | 4 |  |  | json-ld, microdata, opengraph, rdfa | page blocked for plain HTTP only + page text for 13/23 values | 14 | 23 | 1 | 0.15 | 5 | 0 | 2 |
| P9337 | Keratsini-Drapetsona libraries' catalogue authority ID | 2006 | 0.03 | 1 | load_failed | 3.6 | False | False | False | none | 0 | 0 | 184 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P9352 | Portrait Archive ID | 848 | 0.13 | 1 | ok | 5.1 | False | False | False | none | 0 | 1 | 42 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 14 | 14 | 1 | 0.3 | 6 | 0 | 0 |
| P9459 | Rekhta author ID | 1574 | 0.04 | 1 | ok | 9.6 | False | False | False | ads served | 8 | 24 | 508 | 9 | json, xml |  | microdata, opengraph, rdfa | plain HTTP + page text for 6/10 values | 5 | 10 | 2 | 0.86 | 1 | 0 | 5 |
| P9495 | National Historical Museums of Sweden ID | 317 | 0.64 | 1 | ok | 4.6 | False | False | True | none | 3 | 5 | 102 | 2 |  |  | opengraph, rdfa | plain HTTP + page text for 6/11 values | 8 | 11 | 1 | 0.0 | 0 | 0 | 2 |
| P9522 | Biblioteca di Santa Sabina ID | 769 | 0.16 | 1 | wrong_page | 5.4 | False | True | True | none | 0 | 0 | 66 | 1 |  |  | rdfa | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P9545 | Encyclopedia of China (Second Edition) ID | 674 | 0.19 | 1 | blocked | 7.3 | False | False | False | none | 0 | 0 | 6 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P9556 | LTit person ID | 1427 | 0.05 | 1 | ok | 4.6 | False | False | False | none | 0 | 3 | 95 | 6 | json, json-ld |  | json-ld | js-rendered page only + page text for 29/37 values | 13 | 37 | 1 | 0.61 | 5 | 0 | 12 |
| P9629 | Armeniapedia ID | 1027 | 0.09 | 1 | ok | 11.7 | False | False | False | none | 0 | 2 | 23 | 3 | json, rdf-xml |  | rdfa | plain HTTP + page text for 4/7 values | 6 | 7 | 1 | 0.5 | 1 | 0 | 1 |
| P9707 | GCD creator ID | 336 | 0.57 | 1 | ok | 11.2 | False | False | False | none | 1 | 2 | 66 | 1 |  |  | rdfa | page text only (page blocked for plain HTTP) | 13 | 23 | 2 | 0.22 | 6 | 0 | 0 |
| P9802 | Penguin Random House author ID | 467 | 0.33 | 1 | ok | 11.1 | False | False | False | ads served | 10 | 41 | 272 | 10 | json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 20/48 values | 16 | 48 | 1 | 0.19 | 5 | 0 | 9 |
| P9807 | SNK ID | 340 | 0.57 | 4 | ok×4 | 7.2 | False | False | False | none | 0 | 5 | 67 | 21 |  | json | rdfa | browser only + page text for 55/91 values | 18 | 91 | 3 | 0.21 | 8 | 0 | 21 |
| P9918 | Kallías ID | 67 | 3.86 | 1 | ok | 22.7 | False | False | False | none | 0 | 1 | 253 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 8 | 11 | 2 | 0.2 | 2 | 0 | 1 |
| P9964 | Kalliope-Verbund (GND) ID | 33 | 7.86 | 1 | ok | 5.2 | False | False | False | none | 0 | 1 | 15 | 2 | eac-cpf |  | rdfa | plain HTTP + page text for 60/122 values | 15 | 122 | 6 | 0.11 | 6 | 0 | 52 |
| P9984 | CANTIC ID | 36 | 7.33 | 1 | ok | 5.7 | False | False | False | none | 2 | 2 | 21 | 6 | json |  | rdfa | plain HTTP + page text for 2/32 values | 11 | 32 | 1 | 0.0 | 3 | 0 | 7 |
| P9995 | MYmovies person ID | 153 | 1.5 | 1 | ok | 7.5 | False | False | True | ads served | 3 | 36 | 469 | 9 | json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 18/23 values | 8 | 23 | 1 | 0.43 | 5 | 0 | 14 |
| P10018 | George Eastman Museum people ID | 370 | 0.49 | 1 | ok | 6.9 | False | False | False | none | 3 | 7 | 38 | 1 |  |  | rdfa | page blocked for plain HTTP only + page text for 3/8 values | 6 | 8 | 1 | 0.0 | 2 | 0 | 0 |
| P10021 | UAE University Libraries ID | 1501 | 0.05 | 1 | ok | 4.1 | False | False | True | none | 4 | 5 | 217 | 7 | json |  | rdfa | plain HTTP | 18 | 110 | 2 | 0.12 | 8 | 0 | 21 |
| P10069 | Tabakalera ID | 209 | 1.09 | 1 | ok | 5.7 | True | True | True | none | 3 | 5 | 129 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 5 | 5 | 1 | 0.0 | 2 | 0 | 0 |
| P10141 | Academy of Athens authority ID | 295 | 0.71 | 1 | ok | 7.5 | False | True | True | none | 2 | 3 | 42 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 7 | 7 | 0 | 0.0 | 3 | 0 | 0 |
| P10227 | National Library of Ireland ID | 144 | 1.58 | 1 | ok | 3.6 | False | False | True | none | 4 | 5 | 217 | 7 | json |  | rdfa | plain HTTP | 19 | 176 | 1 | 0.38 | 8 | 0 | 55 |
| P10297 | Google Arts & Culture entity ID | 244 | 0.88 | 1 | ok | 5.0 | False | False | False | none | 2 | 13 | 860 | 3 |  |  | json-ld, opengraph, rdfa | plain HTTP + page text for 18/40 values | 15 | 40 | 1 | 0.07 | 7 | 0 | 5 |
| P10298 | Sceneweb artist ID | 500 | 0.3 | 1 | ok | 8.3 | False | False | False | none | 1 | 2 | 11 | 1 |  |  | opengraph | plain HTTP + page text for 7/9 values | 8 | 9 | 1 | 0.2 | 2 | 0 | 1 |
| P10373 | Mnemosine ID | 1368 | 0.06 | 1 | ok | 6.2 | False | False | False | none | 2 | 6 | 8 | 1 | json |  |  | page text only (page served to plain HTTP) | 7 | 7 | 1 | 0.17 | 3 | 0 | 1 |
| P10387 | Databazeknih.cz author ID | 101 | 2.51 | 1 | ok | 8.7 | False | False | True | ads served | 3 | 37 | 144 | 7 | json, xml |  | json-ld, microdata, rdfa | plain HTTP + page text for 21/31 values | 12 | 31 | 2 | 0.24 | 2 | 0 | 12 |
| P10400 | CBDB.cz author ID | 115 | 2.08 | 1 | ok | 8.3 | False | True | True | ads served | 4 | 44 | 175 | 7 | feed, json |  | json-ld, microdata, rdfa | plain HTTP + page text for 64/78 values | 18 | 78 | 1 | 0.56 | 6 | 0 | 42 |
| P10553 | IxTheo authority ID | 34 | 7.81 | 1 | challenge_suspected | 1821.8 | False | False | False | none | 0 | 0 | 2 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P10565 | Encyclopedia of China (Third Edition) old ID (2021) | 175 | 1.32 | 1 | ok | 16.9 | False | False | False | none | 0 | 4 | 97 | 2 | json |  |  | page text only (page served to plain HTTP) | 14 | 16 | 2 | 0.38 | 6 | 1 | 1 |
| P10608 | FID performing arts ID | 89 | 2.8 | 1 | ok | 9.8 | False | False | False | none | 1 | 14 | 31 | 3 | xml | rdf-xml | rdfa | plain HTTP, partly (browser) + page text for 46/99 values | 19 | 99 | 5 | 0.07 | 7 | 0 | 44 |
| P10757 | Personality Database profile ID | 490 | 0.31 | 1 | ok | 12.2 | True | False | True | ads served | 5 | 106 | 189 | 16 | json, json-ld |  | rdfa | plain HTTP + page text for 2/28 values | 15 | 28 | 1 | 0.24 | 7 | 0 | 4 |
| P10780 | Radio France person ID | 259 | 0.82 | 1 | ok | 6.7 | False | False | True | ad slots in markup, nothing loaded | 0 | 7 | 665 | 6 | json |  | opengraph, rdfa | plain HTTP + page text for 14/31 values | 11 | 31 | 2 | 0.54 | 3 | 0 | 11 |
| P10832 | WorldCat Entities ID | 4 | 61.26 | 1 | ok | 5.4 | False | False | True | none | 2 | 4 | 216 | 7 | json, json-ld |  | rdfa | plain HTTP + page text for 16/274 values | 11 | 274 | 157 | 0.02 | 4 | 0 | 4 |
| P10883 | The Encyclopedia of Fantasy ID | 1007 | 0.1 | 1 | ok | 4.1 | False | False | True | none | 2 | 5 | 21 | 0 |  |  |  | page text only (page blocked for plain HTTP) | 12 | 24 | 1 | 0.43 | 4 | 0 | 9 |
| P11137 | Reddit topic ID (obsolete) | 516 | 0.28 | 1 | wrong_page | 5.1 | False | False | False | none | 0 | 4 | 133 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P11155 | Municipal Library of Trikala ID | 1012 | 0.1 | 1 | http_error | 4.1 | False | False | False | none | 1 | 1 | 2 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P11180 | Central Library of Volos authority ID | 577 | 0.23 | 1 | ok | 6.7 | False | False | True | none | 2 | 3 | 33 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 6 | 6 | 0 | 0.0 | 3 | 0 | 0 |
| P11182 | UOM ID | 147 | 1.55 | 1 | ok | 8.7 | False | True | True | none | 2 | 3 | 61 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 11 | 43 | 2 | 0.04 | 3 | 0 | 14 |
| P11192 | Piraeus Bank Group Cultural Foundation Library (A) ID | 1851 | 0.03 | 1 | ok | 6.2 | False | False | True | none | 2 | 6 | 25 | 4 | json |  | rdfa | plain HTTP + page text for 7/21 values | 8 | 21 | 2 | 0.71 | 3 | 0 | 5 |
| P11194 | Famous Birthdays ID | 466 | 0.33 | 1 | ok | 11.5 | True | False | False | ads served | 0 | 111 | 123 | 15 | json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 19/29 values | 17 | 29 | 1 | 0.05 | 10 | 0 | 3 |
| P11227 | AniList staff ID | 548 | 0.26 | 1 | ok | 7.3 | True | False | True | ads served | 3 | 68 | 60 | 6 | json, xml |  | opengraph, rdfa | page text only (page served to plain HTTP) | 11 | 21 | 2 | 0.05 | 7 | 0 | 6 |
| P11249 | KBR person ID | 31 | 8.93 | 1 | ok | 7.5 | False | False | False | none | 0 | 2 | 234 | 4 | json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 4/8 values | 7 | 8 | 2 | 0.0 | 3 | 0 | 0 |
| P11386 | Listal ID | 301 | 0.69 | 1 | ok | 7.7 | False | False | False | none | 6 | 12 | 96 | 2 |  |  | microdata, rdfa | page text only (page served to plain HTTP) | 14 | 24 | 1 | 0.13 | 8 | 0 | 5 |
| P11394 | Internet Sacred Text Archive ID | 4576 | 0.0 | 1 | ok | 8.5 | True | False | False | ads served | 1 | 3 | 391 | 4 | json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 6/10 values | 5 | 10 | 1 | 0.5 | 1 | 0 | 5 |
| P11407 | Ozon person ID | 5100 | 0.0 | 1 | ok | 17.6 | False | False | False | none | 0 | 3 | 628 | 3 |  |  | json-ld, microdata, opengraph | plain HTTP + page text for 8/10 values | 7 | 10 | 2 | 0.56 | 1 | 0 | 4 |
| P11408 | Pixiv Encyclopedia ID | 555 | 0.25 | 1 | ok | 12.9 | False | False | False | none | 4 | 7 | 263 | 3 | json |  | json-ld, opengraph | plain HTTP + page text for 12/17 values | 9 | 17 | 1 | 0.47 | 4 | 0 | 6 |
| P11449 | TV Maze person ID | 374 | 0.49 | 1 | ok | 6.0 | True | False | True | ads served | 0 | 28 | 57 | 5 | json |  | microdata, rdfa | plain HTTP + page text for 3/14 values | 10 | 14 | 2 | 0.11 | 5 | 0 | 2 |
| P11496 | CiNii Research ID | 24 | 12.03 | 1 | ok | 7.2 | False | False | False | none | 0 | 5 | 108 | 16 | json, rdf-xml | json-ld | json-ld, opengraph, rdfa | plain HTTP, partly (page blocked for plain HTTP) + page text for 16/53 values | 19 | 53 | 2 | 0.5 | 6 | 0 | 10 |
| P11686 | University of Barcelona authority ID | 59 | 4.71 | 1 | ok | 6.7 | False | False | False | none | 0 | 0 | 7 | 0 |  |  |  | page text only (page served to plain HTTP) | 9 | 31 | 1 | 0.0 | 3 | 0 | 12 |
| P11870 | The Literary Encyclopedia person ID | 482 | 0.32 | 1 | ok | 6.2 | False | False | False | none | 0 | 3 | 25 | 2 |  |  | opengraph, rdfa | plain HTTP + page text for 22/25 values | 12 | 25 | 1 | 0.32 | 4 | 0 | 4 |
| P12040 | J. Paul Getty Museum agent ID | 740 | 0.17 | 1 | ok | 8.7 | False | False | False | ads served | 5 | 23 | 83 | 21 | json, json-ld |  | json-ld, rdfa | plain HTTP + page text for 14/61 values | 21 | 61 | 1 | 0.17 | 7 | 0 | 6 |
| P12086 | WikiKids ID | 326 | 0.61 | 1 | ok | 6.4 | False | False | False | none | 2 | 5 | 26 | 7 | feed, json |  | rdfa | page text only (page served to plain HTTP) | 12 | 13 | 1 | 0.08 | 7 | 0 | 2 |
| P12098 | Kinobox person ID | 42 | 6.4 | 1 | ok | 33.5 | True | False | True | ads served | 10 | 59 | 510 | 8 | json |  | json-ld, rdfa | page blocked for plain HTTP only + page text for 55/60 values | 11 | 60 | 1 | 0.36 | 3 | 1 | 42 |
| P12153 | FilmAffinity person or company ID | 621 | 0.21 | 1 | ok | 13.8 | True | False | True | ads served | 4 | 97 | 113 | 15 | json |  | microdata, opengraph, rdfa | plain HTTP + page text for 12/30 values | 12 | 30 | 1 | 0.42 | 5 | 0 | 10 |
| P12385 | Gran Enciclopèdia Catalana ID | 85 | 2.84 | 1 | ok | 4.6 | True | True | False | ads served | 0 | 8 | 98 | 1 |  |  | rdfa | page text only (page blocked for plain HTTP) | 16 | 27 | 1 | 0.08 | 9 | 0 | 10 |
| P12386 | Dansk Forfatterleksikon ID | 358 | 0.52 | 1 | ok | 6.2 | False | False | False | none | 0 | 1 | 1075 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 14 | 65 | 1 | 0.52 | 5 | 0 | 42 |
| P12451 | Arabic Ontology lexical concept ID | 652 | 0.2 | 1 | ok | 9.3 | False | False | False | none | 4 | 10 | 36 | 9 | json, xml |  | opengraph | plain HTTP + page text for 1/13 values | 9 | 13 | 2 | 0.0 | 4 | 0 | 0 |
| P12458 | Parsifal cluster ID | 27 | 10.78 | 3 | ok×3 | 7.8 | False | False | False | none | 1 | 3 | 133 | 18 | json, xml |  | rdfa | plain HTTP + page text for 11/39 values | 17 | 39 | 2 | 0.19 | 9 | 0 | 8 |
| P12483 | PMB – Personen der Moderne Basis person ID | 293 | 0.71 | 1 | ok | 6.2 | False | False | False | none | 1 | 4 | 36 | 3 |  | json | opengraph, rdfa | browser only + page text for 20/47 values | 22 | 47 | 2 | 0.37 | 8 | 0 | 2 |
| P12502 | UCA authority ID | 1241 | 0.07 | 1 | ok | 6.7 | False | True | True | none | 2 | 2 | 70 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 8 | 11 | 1 | 0.0 | 2 | 0 | 0 |
| P12597 | museum-digital person/organization ID | 126 | 1.86 | 1 | ok | 4.1 | False | False | False | none | 0 | 1 | 10 | 2 | json |  |  | plain HTTP + page text for 19/219 values | 18 | 219 | 35 | 0.45 | 10 | 0 | 7 |
| P12614 | az.lib.ru author ID | 595 | 0.22 | 1 | ok | 6.2 | False | False | False | none | 2 | 8 | 57 | 0 |  |  |  | page text only (page served to plain HTTP) | 16 | 67 | 2 | 0.4 | 6 | 0 | 39 |
| P12674 | Kunstenpunt Knowledge Graph ID | 451 | 0.35 | 1 | ok | 4.9 | False | False | False | none | 0 | 0 | 35 | 10 |  | feed, json, json-ld, n-triples, rdf-xml, turtle | opengraph, rdfa | browser only + page text for 2/17 values | 9 | 17 | 2 | 0.2 | 2 | 0 | 1 |
| P12749 | SNARC ID | 123 | 1.93 | 1 | ok | 15.0 | False | False | False | none | 0 | 2 | 129 | 10 |  | feed, json, json-ld, n-triples, rdf-xml, turtle | opengraph, rdfa | browser only + page text for 13/80 values | 22 | 80 | 2 | 0.05 | 12 | 0 | 2 |
| P12800 | Vikidia article ID | 315 | 0.64 | 1 | ok | 4.6 | False | False | False | none | 0 | 3 | 39 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 15 | 45 | 1 | 0.56 | 8 | 0 | 28 |
| P12836 | Douban personage ID | 223 | 0.99 | 1 | ok | 7.4 | False | False | False | none | 0 | 5 | 31 | 4 | json |  | opengraph | plain HTTP + page text for 22/47 values | 17 | 47 | 2 | 0.27 | 8 | 0 | 19 |
| P12854 | Plex person key | 116 | 2.07 | 1 | ok | 6.0 | False | False | False | none | 0 | 10 | 70 | 2 | json |  | rdfa | page text only (page served to plain HTTP) | 7 | 8 | 1 | 0.0 | 5 | 0 | 1 |
| P13019 | RedBA Granada authority ID | 323 | 0.62 | 1 | ok | 6.2 | False | True | False | none | 0 | 1 | 73 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 20 | 64 | 7 | 0.06 | 8 | 0 | 22 |
| P13030 | Münzkabinett ID | 531 | 0.27 | 1 | ok | 5.7 | False | False | False | none | 0 | 1 | 15 | 6 | json-ld, n-triples, rdf-xml, turtle | csv | opengraph | plain HTTP + page text for 7/25 values | 14 | 25 | 2 | 0.2 | 6 | 0 | 1 |
| P13049 | DDB person (GND) ID | 16 | 19.69 | 2 | ok×2 | 6.4 | False | True | True | none | 2 | 3 | 66 | 4 |  |  | opengraph, rdfa | plain HTTP + page text for 25/28 values | 13 | 28 | 1 | 0.21 | 6 | 0 | 5 |
| P13166 | PUG authority ID | 120 | 2.02 | 1 | ok | 11.2 | False | False | False | none | 2 | 4 | 10 | 0 |  |  |  | page text only (page blocked for plain HTTP) | 6 | 8 | 1 | 0.0 | 1 | 0 | 0 |
| P13183 | JudaicaLink person (GND) ID | 167 | 1.41 | 1 | ok | 9.7 | False | False | False | none | 0 | 0 | 1252 | 6 | json-ld, rdf-xml, turtle |  | rdfa | plain HTTP + page text for 27/79 values | 11 | 79 | 2 | 0.0 | 2 | 0 | 33 |
| P13204 | Wellcome Collection concept ID | 54 | 5.21 | 1 | ok | 4.6 | False | False | False | ads served | 2 | 8 | 102 | 7 | json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 12/15 values | 11 | 15 | 1 | 0.15 | 3 | 0 | 2 |
| P13255 | L'Humanité topic ID | 2641 | 0.01 | 1 | ok | 8.0 | False | False | False | ads served | 4 | 25 | 182 | 16 | feed, json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 4/5 values | 4 | 5 | 1 | 0.5 | 1 | 0 | 2 |
| P13437 | Chtyvo author ID | 1041 | 0.09 | 1 | wrong_page | 4.1 | False | False | False | none | 0 | 0 | 2 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P13591 | ‎Yale LUX ID | 6 | 52.45 | 1 | ok | 4.1 | False | False | False | none | 4 | 6 | 28 | 4 | json, json-ld |  | opengraph, rdfa | plain HTTP | 15 | 164 | 10 | 0.04 | 9 | 0 | 60 |
| P13613 | Enciclopedia Galega Universal ID | 226 | 0.97 | 1 | ok | 5.7 | False | False | False | none | 2 | 4 | 53 | 2 |  |  | opengraph, rdfa | plain HTTP + page text for 13/15 values | 8 | 15 | 2 | 0.14 | 3 | 0 | 7 |
| P13750 | Arab Encyclopedia concept ID | 700 | 0.18 | 1 | ok | 7.2 | False | False | False | none | 2 | 4 | 133 | 2 |  |  | opengraph, rdfa | plain HTTP + page text for 32/55 values | 17 | 55 | 2 | 0.45 | 4 | 1 | 17 |
| P13772 | Harper's tag | 228 | 0.95 | 1 | ok | 6.2 | True | False | False | ads served | 5 | 15 | 92 | 5 | json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 7/12 values | 7 | 12 | 1 | 0.75 | 2 | 0 | 5 |
| P13797 | ‎Dimensions.com element ID | 1488 | 0.05 | 1 | ok | 8.3 | False | False | False | none | 2 | 14 | 972 | 15 | feed, json |  | json-ld, opengraph, rdfa | plain HTTP + page text for 11/31 values | 16 | 31 | 1 | 0.32 | 6 | 0 | 6 |
| P13804 | ‎Sancho el Sabio Foundation ID | 433 | 0.38 | 1 | ok | 7.1 | False | False | False | none | 4 | 7 | 53 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 15 | 28 | 1 | 0.23 | 8 | 0 | 8 |
| P13951 | National Virtual Library of India ID | 76 | 3.36 | 44 | load_failed×44 | 49.2 | False | False | False | none | 0 | 0 | 184 | 0 |  |  |  | none | 0 | 0 | 0 |  | 0 | 0 | 0 |
| P14178 | Obálky knih ID | 104 | 2.44 | 2 | wrong_page×2 | 5.6 | False | True | False | none | 1 | 2 | 13 | 2 |  |  | opengraph | page text only (page served to plain HTTP) | 13 | 37 | 2 | 0.03 | 7 | 0 | 4 |
| P14211 | Library of the University of Santiago de Compostela authority ID | 630 | 0.21 | 1 | ok | 12.0 | False | False | False | none | 0 | 5 | 200 | 10 | json |  | json-ld, opengraph, rdfa | page blocked for plain HTTP only + page text for 3/13 values | 6 | 13 | 1 | 0.2 | 2 | 0 | 1 |
| P14214 | Foto Atlas taxonomy ID | 3303 | 0.01 | 1 | ok | 4.1 | False | False | False | none | 3 | 10 | 35 | 8 | feed, json |  | json-ld, microdata, opengraph, rdfa | plain HTTP + page text for 4/21 values | 11 | 21 | 2 | 0.0 | 5 | 0 | 1 |
| P14225 | NSK ID | 97 | 2.6 | 1 | ok | 9.2 | False | False | False | none | 0 | 0 | 172 | 9 | json, xml |  | json-ld, opengraph, rdfa | plain HTTP, partly (page blocked for plain HTTP) + page text for 25/73 values | 16 | 73 | 5 | 0.28 | 8 | 0 | 12 |
| P14397 | ‎Darwin Correspondence ID | 542 | 0.26 | 1 | ok | 9.7 | False | False | True | none | 0 | 4 | 141 | 4 | json |  | microdata, opengraph, rdfa | page text only (page served to plain HTTP) | 10 | 11 | 1 | 0.1 | 5 | 0 | 0 |
| P14536 | FES digital collections entity ID | 129 | 1.77 | 1 | ok | 11.7 | False | False | False | none | 0 | 0 | 30 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 9 | 13 | 2 | 0.0 | 5 | 0 | 0 |
| P14541 | Encyclopedia of China (Third Edition) ID (2026) | 176 | 1.31 | 1 | ok | 38.7 | False | False | False | none | 0 | 2 | 165 | 1 | json |  |  | page text only (page served to plain HTTP) | 9 | 12 | 2 | 0.3 | 3 | 0 | 3 |
| P14611 | Pontifical Urbaniana University ID | 278 | 0.76 | 1 | ok | 7.6 | False | False | True | none | 0 | 2 | 53 | 1 |  |  | rdfa | page text only (page served to plain HTTP) | 7 | 7 | 1 | 0.0 | 1 | 0 | 0 |
| P14750 | ‎HAND ID | 30 | 10.06 | 1 | ok | 4.1 | False | True | False | none | 0 | 1 | 204 | 5 | json |  | rdfa | plain HTTP + page text for 2/18 values | 9 | 18 | 2 | 0.25 | 6 | 0 | 0 |
