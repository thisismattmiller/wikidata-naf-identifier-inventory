# Extraction task

You are extracting what a website says about ONE person — Mark Twain (Samuel Langhorne Clemens, 1835-11-30 – 1910-04-21), including records for his pseudonyms (Quintus Curtius Snodgrass, Louis de Conte, Sieur Louis de Conte, Jean François Alden) — from ad-hoc JSON/XML data files that automated parsers could not interpret.

Your batch file (JSON) lists sites. For each site: `property` (Wikidata property id), `label` (site name), `have` (elements already extracted deterministically — you may still add values), `files` (paths relative to `data/Q7245/representations/`, i.e. read `data/Q7245/representations/<file>`).

For each site, read its files and write ONE output file `data/Q7245/analysis/llm_extractions/<property>.json` with this shape:

```json
{
 "property": "P1234",
 "label": "Site name",
 "files_read": ["P1234__x/xhr_1.json"],
 "about_entity": true,
 "notes": "one or two sentences: what the file(s) are (page API, search results, consent config...), and anything odd",
 "elements": {
   "name_preferred": [{"value": "Twain, Mark", "lang": "en", "via": "xhr_1.json: $.record.heading"}],
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
- Only data about Mark Twain / Clemens (or his pseudonym records). If a file is about another entity, search results containing many people, or only page chrome (cookie consent, menus, site name), set `about_entity` false for that file in `notes` and extract nothing from it. Never invent values.
- `value` is the cleaned value; keep the original text in `raw` when you normalised it (dates → ISO `YYYY-MM-DD` / `YYYY-MM` / `YYYY`; keep place strings as given). `lang` is a BCP47 code when known, else null. `via` says which file and where in it (JSON path or XML element) the value came from.
- Only include an element key when you found values; omit empty ones. Cap each list at 40 values; prefer distinct ones.
- `same_as`: full URIs the site gives for the same person in other systems (VIAF, ISNI, LC, GND, Wikidata, Wikipedia...). `identifier`: the site's own id(s) for the person. `description`: biographical/scope notes (one per language). `work`: titles of works the site attributes to him. `related_agent`: named people/organizations linked to him with the relation if stated.
- Big files: do not read a 400 KB file whole. Grep for `Twain`, `Clemens`, `1835`, `1910` and read around the hits; the Read tool supports offset/limit.
- Files named `embedded_opengraph.json` / `embedded_microdata.json` are page metadata lifted from HTML; `og:description` is usually a one-line description of the entity, `og:title` is usually the page title (treat as name only if it is clearly the person's name).
- Work through every site in the batch. Write each output file as soon as that site is done (use the Write tool). When finished, reply with a short list: property → number of elements found, plus any sites where nothing about the entity was present.
