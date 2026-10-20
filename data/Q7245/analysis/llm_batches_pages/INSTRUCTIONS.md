# Extraction task (rendered page text)

You are extracting what a website says about ONE person — Mark Twain (Samuel Langhorne Clemens, 1835-11-30 – 1910-04-21), including records for his pseudonyms (Quintus Curtius Snodgrass, Louis de Conte, Sieur Louis de Conte, Jean François Alden) — from the visible text of the web page as the browser rendered it. These are sites that offer no machine-readable data at all (no RDF, no JSON, no MARC), so the page text is the only source.

Your batch file (JSON) lists sites. For each site: `property` (Wikidata property id), `label` (site name), `status` (crawl status; `login_wall_suspected` / `http_error` pages may still show the record), `files` (each with `file`, a path relative to `data/Q7245/` — read `data/Q7245/<file>` — plus `chars`, `url`, `title`). `__frameN.txt` files are the text of iframes on that page.

For each site, read its files and write ONE output file `data/Q7245/analysis/llm_extractions_pages/<property>.json` with this shape:

```json
{
 "property": "P1234",
 "label": "Site name",
 "files_read": ["pages/P1234__x.txt"],
 "about_entity": true,
 "page_kind": "authority record | catalogue record | encyclopedia article | biography page | author page with work list | search results | home page | error page | other",
 "notes": "one or two sentences: what the page is, what it mainly offers (a bio, a work list, holdings, cross-links...), and anything odd (navigation only, record truncated, login box over the record...)",
 "elements": {
   "name_preferred": [{"value": "Twain, Mark", "lang": "en", "via": "page heading"}],
   "name_variant": [...], "given_name": [...], "family_name": [...], "pseudonym": [...],
   "birth_date": [{"value": "1835-11-30", "raw": "30 Nov 1835", "lang": null, "via": "..."}],
   "death_date": [...], "birth_place": [...], "death_place": [...], "activity_place": [...],
   "gender": [...], "occupation": [...], "field_of_activity": [...], "nationality": [...], "language": [...],
   "description": [{"value": "American writer ...", "lang": "en", "via": "..."}],
   "work": [...], "subject_of": [...] (works ABOUT him: biographies, studies, portraits, subject-search hits), "related_agent": [...], "same_as": [{"value": "http://viaf.org/viaf/50566653", "via": "..."}],
   "identifier": [...], "image": [...], "source": [...], "record_created": [...], "record_modified": [...], "license": [...]
 }
}
```

Rules:
- Only data about Mark Twain / Clemens (or his pseudonym records). Page chrome (site name, menus, cookie banners, footer, "related" sidebars about other people) is not data. If the page turns out not to be about him at all (search results for many people, a home page, an error), set `about_entity` false, say why in `notes`, and extract nothing. Never invent values.
- `value` is the cleaned value; keep the original text in `raw` when you normalised it (dates → ISO `YYYY-MM-DD` / `YYYY-MM` / `YYYY`; keep place strings as given). `lang` is a BCP47 code for the language the text is in (page language if not stated), else null. `via` says where on the page the value came from (heading, infobox row "Born", "Works" list, a sentence of the bio...).
- `description`: the biographical / scope text about him, in the page's language, trimmed to the first ~600 characters if long (note "truncated" in `raw`). One per language.
- `work`: titles of works the page attributes to him — cap at 40, prefer distinct titles, drop edition noise (years, publishers) into `raw` if you keep it.
- `related_agent`: named people/organisations the page links to him, with the relation when stated (e.g. "Olivia Langdon (wife)").
- `same_as`: full URIs the page gives for the same person elsewhere (VIAF, ISNI, LC, GND, Wikidata, Wikipedia...); `identifier`: the site's own id(s) for him as shown on the page.
- Only include an element key when you found values; omit empty ones.
- Big files: do not read a 100 KB+ file whole. Grep for `Twain`, `Clemens`, `1835`, `1910` and read around the hits; the Read tool supports offset/limit. Small files (< 20 KB) read whole.
- Work through every site in the batch. Write each output file as soon as that site is done (use the Write tool). When finished, reply with a short list: property → page_kind, number of elements found, plus any sites where nothing about the entity was present.

## Round 2: sites that already have structured data (batches 10 and up)

Batches 10 and up cover sites whose structured data (JSON-LD, RDFa, an API...) was already profiled but is often thin - a title and an og:description - while the rendered page shows much more (work lists with translators and editions, holdings, relatives, cross-links). Extract everything the page says about him exactly as above, regardless of what the structured data may already contain; the merge step de-duplicates. The same rules apply: only data about him, never invent, page chrome is not data, cap works at 40 distinct titles (note in `notes` when the page shows more), and name translators/illustrators/co-authors in `related_agent` with their relation.
