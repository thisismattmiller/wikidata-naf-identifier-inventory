# Audit task: is what the atlas says about each identifier true?

Entity: Mark Twain (Q7245) = Samuel Langhorne Clemens, 1835-11-30 Florida, Missouri – 1910-04-21 Redding, Connecticut. Pseudonym records (Quintus Curtius Snodgrass, Louis de Conte, Jean François Alden, Thomas Jefferson Snodgrass, J. W. Bothwell) are *his*. Library headings "Twain, Mark (Spirit)" are NOT (books channelled through a medium).

The project crawled every external identifier on his Wikidata item with a real browser, pulled each site's data representations (RDF, JSON, MARC, embedded markup, XHR payloads), had an LLM read the rendered page text, reduced everything to one element schema, compared it with Wikidata, and summarised each site on a web atlas. Several whole classes of error were found by spot checks (a site tagline counted as data; JS-loaded work lists captured as page 1 only and then dropped; MARC-as-JSON unparsed; a Wikidata id that opens somebody else's record). Your job is to look at every site in your batch end to end and say whether the atlas is telling the truth about it.

Your batch file is a JSON list, one object per identifier property:
- `wikidata_values` / `records`: what Wikidata links to, what the browser got (`crawl_status`, `title`, `final_url`, `override_reason` when a different URL was crawled on purpose), and `page.excerpt` - the start of the rendered text plus the first passage naming him. Read `data/Q7245/pages/<key>.txt` yourself when the excerpt is not enough (key = the file stem you can derive from the record: `<property>__<value>`; grep for Twain/Clemens). `screenshot` is a PNG you may view.
- `atlas_labels`: what the atlas shows. `status` (ok / login_wall_suspected / wrong_page / http_error / load_failed / blocked / challenge_suspected), `resolved`, `wrong_page_reason`, `access` (how a machine can get the entity data: plain HTTP / browser only / page blocked for plain HTTP / JS-rendered / page text only, "+ page text for n/m values" when part came from the rendered text), `format_family` (RDF / library format / embedded markup / ad-hoc JSON/XML / page text (LLM) / none), `values`, `page_text_values`, `uniqueness_bucket` (share of the site's descriptive values that no other crawled site also states: > 60% mostly unique, 30-60% mixed, < 30% mostly repeated, < 5 values too few to judge).
- `profile_elements`: per element, how many values, how many from structured data vs page text, and up to five samples with their provenance (`via`). `chrome_elements_parked` = values judged to be page chrome, not data.
- `extraction_notes`: what the LLM passes said the page / data files were. `review_verdicts` / `review_flags`: how earlier reviewers judged this site's disagreements with Wikidata.

For each site answer:
1. **page_shows_record**: does the crawled page actually show *his* record (true / false / partial, e.g. login wall over the record, search results that include him, a JS shell)?
2. **captured_faithfully**: do the profile elements reflect what the page/data show about him, with no values that are chrome, another person, or wrong? List any `wrong_values`.
3. **missing**: substantial information visible on the page or in its data that the profile lacks (a work list, translators, relatives, dates, cross-links, holdings counts...). Be concrete; "nothing substantial" is a fine answer. Remember the project caps work lists at 40 titles per site on purpose; do not report that as missing.
4. **label_issues**: any atlas label that is wrong or misleading (status, resolved, access, format family, uniqueness bucket, page_text_only). Say what it should be.
5. **notable**: site errors (wrong dates, conflated records), wrong Wikidata values (the id opens somebody else, a Spirit heading), or anything a reader of the atlas should know. Empty string if nothing.
6. **verdict**: one of `sound` (page shows his record and the capture and labels are right), `incomplete` (right record, but substantial data missed), `mislabelled` (capture fine, a label wrong), `wrong_record` (the page is not his record, whatever the labels say), `unreachable` (no usable page: wall, error, dead site - and the labels say so correctly), `unsure`.

Write ONE file `data/Q7245/analysis/audit/verdicts_<N>.json` (N = your batch number) as a JSON list, one object per site in batch order:
```json
{"property": "P1234", "label": "Site", "page_shows_record": "true|false|partial", "captured_faithfully": true, "wrong_values": [], "missing": "…", "label_issues": "…", "notable": "…", "verdict": "sound", "confidence": "high|medium|low"}
```
Be specific and quote values. Use only Read, Grep and Write (and view screenshots); modify no other file; never commit. Reply with the verdict counts for your batch and a bulleted list of every site that is not `sound` or `unreachable` (property, label, verdict, one line why).

## Round 2 (analysis/audit/round2/)

The first round's verdicts led to pipeline fixes: values are only taken from JSON objects that are about him (ad players, cookie
banners, geolocation, interface settings and relatives' records are dropped); site-wide JSON-LD nodes (WebSite, Organization,
VideoObject, vocabulary classes) are ignored; OpenGraph taglines and site logos no longer count; "login wall" pages whose record
rendered are now ok; VIAF-served records whose HTML shell was blank are resolved through their data; "(Spirit)" headings and
records for a different person are wrong_page; "record not found" is a dead identifier; works *about* him go to `subject_of`;
format labels rest on descriptive values only. Each site carries `previous_audit` (your predecessor's verdict). Judge the site
afresh against the refreshed labels and profile, and say in `notable` whether the earlier problem is fixed, partly fixed, or
still there. Write `data/Q7245/analysis/audit/round2/verdicts_<N>.json`.
