# Review task: site vs Wikidata disagreements (second pass, page-text sites)

Entity: Mark Twain (Q7245) = Samuel Langhorne Clemens, born 1835-11-30 Florida, Missouri; died 1910-04-21 Redding, Connecticut. Pseudonyms with their own authority records in some systems: Quintus Curtius Snodgrass, Louis de Conte / Sieur Louis de Conte, Jean François Alden; other pen names Josh, Thomas Jefferson Snodgrass, Sergeant Fathom, W. Epaminondas Adrastus Blab.

Context file: `data/Q7245/analysis/review_input_pages.json` holds `wikidata` (every Wikidata value per element, with language), `wikidata_identifiers` (every external identifier Wikidata has for him, by property label) and `extraction_notes` (what each site's page was). Read the `wikidata` and `wikidata_identifiers` parts once before judging; look up a site's extraction note when you need to know what the page was.

Your batch file lists `items`. Each is one disagreement the automated comparison could not settle:
- `kind: element` — the site's values for one element (`site_values`, `‖`-separated, `@lang` suffix when known) vs Wikidata's (`wikidata_values`, truncated); `status` is `mismatch` (nothing in common), `partial` (dates/places agree only in part, e.g. year only), or `no_overlap` (lists that share nothing, typically works or related agents). `site_via` says where on the page the value came from (prefix `llm-page:` = extracted from rendered page text by an earlier pass).
- `kind: crosslink` — a link the site gives to another identifier system (`target_system`, `target_value`) that Wikidata does not hold, or holds with a different value (`wikidata_verdict`).

For each item give exactly one verdict:
- `equivalent` — same fact, different form (year-only vs full date, transliteration, "Clemens, Samuel Langhorne" vs "Samuel Langhorne Clemens", a translated work title, a place given at a different granularity, a pseudonym record's own name).
- `different_entity` — the site value describes a different person/thing (a pseudonym treated as a separate authority record counts as *equivalent* when the record is clearly his; a genuinely different person is `different_entity`).
- `extraction_noise` — the site value is not a real claim (page chrome, a label taken as a name, a translator listed as a related agent without relation, a machine-translation artefact, an id string in a name field).
- `site_disagrees` — a real, specific claim that contradicts Wikidata (a different death date, a different birthplace) where the site is probably wrong or unverifiable.
- `wikidata_gap_or_error` — the site is right (or probably right) and Wikidata lacks or has the wrong value: a missing alias, pseudonym, identifier, work, relative; or a wrong/outdated Wikidata identifier. Fill `likely_correct` with the value Wikidata should have.
- `unclear` — cannot be judged from the data.

For works (`no_overlap` on `work`): judge whether the titles are his works (translations and editions count as his); Wikidata's work list is partial by design, so a site listing genuine Twain works that Wikidata lacks is `equivalent` unless a title is clearly not his (`different_entity`) or noise. Mention notable gaps (a well-known work missing from Wikidata) in the reason.

Write ONE file `data/Q7245/analysis/review_batches_pages/verdicts_<N>.json` (N = your batch number) as a JSON list, one object per item in your batch, in order:
```json
{"index": 1000, "kind": "element", "property": "P1234", "site": "Site", "element_or_link": "birth_date", "verdict": "equivalent", "reason": "one or two sentences", "likely_correct": null}
```
`element_or_link` is the `element` for element items and the `link` for crosslink items. Keep `reason` specific (quote the values that matter). Then reply with: verdict counts, and a bulleted list of every `wikidata_gap_or_error` and `site_disagrees` item (site, element/link, the value, one line why) — this list is used verbatim in the write-up, so make it precise. Use only Read and Write tools; do not modify any other file; never commit.
