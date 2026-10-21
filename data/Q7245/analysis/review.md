# Q7245 (Mark Twain): review of site vs Wikidata disagreements

Source: `review_input.json` (307 items: 177 element, 130 crosslink). Per-item verdicts are in `review.json`.

## 1. Verdict counts

| Verdict | Items |
|---|---|
| equivalent | 163 |
| different_entity | 75 |
| extraction_noise | 43 |
| wikidata_gap_or_error | 18 |
| site_disagrees | 6 |
| unclear | 2 |
| **total** | **307** |

## 2. Wikidata gaps and errors

### Identifiers Wikidata lacks
| Site (source of link) | Missing identifier | What it is |
|---|---|---|
| LC (no2003079632 RWO), VIAF 305239133, DBC 87097968223113 (025) | ISNI 0000000418649406 | Second ISNI for the "Conte, Louis de" identity. Wikidata holds only 0000000108000249 for it, so this may be a duplicate ISNI. |
| GND 1282802690 | VIAF 9358167867532223060005 | VIAF cluster for the GND record of the pseudonym "Bothwell, J. W." |
| LC n93099439 (closeMatch) | FAST 1986616 | FAST heading linked from LC's real-name record "Clemens, Samuel Langhorne". Wikidata has only FAST 31622. |
| NACSIS-CAT DA00300263 (sameAs) | NACSIS-CAT DA03513635 | CiNii record "Clemens, Samuel Langhorne" |
| NACSIS-CAT DA00300263 (sameAs) | NACSIS-CAT DA04621156 | CiNii record "Snodgrass, Quintus Curtius" |
| NTA p068242964 (sameAs) | NTA 068242956 | KB record "Clemens, Samuel Langhorne (1835-1910)" (in VIAF 53367783) |
| National Library of Ireland (VIAF 998) | IdRef 137182333 | Pseudonym record (Alden/Conte, in VIAF cluster 305239133) |
| CiNii Research | crid 1981993809649634716 | Wikidata's P11496 value 1140000791666601344 resolves to this ID, so the stored value looks outdated. |

### Identifiers on Wikidata that look wrong
- **Archives at Yale agent ID `people/56569`**: the record is "Twain, Mark, (Spirit), 1835-1910" and is sameAs LC n82045653, the Spirit record. It belongs on the Spirit item, not on Q7245. (`people/87456` is the real Twain.)
- **Open Plaques subject ID (P1430)** (from the extraction notes, not a review item): the page is James Wallace Richard Hall (1799-1860), so the ID is either wrong or has been reassigned.
- **CiNii Research ID 1140000791666601344**: outdated or redirected (see table above).

### Facts and aliases Wikidata lacks
- **Pseudonym "Jean François Alden"**: Pontificia Università della Santa Croce (400 $a "Alden, Jean François"). The LC 663 note also names it. It is missing from Wikidata's pseudonym list (P742) and aliases.
- **Given name "Langhorne"**: SBN, Open Library, NARA, Geni and Great Norwegian Encyclopedia treat "Samuel Langhorne" as the forename. Wikidata gives Langhorne as a family name (P734 Q29407143). Langhorne is a middle name, so it should be a second P735 and come off P734.
- **Occupation draughtsman**: Artists of the World (AKL) classes him as "Master Draughtsman" (Zeichner). This is plausible, since he drew the sketches in *A Tramp Abroad*. Low priority.
- **Possible pen name "Josh"** (no separate item; it sits inside a noise item): FamilySearch alternateName "Josh Clemens". Clemens signed some early newspaper letters as "Josh".

## 3. Site disagreements

| Site | Element | Site value | Wikidata | Likely right |
|---|---|---|---|---|
| Wien Geschichte Wiki (P7842) | death_date | 1910-05-12 ("† 12. Mai 1910") | 1910-04-21 | Wikidata |
| PORT (P2435) | occupation | író, forgatókönyvíró, rendező (writer, screenwriter, director) | writer etc. | Wikidata (the extra roles come from film adaptation credits) |
| Swedish Open Cultural Heritage (P1260) | given_name / family_name | "Clemens Samuel" / "Langhorne, Mark Twain" | Samuel, Mark / Langhorne, Clemens, Twain | Wikidata (the source mis-splits the name) |
| National Historical Museums of Sweden (P9495) | given_name / family_name | same mis-split as SOCH | same | Wikidata |

## 4. Different-entity cases that point at wrong records
- **Archives at Yale people/56569 → LC n82045653 (Spirit)**: Wikidata's Yale ID is the Spirit agent (see section 2).
- **Encyclopedia of Surfing**: the 1876–1916 dates come from the Jack London entry loaded on the same page. Wikidata's ID `twain-mark` is correct.
- **The rest are expected and harmless**: relatives on Find a Grave (13), FamilySearch (15), WikiTree (13) and WeRelate (13); co-authors and editors on Goodreads (11) and Penguin Random House (Philip C. Stead); the Britannica article author (Thomas V. Quirk); and people in NARA's linked description records. None of these means a Wikidata ID is wrong.
- **Related, from the extraction notes**:
  - The Getty agent person/104WZ9 looks conflated with an obscure Plainfield, NJ photographer "Langhorne". This is a Getty data issue, but the Wikidata link should be checked.
  - VIAF clusters mis-include NKC jx20050822002 (Olivia Langdon Clemens) and a PLWABN Karłowicz record.

## 5. Extraction-noise patterns
- **Unresolved node URIs taken as values.** The pipeline repeatedly takes URIs and blank nodes as values instead of following them to the literal: ULAN birth/death activity URIs, RKD search-facet URLs and genids, GTAA label nodes, and WikiTree/JSON-LD `@type` ("Place").
- **Field labels and site chrome taken as values.** Examples: Stedelijk "Geslacht"/"Land", ISNI's "ISNI 0000 …" label, the Google Doodle site title, SVKKL "Detail záznamu", HAND's JSON-schema token "table", and AKL search-filter strings.
- **Language fields picked up from the wrong source.** The values come from the page or record locale (CineMagia "ro", Rekhta's UI locales, Kunstenpunt "nl", KANTO "fi") or from the ONIX of a translated book (CiNii "jpn").
- **Data about other entities taken as the subject's own.** The pipeline treats side-loaded records as facts about the subject: relatives' dates on Find a Grave, NARA ancestor and subject dates, and the Jack London record on the surfing site.
- **Crosslinks that are not same-as assertions:**
  - VIAF 996 entries (records VIAF keeps in other clusters) were turned into same-as links. This produced 16 DBC links to probably unrelated "Conte" records, so 996 should never be used.
  - ULAN `aggregations/*` resources were treated as identifiers.
  - Family, co-author and article-author links were treated as same-as.
  - A FAST value had "uri" glued onto the ID.
- **Normalization gaps that inflated the mismatch count:**
  - Slug suffixes (`1244.Mark_Twain`, `31611/mark-twain`), the `/id` suffix, the `person/` prefix and case differences (Filmportal) should be stripped before comparing IDs.
  - VIAF source-record URLs (`viaf/LC|n 79021164`) should be mapped to the source system, not to VIAF clusters.
  - Year-only dates, including the `YYYY-01-01` and `YYYY-12-31` placeholders, should count as matches at year precision.
  - Demonyms should map to the country (American, américain, Americký, statunitense, 美国人).
  - Coded vocabularies (lexvo, GeoNames, GND area codes, YSO, NLP descriptors) should be resolved to labels.

## Addendum: second pass (page-text sites and remaining items)

A second Opus pass judged the 411 disagreements that appeared after the page-text extraction (`llm_extractions_pages/`) and the "about the entity" gate were added (`review_batches_pages/`). Verdicts are appended to `review.json` with `pass: "pages"`.

| Verdict | Items |
|---|---|
| equivalent | 327 |
| extraction_noise | 65 |
| wikidata_gap_or_error | 9 |
| unclear | 5 |
| site_disagrees | 4 |
| different_entity | 1 |
| **total** | **411** |

### Wikidata gaps and errors (second pass)

- **ISFDB author ID (P1233)**, given_name: ISFDB gives the legal given names as 'Samuel Langhorne'. Wikidata has given names 'Samuel' and 'Mark', and puts 'Langhorne' under family name. Langhorne is his middle name, so Wikidata models it as a second given name. → *given name (P735): Langhorne (series ordinal 2), removed from family name (P734)*
- **National Library of Korea ID (P5034)**, occupation: '소설가' (novelist) and '작가' (writer) match Wikidata. '발명가' (inventor) is missing, yet Twain held three US patents, including 'Improvement in Adjustable and Detachable Straps for Garments' (US 121992, 1871), which the NARA record also shows. → *occupation (P106): inventor*
- **Rodovid ID (P1185)**, given_name: Rodovid gives the birth given names 'Samuel Langhorne'. Wikidata has 'Samuel' and 'Mark' and puts 'Langhorne' under family name, but Langhorne is a middle (given) name. This is the same issue as the ISFDB item 1046. → *given name (P735): Langhorne (series ordinal 2), removed from family name (P734)*
- **Münzkabinett ID (P13030)**, https://www.britishmuseum.org/collection/term/BIOG240173: Münzkabinett asserts exactMatch to British Museum term BIOG240173. No British Museum person or institution ID appears in Wikidata's identifiers for Q7245, so it is probably a missing identifier, though it should be checked on the BM page first. → *British Museum person or institution ID (P1711): BIOG240173*
- **CCAB ID (P1890)**, pseudonym: 'Jean Francois Alden' is a known Twain pseudonym with its own authority records, but Wikidata's pseudonym list (Mark Twain, Sieur Louis de Conte, Thomas Jefferson Snodgrass, Quintus Curtius Snodgrass, J. W. Bothwell) does not include it. → *Jean François Alden*
- **Archive Site Trinity College Cambridge ID (P8496)**, related_agent: The record's one family relationship, 'Clemens, Cyril (1902-1999) author, cousin of Samuel Clemens', is a real (distant) kinship Wikidata lacks; the other values (F.W.H. Myers as correspondent, letters by d'Arányi/Trevelyan and Pethick/Lawrence mentioning him) are archival subjects, not relations. → *relative (P1038): Cyril Clemens (1902-1999), distant cousin*
- **Bibliothèque nationale de France ID (P268)**, given_name: BnF gives forenames 'Samuel Langhorne'; Langhorne is his middle (given) name, but Wikidata lists 'Langhorne' under family name and only 'Samuel' (and 'Mark') as given names. → *given name (P735): Samuel, Langhorne (ordinal 2); remove 'Langhorne' from family name (P734)*
- **‎Darwin Correspondence ID (P14397)**, given_name: Given names 'Samuel Langhorne'; Langhorne is a middle (given) name, yet Wikidata records it as family name and lacks it as given name. → *given name (P735): Samuel, Langhorne (ordinal 2); remove 'Langhorne' from family name (P734)*
- **RPO poet ID (P5478)**, given_name: Facts table 'Given Name: Samuel Langhorne'; Langhorne is his middle name, which Wikidata wrongly has as a family name. → *given name (P735): Samuel, Langhorne (ordinal 2); remove 'Langhorne' from family name (P734)*

### Sites that disagree with Wikidata (second pass)

- **Encyclopedia of China (Third Edition) old ID (2021) (P10565)**, birth_date: The site gives '1835-11-31', an impossible date because November has 30 days, in both its header and infobox. It is a typo for Wikidata's correct 1835-11-30.
- **Filmportal ID (P2639)**, death_date: Filmportal gives "1910-02-21", but he died 21 April 1910 (Wikidata 1910-04-21). The month is wrong on the site.
- **Encyclopedia of China (Third Edition) ID (2026) (P14541)**, birth_date: The page prints the birth day as 31 November 1835, which is an invalid date, so only 1835-11 was kept. Year and month agree with Wikidata's 1835-11-30, but the printed day is wrong.
- **Enciclopédia Açoriana ID (P1385)**, death_date: The article gives the death date as '2.4.1910' (1910-04-02), but Wikidata and every authority have 1910-04-21. This is almost certainly a typo for 21.4.1910.

### Different entity / unclear (second pass)

- **CiNii Research ID (P11496)**, work [different_entity]: Most titles are his: Huckleberry Finn and Tom Sawyer in Japanese, 'Pudd'nhead Wilson ... Those extraordinary twins', 'Mark Twain's tales of the macabre & mysterious' and 'The illustrated Mark Twain and the Buffalo Express'. But 'James : a novel' is Percival Everett's 2024 novel, not a Twain work; it was picked up from related items. Pudd'nhead Wilson is missing from Wikidata.
- **GTAA ID (P1741)**, https://data.muziekschatten.nl/som/524a74d7e9016bdfd700366fde1d00ba [unclear]: This exactMatch to a Muziekschatten (Dutch music library) person URI is probably the same entity. It is unclear whether Wikidata has a property for this system, so a gap cannot be confirmed.
- **CoBiS author ID (P7865)**, related_agent [unclear]: Organisations from SPARQL fields: 'American Academy of Arts and Letters' (membroDi; true, he was a founding member) and 'Cascadilla School' (istruzione; doubtful, he had no schooling there). These are member-of/educated-at claims not covered by the supplied Wikidata data, so they cannot be settled here; Cascadilla School should be checked.
- **National Library of Spain SpMaBN ID (P950)**, work [unclear]: These are 12 bare datos.bne.es resource URIs (e.g. 'a4821154', 'bimo0002036040') linked via OP3005 (author of), with no titles. They are probably his BNE works or editions, but the titles cannot be checked from the data.
- **National Library of Spain SpMaBN ID (P950)**, related_agent [unclear]: These are 12 bare BNE person URIs (XX2258036 and others) via OP5001, with no names, so the nature of the relation cannot be judged. They are most likely co-authors or translators rather than relatives.
- **IdRef ID (P269)**, work [unclear]: 'http://www.idref.fr/033702462/id' is a bare IdRef URI linked via 'creator', with no title, so the work it denotes cannot be checked.

### Recurring observations from the reviewers

- **Works missing from Wikidata's work list**: every reviewer independently noted that sites list well-known works Wikidata does not link to Q7245 as works: *A Connecticut Yankee in King Arthur's Court*, *The Prince and the Pauper*, *Life on the Mississippi*, *The Innocents Abroad*, *A Tramp Abroad*, *Roughing It*, *Pudd'nhead Wilson*, *Personal Recollections of Joan of Arc*, *What Is Man?*, *King Leopold's Soliloquy*. The work list on Wikidata is partial by design, so these were judged `equivalent`, but the gap is consistent.
- **"Langhorne" modelling**: five sites (ISFDB, Rodovid, BnF, Darwin Correspondence, RPO; also DBNL and others judged equivalent) give "Samuel Langhorne" as given names, while Wikidata files Langhorne under family name (P734). Same finding as the first pass.
- **Identifier list given to reviewers was incomplete** (no BnF, BIBSYS, Libraries Australia...). Any identifier gap a reviewer flagged was re-checked against `identifiers.json` at merge time; false gaps were re-verdicted `equivalent` and annotated.
- **Wrong identifier on Wikidata**: Biblioteca di Santa Sabina ID (P9522) resolves to "Muguet, Christian", not Twain (found by the page-text extraction, not a review item).
- **Site typos**: three sites print impossible or wrong dates for him (Encyclopedia of China 1835-11-31 twice; Enciclopédia Açoriana 2.4.1910; Filmportal 1910-02-21).

## Addendum: third pass (re-crawled and restored sites)

A third Opus pass judged the 69 disagreements that appeared after the trust-audit re-crawl (archived snapshots, resolved redirectors, Yale LUX's Linked Art record, the feb-web frame) and after profiles were restored for page-text sites that had no representation file at all (BIBSYS, az.lib.ru, Online Books Page, SFE, Roglo, gravsted.dk...). Verdicts are in `review.json` with `pass: "recrawl"`.

| Verdict | Items |
|---|---|
| equivalent | 57 |
| extraction_noise | 8 |
| unclear | 2 |
| site_disagrees | 1 |
| wikidata_gap_or_error | 1 |
| **total** | **69** |

### Wikidata gaps and errors (third pass)

- **CANTIC (P9984), name_variant "Alden, Jean François, 1835-1910"** — his pseudonym for *Personal Recollections of Joan of Arc* (CCAB has the same form); Wikidata has no alias or pseudonym statement for it. Same gap the second pass found on other catalogues.

### Sites that disagree with Wikidata (third pass)

- **Roglo (P7929), birth_place "Hannibal, Marion Co., Missouri"** — he was born in Florida, Monroe County, Missouri; the family moved to Hannibal in 1839. Roglo has his boyhood home as his birthplace.

### Unclear (third pass)

- **Yale LUX (P13591) same-as `id.loc.gov/authorities/names/n82045653`** — the reviewer could not place it; a follow-up lookup on id.loc.gov shows it is the LC heading *Twain, Mark, 1835-1910 (Spirit)*, used for books channelled through a medium. Re-verdicted `different_entity`: LUX has folded the spirit heading into his record, and Wikidata is right to omit it.
- **Yale LUX related_agent** — a group membership whose label LUX did not resolve.

### Recurring observations (third pass)

- Yale LUX's own display label for the record is "Clemens, Smauel Langhorne, 1835-1910" (typo in the source); its 21 `equivalent` links are the richest cross-link set of any site after VIAF.
- "Langhorne" is modelled as a family name on Wikidata; sites that give the given name as "Samuel Langhorne" (SFE, Roglo) were marked equivalent.
- Works still missing from Wikidata's notable-work list, confirmed again: *A Connecticut Yankee in King Arthur's Court*, *The Innocents Abroad*, *Roughing It*, *Personal Recollections of Joan of Arc*.
- The eight extraction-noise items are related-agent lists made of translators, illustrators, editors and performers; two genuine relations sit among them (Charles Dudley Warner, co-author of *The Gilded Age*; William Dean Howells, close friend).

## Addendum: fourth pass (page text read for every resolved site)

After the Ben Yehuda finding (six Hebrew editions with their translators, invisible to the site's structured data) the Opus page-text pass was run over all 167 resolved sites that already had structured data (`llm_batches_pages/batch_10..18`). That added 8,229 page-text values to 17,786 in total and 295 new disagreements, judged here; verdicts are in `review.json` with `pass: "fulltext"`.

| Verdict | Items |
|---|---|
| equivalent | 233 |
| extraction_noise | 48 |
| different_entity | 5 |
| wikidata_gap_or_error | 4 |
| unclear | 3 |
| site_disagrees | 2 |
| **total** | **295** |

### Wikidata gaps and errors (fourth pass)

- **Two Wikidata identifiers point at the "Twain, Mark (Spirit)" headings** that libraries use for books channelled through a medium: ISNI `0000000077209145` (P213; the ISNI record's only title is *Mark Twain returns*, c1982) and Archives at Yale `people/56569` (P8902; heading "Twain, Mark, (Spirit), 1835-1910", found only in the Charles H. Hapgood Papers - his real Yale record is `people/87456`, which Wikidata also holds). Both verified on the saved pages. They should come off Q7245, or be qualified. The LC heading n82045653 is the same case and is not on Wikidata.
- **"Langhorne" is a given name, not a family name** (GeneaStar, BHCL, and the same pattern on SFE, Roglo, Slovak NL): Wikidata has given names Samuel and Mark and lists Langhorne under family name.
- **CiNii Research** links two further NACSIS-CAT author ids (DA03513635, DA04621156) to his page; Wikidata holds DA00300263 only. Probably his real-name or pseudonym records; check before adding.
- Works missing from Wikidata's notable-work list, seen again on Larousse, LTit, Wellcome and WorldCat: *The Innocents Abroad*, *Roughing It*, *Life on the Mississippi*, *The Prince and the Pauper*, *A Connecticut Yankee in King Arthur's Court*.

### Sites that disagree with Wikidata (fourth pass)

- **National Library of Israel (P8189)** links the English form of his birthplace to Florida, Montgomery County, New York; its Hebrew form says Florida, Missouri. A mis-linked place authority.
- **Kinobox (P12098)** gives both dates one day early (29.11.1835, 20.4.1910); a timezone or off-by-one display error.
- **Wien Geschichte Wiki (P7842)** gives the death date as 12 May 1910 and the NLI Hebrew note as 12.4.1910 (both wrong; 21 April 1910). Flagged by the extraction agents; the date items themselves were judged in this pass where they surfaced.
- **Tebeosfera** puts Redding in New Haven County (it is Fairfield County). Marked equivalent because the town is right.

### Different entity (fourth pass)

- Links to LC n82045653 (Lebanese NL, Slovak NL clusters) - the Spirit heading.
- ISNI 0000000077209145's work list and the SNAC ark taken from Archives at Yale people/56569 - both Spirit records, see above.
- The Getty record "Langhorne" conflates Twain with a photographer from Plainfield, New Jersey (the extraction kept only the Twain parts).

### Recurring observations (fourth pass)

- The extraction-noise items are almost all co-contributor lists (translators, illustrators, audiobook readers, editors, photographers, article authors) read off work lists; two genuine collaborators recur in them, Charles Dudley Warner (co-author of *The Gilded Age*) and Albert Bigelow Paine (biographer).
- VIAF-style pages (national libraries served through VIAF's processed view) carry 40-50 cluster links each; all resolve to real records of his and most match identifiers Wikidata already holds, often under a different number form (NSK 000047578 vs 981005677060509366, BNE 981060902239808606 vs XX945992).
- Several reviewers noted that `wikidata_identifiers` in the context file is incomplete, so no cross-link was called a Wikidata gap on absence from that list alone.

### Follow-up (LC panels, MARC-in-JSON, unread data files)

After the LC Authorities finding, step 4 now follows paginated XHR JSON (LC's "Subject Of Works" 433 and "Contributor To Works" 1,530 entries were previously captured as page 0 only and then dropped by the JSON profiler), step 6 parses MARC serialised as JSON (13 VIAF-served sites and IdRef's UNIMARC export) deterministically, and a new element `subject_of` holds works *about* him (LC, NTA, KANTO). An Opus pass read the six data files no earlier pass had opened (KulturNav, Polish National Library works/manifestations, NL Korea JSON-LD, KANTO, CANTIC). The four disagreements this produced were all judged equivalent or noise (MARC 500 see-also headings are his own pseudonym records; KulturNav's cataloguing language is not his language).

## Independent audit of every identifier (round 1)

Sixteen Opus auditors looked at all 315 identifiers end to end (Wikidata value, crawled page, captured values, atlas labels) and asked whether the atlas tells the truth about each. Verdicts in `audit/verdicts_*.json`, shown per tile on the atlas.

| Verdict | Sites |
|---|---|
| sound | 146 |
| mislabelled | 119 |
| unreachable | 26 |
| incomplete | 21 |
| wrong_record | 3 |

### What the audit found, and what was changed

- **Page chrome counted as his data** (the largest class, ~90 sites): site taglines in `og:description`, logos in `og:image`, site-wide JSON-LD nodes (WebSite, Organization, BreadcrumbList, VideoObject, FAQ), vocabulary classes expanded from JSON-LD contexts (`CompoundLiteral`, `isDefinedBy`), ad-player and consent-banner payloads (jwplayer posters, prebid bidders, cookie-banner language `en`), the crawler's own geolocation stored as nationality (`US` on ČSFD, FamilySearch, NL Wales), Primo interface settings, and relatives' names and dates filed under his own on genealogy sites. These inflated value counts, decided the format family ("RDF" resting on a WebSite node) and pushed sites into the "mostly unique" bucket. Fix: values are taken only from JSON objects that are about him (a name-bearing object must carry one of his labels in full), site/ad/vocabulary nodes are never chosen as the RDF focus, OpenGraph is kept only when the card names him, and format/access labels rest on descriptive values only.
- **False login walls** (~17 Koha, Primo, Alvin, HAND, Geni, Find a Grave pages): a "Log in" link made a fully rendered record count as unresolved. Fix: such pages are `ok` with a note.
- **VIAF-served national libraries** (UAE, Ireland, RILM, Canadiana, ELNET): the HTML shell was blank, so the site read as `wrong_page` although the full MARC record came back through VIAF's JSON. Fix: a page whose record arrived through the site's data endpoint is resolved, with a note.
- **"(Spirit)" headings**: ISNI 0000000077209145 and Archives at Yale people/56569 (both on Wikidata) are the library heading for books channelled through a medium. Now `wrong_page` with that reason; Open Plaques 1709 (James Wallace Richard Hall) and Santa Sabina 10370 (Christian Muguet) are `record for a different person`.
- **Dead identifiers**: VIAF "Processed record not found" (Libraries Australia, Iceland, one ELNET, one RERO, one NTA value) was read as a bot challenge; now `http_error` "record not found".
- **Getty's "Langhorne" record** conflates him with a photographer, and 393 of its values were labels of linked concept records; the Linked Art walker now only follows actor-typed nodes (506 → 64 values). ULAN/Getty year-only dates were padded to 1 January; now the year.
- **SNAC's 935 "works"** are archival collections that reference him; they are now `subject_of`, which still makes SNAC the most "unique" site - honestly so, since nobody else lists where his papers are.
- **VIAF 996 fields** (records VIAF did *not* cluster with him) had been read as cross-links on archived VIAF pages; dropped.
- **Still open, documented as limits**: JS "load more" lists and collapsed sections (LibriVox's 270 recordings, IMSLP's "[36 more]", CoBiS, nooSFere tabs, Discogs/Open Library/Harper's pagination), records one click behind a results list (RSL, NUKAT), holdings counts (FES, Kallías, BnF), structured exports the crawl never advertised (BNMM MARC, NLW/Turnbull EAC-CPF, FactGrid's Wikibase API, BnF's data.bnf.fr), and Chrome's auto-translate rewriting some Chinese and German pages before capture (NLC, Perlentaucher, Klexikon).
- **Wikidata values the audit calls wrong or stale**: ISNI and Archives at Yale Spirit records; Santa Sabina 10370; Open Plaques 1709; NTA p227880145, ELNET a11300425, RERO A010034463, Hoopla, Cultureel Woordenboek, Brockhaus "mark-twain" (dead); CiNii 1140000791666601344, Itaú pessoa407320, SNAC w65h7dgf (superseded); P691 duplicate value; FAST 1986616, CiNii DA03513635/DA04621156, a second de Conte ISNI and a Bothwell VIAF cluster that Wikidata lacks; Canadiana's formatter URL drops the `|` separator.
- **Site errors seen by the auditors**: Vienna History Wiki (death 12 May 1910), Kinobox (both dates a day early), Filmportal (21 Feb 1910), Açoriana (2.4.1910), NL Greece (1910-04-10), NLI (Florida, NY), Roglo and Angelicum (Hannibal as birthplace), Encyclopedia of China (1835-11-31), Treccani (Tom Sawyer 1867), Gran Enciclopèdia Catalana / Enciclopedia Galega (Huck Finn 1882), Parsifal ("Lanhorne"), LUX ("Smauel"), BookBrainz (Oliver Twist), NILF ("Dixon Wecter" as an alias), Arab Encyclopedia (river boatman with his father), Comic Vine ("Longhorne").

## Audit round 2 (the 143 sites round 1 did not call sound, re-judged after the fixes)

| Verdict | Sites |
|---|---|
| mislabelled | 76 |
| sound | 39 |
| incomplete | 23 |
| wrong_record | 3 |
| unreachable | 2 |

Round 2 confirmed the login-wall, VIAF-shell, Spirit, vocabulary and ad-payload fixes and listed what the first fix round had missed; a third round of changes followed: in-page JSON-LD counts as *embedded markup* and only data from a link, content negotiation, export or XHR counts as *RDF* / *ad-hoc JSON*; MARC-as-JSON is a *library format*; "(Spirit)" headings and VIAF non-matches are dropped from page-text merges as well; pages judged `wrong_page` contribute nothing to their property's profile (step 6 is re-run after step 8); site logos, placeholder images, schema type names used as places, and bare URIs no longer count as descriptive values; organisation-, page-, book- and album-typed nodes are never the RDF focus and a stray Person node (an article's author) is not taken for him; record titles inside record-like JSON objects (a photo, a census entry, a patent) go to `subject_of` instead of his name; CAPTCHA and obfuscated renders read as challenges; login-box pages that show a catalogue record are `ok` even when short; a multi-value property's page whose heading is somebody else is `wrong_page` (Open Plaques 1709). Six newly recognised record pages got their page-text pass.

Known remaining limits (not fixable from the saved crawl): JS "load more" lists and collapsed sections, paginated discographies and tag archives beyond page 1, records one click behind a results list (RSL, NUKAT), holdings counts, structured exports the pages advertise only as buttons (BNMM MARC, Turnbull/NLW EAC-CPF, FactGrid's API, BnF's RDF, RERO's MARC-JSON on the non-/en/ path), Chrome auto-translation of some Chinese and German pages, and sites that proxy Wikidata's or Wikipedia's own data (BookBrainz, SNK, CoBiS, the Polish National Library's "Wikidane" block), which count as agreement with Wikidata although they are not independent.


## Addendum: comparison rules tightened (2026-10-20)

The "Agreement with Wikidata" facet had flagged 177 sites as "mismatch somewhere". Reading the ten worst showed the comparison was too literal:
demonyms in other languages (estadounidense, statunitense, americký) were held against the English label "United States"; coarser places
(Missouri, Connecticut, United States) against the village and town; inflected occupations (Συγγραφείς) against singular labels; and
anything Wikidata lacks - a pseudonym, an occupation, a work, a relative, a language - was counted as a contradiction.

`compare_wikidata.py` now fetches each nationality item's demonyms (P1549) and each place item's containing places (P131 chain, P17),
compares every name element against the pool of all his Wikidata name forms, stem-matches occupations and nationality adjectives, and treats
occupation, language, work, related_agent, pseudonym, name_variant, field_of_activity and activity_place as additive: a non-match there is
`no_overlap`, never `mismatch`. Only dates, places, gender, nationality, the preferred name and given/family names can still mismatch.

Result: 11 mismatching site×element rows across 11 sites. Real disagreements: Enciclopédia Açoriana death 1910-04-02, Filmportal 1910-02-21,
Vienna History Wiki 1910-05-12, Kinobox 1910-04-20, Encyclopedia of China birth 1835-11-31 (an impossible date), DBNL "Missiouri", Media Arts
Database "TwainMark". Leftover false positives, left as they are: Freebase "Stormfield" (his house in Redding, finer than Wikidata, not wrong),
and three non-Latin spellings of Redding/Connecticut/American (Armenian, Arabic, Lebanese) that differ from Wikidata's transliterations.

## Addendum: the unique-vs-repeated measure audited (2026-10-20)

Checked `quality_report.py`'s unique share against the data. Four faults, all fixed:

1. **Duplicates counted as values.** A label repeated in five files of one site counted five times (8% of all descriptive values;
   WorldCat Entities had "Mark Twain" 94 times). Now distinct per site.
2. **Names compared only within their element.** "Mark Twain" as `name_preferred` on one site and `name_variant` on another counted as
   unique on both (80 such values). Name elements are now pooled, and word order ignored.
3. **Wikidata ignored.** 191 values no other site stated were on Wikidata (Korean, Armenian and Greek name forms, mostly), yet counted as
   unique information. Wikidata now counts as one more source.
4. **Annotations made everything unique.** The page-text pass writes "Orban, Jean-Pierre (translator of …)" and headings carry ", 1835-1910";
   those never matched a plain "Jean-Pierre Orban". Parentheticals and trailing life dates are stripped for the comparison; dates are
   compared digits-only.

And one design flaw: holdings lists dominated the ratio, so Library of Congress (783 works) and SNAC (932 archival collections about him)
scored 0.86 and 0.95 and read as "most unique". Each element now weighs at most 50 distinct values in the share. SNAC stays high because
its related agents and archival subjects are genuinely found nowhere else; Library of Congress drops to 0.56.

Buckets moved from 35 mostly unique / 105 mixed / 125 mostly repeated to 20 / 89 / 153; 50 sites changed bucket. Largest drops: National
Library of Korea 0.77 → 0.32, Open Library subject 0.64 → 0.21, Union Catalog of Armenian Libraries 0.74 → 0.43, Library of Congress
0.86 → 0.56. Two value-level problems noted but not changed: Flemish Public Libraries lists "Sawyer, Tom" and "Huckleberry, Finn" as related
agents (the MARC-JSON page-text pass read subject headings for his characters as people), and Greek or Italian edition titles are unique by
language rather than by content, which the measure cannot tell apart.

## Addendum: from "unique" to "useful beyond Wikidata" (2026-10-20)

A share cannot rank sites by what a reader gains: one unique relative and 700 unique works are the same ratio. The atlas facet is now a
score: for each element, the distinct values Wikidata does not hold (labels, aliases, demonyms and containing places in every language count
as held; a year or year-month counts as held when Wikidata has the full date), log2(1 + n), weighted - works, works about him and
relatives 1.5; name forms, occupations, fields, places 1; descriptions, languages, gender, nationality 0.5. Buckets: rich ≥ 20 (23 sites),
substantial 10–20 (94), modest 4–10 (90), thin < 4 (59), nothing beyond Wikidata (49). Top: Library of Congress 46 (700 works, 345 works
about him), SNAC 43 (927 archival collections about him, 384 correspondents), VIAF 37, Geni 36, Slovak National Library 27, GND 27.
The score inherits any junk the profiler let through (a character read as a relative counts), and "not on Wikidata" is a snapshot.
The unique share stays in each tile's Volume row as a redundancy signal.

## Addendum: the access facet re-measured with curl (2026-10-20)

The atlas had said 221 sites were open to "HTTP (cURL)". That rested on fetches made with a Python client sending an identifying
User-Agent, and on a page probe that took any HTTP 200 as success. Tested with the curl binary itself (`probe_clients.py`: the page and
the data files his values came from, three client profiles in turn, no cookies, no JavaScript, "served" = 200 with his name in the body):

| class | sites |
|---|---|
| plain curl gets the record | 168 |
| needs an identifying User-Agent | 6 |
| needs browser headers (Chrome User-Agent, Accept, Sec-Fetch) | 4 |
| served 200 but the record needs JavaScript (application shell) | 46 |
| refuses every non-browser client (403, challenge, no reply) | 59 |
| nothing to get | 32 |

So 178 sites, not 221, hand a non-browser client his record, and 168 of those to curl with no headers at all. The JavaScript-shell class
holds the VIAF-hosted libraries (the VIAF page is a single-page app and its record API is a POST), SNAC, Trove, Geni, MusicBrainz and the
Primo and Koha OPACs; the refusals are Cloudflare- and Akamai-fronted sites (IMDb, Britannica, Discogs, Quora, Find a Grave, FilmAffinity),
VIAF's own cluster page and isni.org. Open Library rate-limits by address: after the first run's six parallel requests it answered a
"verify_human" redirect and then timed out, even to a single slow retry, so it stands as a refusal for this address on this day. Two caveats: a 200 "shell" verdict can also be a page that names him only
after a client-side fetch the probe cannot follow, and results are a snapshot of one day's bot rules.

## Addendum: content negotiation surveyed (2026-10-21)

`probe_conneg.py` sent five Accept headers (ld+json, json, turtle, rdf+xml, n-triples) with an identifying User-Agent to every
identifier URL and to the data URLs the values came from, sniffing the body for what it really is and for his name. 62 sites hand back
some non-HTML representation of him to an Accept header; after discounting JSON endpoints that answer JSON to every header (not
negotiation), 23 sites negotiate RDF (JSON-LD, Turtle, RDF/XML or N-Triples) and 13 only JSON. On the identifier URL itself: json 32,
ld+json 18, rdf+xml 16, turtle 10, n-triples 8. Seven sites honour n-triples (ULAN, RKD, NTA, GTAA, Japan Search, Getty, JudaicaLink).
Many servers answer a format they were not asked for - 'turtle' or 'n-triples' returning JSON (20 each), 'ld+json' returning RDF/XML
(8) - so the sniffed format, not the Accept header, is what the atlas reports. The VIAF-hosted libraries answer application/json with
VIAF's MARC-in-JSON on the page URL. LUX serves its Linked Art JSON-LD regardless of header, with no alternates (checked separately).
