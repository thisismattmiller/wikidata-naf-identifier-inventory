# wikidata-naf-identifier-inventory

What does each external identifier on a Wikidata name-entity page actually link to, and
does that site expose machine-readable data (JSON, RDF, XML, MARC...)?

Mark Twain ([Q7245](https://www.wikidata.org/wiki/Q7245)) is the test entity because he has
nearly every common bibliographic identifier (318 identifier properties, 420 values).

**Atlas:** the results are a single static page, the *Twain Identifier Atlas*, served from `docs/`
by GitHub Pages at <https://thisismattmiller.github.io/wikidata-naf-identifier-inventory/>.
`build_map_data.py` writes it (from `atlas.template.html` + `data/<QID>/analysis/`) to both
`data/<QID>/analysis/atlas.html` and `docs/index.html`; `.github/workflows/pages.yml` deploys
`docs/` on every push to `main` (set Pages → Source to "GitHub Actions" in the repository settings once).
The page is self-contained apart from D3 from cdnjs.

Licence: MIT (see `LICENSE`).

## Pipeline

```sh
uv run python fetch_identifiers.py Q7245   # 1. identifiers + the URL each one links to
uv run python crawl.py Q7245               # 2. open each URL in Chrome via AppleScript, save what's there
uv run python build_inventory.py Q7245     # 3. roll the records up into inventory.csv / inventory.md
uv run python fetch_representations.py Q7245  # 4. download every data representation the crawl found
uv run python browser_fetch.py Q7245           # 5. retry the ones plain HTTP could not get, from inside the browser
uv run python profile_representations.py Q7245 # 6. reduce every data file to one canonical element schema
uv run python compare_wikidata.py Q7245        # 7. compare each site's elements and cross-links with Wikidata
uv run python quality_report.py Q7245 --probe-embedded  # 8. how good each site is as a source (resolution, walls, ads, formats, access, useful-beyond-Wikidata score)
#   then steps 6 and 8 once more: pages step 8 judged wrong_page (somebody else's record, a Spirit heading) drop out of step 6's profiles
uv run python build_audit_inputs.py Q7245     # audit: per-identifier dossiers for Opus auditors (analysis/audit/INSTRUCTIONS.md)
uv run python identifier_landscape.py          # landscape: which identifiers bibliographic entities (items with P244) carry, via QLever
uv run python probe_clients.py Q7245            # 8b. can curl get it? page + the data files used, three client profiles (plain curl / User-Agent / browser headers)
uv run python build_image_sprite.py Q7245 --browser  # 9b. download the images the sites state, tile them into analysis/twain_images.jpg
uv run python build_map_data.py Q7245          # 9. the atlas: analysis/map_data.json -> analysis/atlas.html and docs/index.html
uv run python scrub_secrets.py Q7245           # before committing: redact the sites' own browser keys and session tokens from stored request URLs
```

Steps 6–7 write `data/<QID>/analysis/`: `profiles/<P>.json` (per site: formats, vocabularies,
elements with values/languages, unmapped predicates, key-path profiles of ad-hoc JSON),
`site_elements.csv`, `wikidata_elements.json`, `comparison.csv` / `comparison_matrix.csv`
(site × element: match / partial / mismatch / no_overlap / site_only / wikidata_only, with the values on both
sides and the site values Wikidata lacks), `crosslinks.csv` (every same-as a site asserts, resolved
to a Wikidata identifier property and checked against the item), `vocabulary_mapping.csv`
(site predicate/MARC field → element → Wikidata property) and `report.md`.

Element extraction is deterministic for RDF/JSON-LD (rdflib, with a dedicated walker for nested
CIDOC-CRM / Linked Art records such as Yale LUX: typed Appellation nodes, Birth/Death time-spans and
places, P2_has_type concepts sorted into nationality/gender/occupation by their own type), MARC (pymarc),
MADS XML and EAC-CPF, MARC serialised as JSON (VIAF's `mx:record` conneg payloads, IdRef's export) with
UNIMARC authorities (name in 200, coded data in 100) mapped onto the MARC21 tags; ad-hoc JSON/XML uses
key-name heuristics (values must mention the entity). Sites whose
data only exists as ad-hoc JSON/XML are extracted by Claude Opus subagents (instructions in
`analysis/llm_batches/INSTRUCTIONS.md`, outputs in `analysis/llm_extractions/<P>.json`, merged by
step 6). Every resolved site also gets an Opus pass over its rendered page text `pages/<key>.txt`, because
structured data is often a title and a description while the page shows work lists, translators,
holdings and relatives (Ben Yehuda's six Hebrew editions, for instance); for sites with no
machine-readable data at all it is the only source (`analysis/llm_batches_pages/INSTRUCTIONS.md`, outputs in
`analysis/llm_extractions_pages/<P>.json`, values tagged `llm-page:`; a site whose values are all page text is
reported as "page text only", and `quality_sites.csv` keeps `page_text_values` next to `values` so the two
sources stay distinguishable); a site with no representation file at all still gets a profile from that extraction.
Step 6 takes values only from JSON objects and RDF nodes that are about the entity (a name-bearing object must carry one of
his labels in full, so relatives, books, ad players, consent banners and the crawler's own geolocation are dropped; site-wide
WebSite/Organization/Video nodes and vocabulary classes are never the focus; OpenGraph counts only when the card is a sentence
about him; logos and placeholder images, schema type names and bare URIs never count as descriptive values).
Step 6 also gates every site on *is this about the entity*: a site with no personal element (name,
date, work...) and no value naming the entity is page chrome (a site tagline as `og:description`, the
share image) and its values are parked in `chrome_elements`, not counted as data.
Every disagreement with Wikidata is then judged by an Opus reviewer
(`analysis/review.json`, `analysis/review.md`, folded into `report.md`). `analysis/vocabulary_mapping.md`
is the aggregated predicate/field → element → Wikidata property map.

Step 8 writes `analysis/quality.md` (counts and percentages: resolution, challenge/login/consent
walls, ads vs analytics vs CDN third parties, page weight, serialisations *retrieved* vs those that
actually *carried entity data*, how the data was reachable - plain HTTP / browser session only /
JS-rendered markup only - richness, a 'useful beyond Wikidata' score (per element, log2 of the distinct values Wikidata lacks, weighted: works, works about him and relatives 1.5; names, occupations, places 1; descriptions, gender, nationality 0.5), unique-vs-repeated values across sites, overlap with Wikidata,
quality by identifier popularity) plus `quality_sites.csv` (one row per property) and
`quality_records.csv` (one row per page, with every ad/analytics host). `--probe-embedded`
re-fetches each page that had embedded markup with plain Python and records whether the markup is
in the server HTML (`analysis/embedded_probe.json`); several sites (id.loc.gov, Britannica, Discogs,
IMDb, Primo OPACs...) refuse non-browser clients on their HTML even though their data endpoints answer.
Ads are detected from the hosts the rendered page contacted (ad networks vs analytics vs consent
managers vs CDNs, lists at the top of `quality_report.py`) and from ad-slot markup in the saved HTML.
Step 8 also demotes `ok` pages to `wrong_page` when the browser rendered something other than the
entity's record: a Wayback calendar page, a VIAF "processed" or toolforge redirector that never
forwarded, a challenge page the crawler did not recognise, or a page that never mentions the entity
(any label/alias from `entity.json`) and yielded no data about them (a JS app shell, a home page, a 403), or whose
title is a catalogue heading for somebody else (`record for a different person`, e.g. Santa Sabina's id 10370 opens
"Muguet, Christian"); login-box pages get the same checks, since a Koha/Primo login box is site chrome.
"Mentions the entity" means a whole-word match on a distinctive token (5+ characters or a birth/death
year) or two different tokens together - `mark` inside `marquee` does not count; the check reads the
page text plus any `__frameN.txt` child frames, and falls back to the saved DOM when the visible text
is short (a consent modal can hide the whole record from `innerText`, as on the Vatican OPAC).

Two optional per-entity files steer re-crawls: `url_overrides.json` (`{P: {url, reason}}` - crawl this
URL instead of the Wikidata one, e.g. an archived snapshot found via the Wayback CDX API or a resolved
redirector; the record keeps the original as `wikidata_url`) and `extra_representations.json`
(`{P: [url, ...]}` - data endpoints the page never advertises, e.g. Yale LUX's `/data/person/<uuid>`
Linked Art record behind its JS app). Re-run with `--only P1,P2 --force` on steps 2 and 4. Step 4 also follows paginated XHR JSON (`?page=N` with a
`summary.totalPages`, as id.loc.gov's "Subject Of Works" / "Contributor To Works" panels use) up to 60 pages, and
step 6 maps those panels to `work` and to `subject_of` (works *about* the person - an element Wikidata has no
item-level property for, so it is always site-only).

`identifier_landscape.py` asks the QLever Wikidata endpoint (`https://qlever.dev/api/wikidata`,
fresh and fast but every query must finish in 30 s - it answers 429 with "Operation timed out")
for the number of P244 items carrying each of the ~10.6k external-identifier properties, overall and
for humans; the full GROUP BY times out, so it groups over 200k-item slices and adds them up. Output:
`data/landscape/landscape.md` (class breakdown, identifiers-per-item distribution, top 150 ranked,
where the test entity's identifiers sit) and `counts.csv`; step 8 picks the ranks up for its per-site table.

VIAF's record API is POST-only and token-gated; `representations/P214__*/api_cluster-record_*`
were obtained by replaying the page's own `/api/cluster-record` call (with its `x-ui-token`) from
inside the crawler tab.

Step 2 needs Google Chrome with **View > Developer > Allow JavaScript from Apple Events** on.
It opens its own Chrome window and drives only that one. It is resumable: identifiers that
already have a record are skipped. Useful flags: `--only P214,P244`, `--limit 10`, `--force`,
`--retry-status challenge_suspected,load_failed,load_timed_out`.

## Output (`data/<QID>/`)

| file | what |
|---|---|
| `entity.json` | the raw Wikidata entity |
| `wikidata_page.html` | the entity page as served (source of the identifier links) |
| `identifiers.json` | one row per identifier value: property, value, the URL on the Wikidata page, the formatter URL(s), third-party formatter URLs, RDF URI formatter, source website, issuing institution |
| `pages/<P>__<value>.html` | rendered DOM of the identifier page, after client-side JS |
| `pages/<P>__<value>.txt` | visible text of that page |
| `records/<P>__<value>.json` | what `extract.js` found: final URL, HTTP status, response headers of the page (`Link:` etc.), `<link>` elements, JSON-LD, RDFa/microdata, meta tags, links that look like exports/APIs, background XHR/fetch calls, forms, challenge/login/not-found signals |
| `inventory.csv` / `inventory.md` | the roll-up, one row per identifier |
| `representations/<key>/` | the actual data files: `alternate_N` (from `<link rel=alternate>` / `Link:` headers), `export_N` (export/API links on the page), `xhr_N` (the page's own JSON calls), `conneg_N` (content negotiation on the identifier URL), `embedded_<syntax>.json` (JSON-LD / RDFa / microdata / OpenGraph lifted from the saved HTML with extruct); `manifest.json` lists each attempt with status, claimed content-type and the sniffed format |
| `representations/summary.csv` | one row per representation attempt across all pages |
| `crawl.log` | progress of the last crawl |
| `analysis/quality.md`, `quality_sites.csv`, `quality_records.csv` | step 8: source-quality report (see above) |
| `url_overrides.json`, `extra_representations.json` | optional: crawl a different URL for a property / fetch extra data URLs (see above) |
| `analysis/llm_extractions_pages/<P>.json` | Opus extraction from rendered page text for sites with no machine-readable data |
| `analysis/map_data.json` → `uber` | the "Everything the sites say about him" section: per element, every site's values merged and de-duplicated (site count per value, Wikidata-shared and Wikidata-only marks), plus per-site holdings with the first ten values for list elements (works, works about him, related agents, links, identifiers, sources) |
| `analysis/client_probe.json` | `probe_clients.py` (step 8b): for every site, the real curl binary against the page and the data files his values came from, three client profiles in turn (curl's own User-Agent; an identifying User-Agent; Chrome User-Agent with browser headers), no cookies or JavaScript. "Served" = HTTP 200 with his name in the body. The atlas's access facet is built from this, a site classed by the hardest file it needs |
| `analysis/images/images.json`, `analysis/twain_images.jpg` | `build_image_sprite.py` (step 9b): every image URL the sites state (plus Wikidata's P18 files) downloaded, cropped to a 50 px square and tiled into one sprite sheet (copied to `docs/`); the manifest records sites, size, fetch status and which URLs refused plain clients even from the browser. The atlas's Images block renders the sprite at 25 px. `--browser` retries blocked URLs inside the crawler's Chrome window |
| `analysis/audit/` | per-identifier audit dossiers (`batches/`), auditor instructions and verdicts (`verdicts_N.json`; round 2 in `round2/`), shown per tile on the atlas |
| `analysis/beyond_wikidata.md` | curated list of what the sites offer that Wikidata lacks (Opus curator over `beyond_wikidata_input.json`) |

`status` in a record is a rough triage label (`ok`, `http_error`, `blocked`, `challenge_suspected`,
`login_wall_suspected`, `empty_page`, `load_timed_out`, `load_failed`); the raw signals it was
derived from are kept in `page.signals` so a human can overrule it. `login_wall_suspected` only
means "has a password field and says log in", which every Koha OPAC does; check the screenshot.

## How a page is harvested

`crawl_page.applescript` sets the tab to `about:blank`, then to the URL, waits for Chrome
to finish loading (max 45 s), runs `prefetch.js` (a same-origin HEAD request so the page's
own response headers are available), waits until the DOM stops changing (so SPAs have
rendered), then runs `extract.js` and returns its JSON, and `screencapture` grabs the window
by its window-server ID (no focus change needed). On a suspected bot challenge the crawler
polls the tab until it changes; after 15 s it sends a macOS notification and brings its window
forward so a human can click through (it gives up after 20 min). Cloudflare "you have been
blocked" pages are recorded as `blocked` immediately.

Gotchas learned the hard way: Chrome's AppleScript window ids are *text* and some exceed
AppleScript's integer range, so never coerce them; reCAPTCHA/Incapsula scripts appear on
ordinary pages of protected sites, so widget presence only means "challenge" on a bare page;
one Koha OPAC hung Chrome's scripting channel for two minutes (handled by a subprocess timeout
and a fresh window).

Hosts are hit at most once every 3 seconds. Pages render in the user's own Chrome
profile, so cookies/logins apply.

Step 4 fetches with plain HTTP (no browser), so sites that only serve a real browser show up
as 403/HTML there even though step 2 rendered them; the `detected` column says what actually
came back (`json-ld`, `rdf-xml`, `marcxml`, `n-triples`, `turtle`, `html`...), independent of
what the link or the server claimed. A `conneg` row with `detected=html` means the server
ignored the Accept header; those bodies are not kept.

## Not done yet

- judging the data: which representations actually describe the entity, and how richly
- identifiers with no formatter URL on Wikidata (3 for Twain) have no page to crawl
