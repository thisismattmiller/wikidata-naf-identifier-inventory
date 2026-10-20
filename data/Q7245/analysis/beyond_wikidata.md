# Q7245 (Mark Twain): what the linked sites offer beyond Wikidata

Scope: 277 external-identifier sites linked from Q7245, of which 202 returned usable data. Wikidata was read from `entity.json` (all statements, not only the schema elements), so a fact counts as missing only when the item really lacks it. Wrong or missing identifiers are covered in `review.md` and are only referenced here. Inputs: `beyond_wikidata_input.json`, `profiles/*.json`, and the raw files under `representations/`.

## 1. Summary

- **Name forms.** About 400 distinct name strings on the sites are not Wikidata labels or aliases. Most come from the authority cluster: LC NAF, GND, VIAF, ISNI, FAST, Archives at Yale, Kalliope and JudaicaLink. They are transliterations ("Make Tuwen", "Tʻu-wen, Ma-kʻo", "Makū Touen", "Tuėĭn, Mark"), national forms ("Marek Twain", "Marc Twain", "Marks Tvēns", "Markas Tvainas"), Hebrew and Yiddish spellings, the real name in Chinese and Arabic script, and the unrecorded pseudonym **Jean François Alden**.
- **Archival holdings.** This is the largest category Wikidata does not cover. SNAC links 1,010 archival resources (495 "creatorOf" and 516 "referencedIn") from 168 finding aids in about 35 repositories. It also lists 783 related agents, 40 of them marked "correspondedWith". Wikidata's P485 (archives at) names only 3 repositories.
- **Bibliographic and work data.** NLK links 1,346 bibliographic records, CiNii 2,006 related books and Douban 196 titles. VIAF and the VIAF-derived national files list 20–40 titles each, and GND lists 20 publications. MusicBrainz has 60 audiobook and radio-play releases, and the film sites list screen adaptations. Wikidata's P800 (notable work) holds only 2 works.
- **Cataloguing evidence.** "Found in" (670/810) citations come from LC, NLI, BAnQ, the National Library of Lithuania (NLL), SBN, IdRef, BNE, NSK and NARA. Each cites a title-page form ("Przygody Huck'a, 1912: t.p. (Marek Twain)") or a reference work (DAB 1930, БСЭ 1976). Wikidata could use these as references for aliases and pseudonyms, or as P1343 (described by source).
- **Personal facts Wikidata lacks.** Occupations: publisher, businessman, inventor, typesetter, miner, satirist and essayist. Places: Hannibal, Virginia City, San Francisco, Buffalo, Elmira and Hartford as residence or work places (P551 now holds only two buildings). Family: a fourth child, Langdon Clemens (1870–1872), and siblings Henry, Margaret, Benjamin and Pleasant Hannibal. Other: the LC classification PS1300–PS1348 (P1149), an Oxford honorary degree (ULAN), height 1.75 m (Dimensions.com) and descriptions in about 12 more languages.
- **Out of scope for Wikidata.** Census transcriptions, record-administration metadata, usage counts, crowd personality typing and finding-aid paths.
- **Richest sites.** SNAC; LC NAF (with FAST); GND (with Kalliope); VIAF and its VIAF-derived national copies (UAE University, NLI, LAC, BAnQ, the Slovak National Library, NLL); BNE; ISNI; the genealogy sites (FamilySearch, Find a Grave, Geni, WikiTree); Open Library; museum-digital (Wikipedia leads in 35 languages); NLK; CiNii/Douban for East Asian bibliography.
- **Noise.** About a third of the raw "extra" values are noise: other entries loaded on the same page (Encyclopedia of Surfing, the Personality Database Tolstoy record), relatives' data counted as Twain's, ad-network hosts taken as "sources", VIAF 996 non-matches, the conflated Getty record and site logos taken as "images". These are excluded below.

## 2. Values Wikidata lacks for elements it models

### 2.1 Name forms (labels and aliases)

Wikidata has 88 labels and 65 aliases. After normalising (dropping the dates, un-inverting headings, ignoring punctuation), about 400 site name strings remain that Wikidata lacks. Roughly 150 are real name forms. The rest are noise: relatives' names, book titles, field labels ("value", "isDefinedBy"), MARC fragments ("20151019xitaa50 ba0") and glued names.

| Kind | Examples (sites) | Wikidata fit |
|---|---|---|
| National Latin-script forms used on title pages | **"Marek Twain"** (14 sites: LC, GND, FAST, ISNI, VIAF, NLP, Yale; LC 670 cites *Przygody Huck'a*, 1912); **"Marc Twain"** (11: IdRef, GND, Open Library, NSK, NLP); "Markas Tvainas", "Morkas Tvėnas", "Markas Twainas" (NLL, which cites 1904–1996 title pages); "Marks Tvēns", "Marks Twens" (GND, Latvian forms); "Mark Tvejn", "Marka Tvèn" (NLP) | Aliases in pl, fr, lt, lv. These are attested in print, so they are safe. |
| Real name and variant spellings | "Samuel Langhorn Clemens" (GND, VIAF, LTit); "S. L. Clemens", "Clemens, S. L." (ISNI, GND); "Mark Twain Clemens" (VIAF, ISNI, Getty) | "Samuel L. Clemens" is already a mul alias. "Langhorn" is a cataloguing variant, so it is optional. |
| Real name in other scripts | Chinese 萨缪尔·兰亨·克莱门 (Douban, Zhihu); Arabic صامويل لانغهورن كليمنز (Arab Encyclopedia); Hebrew סמואל קלמנס (LC, ISNI, VIAF); Latvian "Semjuels Klemenss" (SNAC, VIAF) | Aliases in zh, ar, he and lv. The zh form differs from Wikidata's 塞姆·朗赫恩·克列門斯. |
| Hebrew and Yiddish spellings | מרק טוויין, מרק טווין, מארק טווען, מארק טװײן, מרק טבןַ (Yale, ISNI, LC, UAE, VIAF; LC 670 cites Hebrew and Yiddish Wikipedia and NLI NAF, viewed 24 July 2026) | Add to he aliases. The Yiddish forms (טװ…) go in yi, which currently has only a label. |
| Other scripts | Bengali মার্ক টোয়েইন (VIAF, WorldCat Entities, museum-digital); Persian مارک تواين (LC, ISNI; written with Arabic yeh, so it differs from Wikidata's fa label); Korean 마아크 트웨인, 마커 투원, 마극 토온 (NLK, VIAF; older Korean renderings); Greek Μαρκ Τουεϊν (Piraeus Bank Library); Japanese hiragana まーく・とうぇいん (Japan Search) | Aliases in bn, fa, ko, el and ja. The Korean and Greek forms are low-risk. |
| Library romanizations of non-Latin headings | "Make Tuwen", "Tuwen, Make" (pinyin, 14 sites); "Tʻu-wen, Ma-kʻo", "Ma-k`o T`u-wen" (Wade-Giles); "Makū Touen", "Māku Towein" (Japanese, Hepburn-style); "Make Teviin" (Mongolian; on a 1985 title page per LC 670); "Tuėĭn, Mark", "Tvėn, Mark", "Klemens, Sami︠u︡ėlʹ" (ALA-LC Russian); "Twayn/Tuwayn/Tvāyn, Mārk" (Arabic/Persian); "Mak'ŭ T'ŭwein" (Korean); "Mārka Ṭoẏena" (Bengali); "Marḳ Ṭṿen" (Hebrew); "Kʻo-lan-man-ssu, Sai-mi-erh Lang-en" (Chinese, real name) | Usually *not* added as aliases, because they are search keys rather than names in use. Exception: "Make Teviin", which LC cites from a Latin-script colophon. |
| Pseudonym headings with dates | "Snodgrass, Quintus Curtius, 1835-1910"; "Conte, Louis de, 1835-1910"; "Bothwell, J. W., 1835-1910" (LC, GND, VIAF, NLI, UAE) | Wikidata already holds these names as P742 values. The dated heading is a cataloguing artefact. |
| Pseudonym "Jean François Alden" | Santa Croce (400), NLI and UAE (500), NSK, GND, ISNI, NLP, VIAF; LC 667: "Pseudonym not established: Jean François Alden"; LC 670: *Personal recollections of Joan of Arc*, 1923, t.p. (the Sieur Louis de Conte; Jean François Alden) | **Add to P742 and as an alias.** Already flagged in `review.md`. |
| "SLC", "Josh" | CineMagia gives "SLC" as a pseudonym. FamilySearch has "Josh Clemens". | "SLC" is his signature initials, not a pen name, so skip it. "Josh" was a real early pen name (1862 letters) but no site gives it cleanly; check a reliable source before adding. |

Noise excluded: ISNI's "ISNI 0000 0001 …" labels, the Getty and ULAN "Mark (pseudonym) Twain", VIAF title strings taken as names ("Autobiography of Mark Twain 3"), the J9U MARC-key strings, and relatives' names from the genealogy sites.

### 2.2 Occupations

Wikidata has 16 P106 values: journalist, novelist, autobiographer, teacher, humorist, children's writer, travel writer, aphorist, science fiction writer, writer, prose writer, opinion journalist, printer, maritime pilot, soldier and lecturer. Site values were judged as follows.

| Verdict | Value (sites) |
|---|---|
| **Real addition** | **publisher** (SNAC "Publishers", NLL "leidėjas", Gutenberg-DE "Verleger", museum-digital, Comic Vine/Fandom/Google Arts/PDB from the Wikipedia lead, Find a Grave; he ran Charles L. Webster & Co.); **businessman / entrepreneur** (NLL "verslininkas", museum-digital, Google Arts, Find a Grave); **inventor** (NARA: patent 121992 "Improvement in Adjustable and Detachable Straps for Garments"; NLK 발명가) |
| Plausible, more specific | **typesetter** (Geni, BookBrainz, Douban 排字工人, Gutenberg-DE "Schriftsetzer"; narrower than printer); **miner / silver prospector** (BookBrainz "miner", Gutenberg-DE "Silbersucher", Nevada 1861–62); **satirist** (Geni; Czech and Slovak "satirik"/"satirici" in NKC-derived BHCL, Provenio, SNK and SNL); **essayist** (BookBrainz, Babelio); draughtsman (Artists of the World (AKL), see `review.md`; low priority) |
| Already covered (translation) | Lotse, elvelos, 水手 → maritime pilot; 演说家, speaker, Redner → lecturer; reporter → journalist; pedagogas → teacher; prozaik → prose writer |
| Noise | Film-credit roles: Actor, Additional Crew, Director, Screenwriter, Producer, "Characters", "Thanks" (IMDb, TMDB, Sinemalar, PORT, CineMagia). These come from adaptations and the 1909 Edison footage. Also Getty "Photographer" (a conflated record), AKL facet labels ("Occupation", "10472") and unresolved URIs (Europeana concepts, KANTO, Carnegie Hall role 946). |

GND also marks "Schriftsteller" as the *characteristic* occupation (550 $4 berc) and the others as plain "Beruf". Wikidata can express this only through statement rank.

### 2.3 Places

- **Residence and work places (P551 / P937).** Wikidata's P551 holds only *Mark Twain House* and *Mark Twain Birthplace State Historic Site*, which are buildings, and the item has no P937. Sites name the towns: **Hannibal** (LC and FAST 370 "associated place", NLI, UAE, Geni, De Agostini, CineMagia, Store norske leksikon (SNL), BookBrainz, museum-digital); **St. Louis**, **Keokuk** and **Cincinnati** (Geni, De Agostini, CineMagia; printer years); **Virginia City / Nevada** (SNL, BookBrainz, Online Nevada Encyclopedia, museum-digital); **San Francisco** (SNL, De Agostini, Gutenberg-DE); **Hawaii** (SNL, Gutenberg-DE; SNAC adds Haleakala and Haiku); **Buffalo** and **Elmira** (Geni); **Hartford** (Geni, CineMagia, SNL, SNAC); **New York** and **Philadelphia** (Gutenberg-DE, De Agostini). Hannibal (residence 1839–1853), Virginia City and San Francisco (work 1862–1866), Buffalo (1869–1871) and Hartford (1871–1891) are safe additions with dates.
- SNAC's 36 "places" are geographic subjects of archival material (Heidelberg, Florence, Venice, Baden-Baden, St Petersburg, the Swiss Alps). They mostly reflect his travels and are not residences, so they are not P551 material.
- **Birthplace hierarchy.** BNE: "Estados Unidos, Missouri (Estado), Monroe (Condado), Florida". Find a Grave: "Florida, Monroe County, Missouri, USA". MusicBrainz: Monroe County. FamilySearch gives coordinates 39.4931, −91.7869. All of this is already implied by Wikidata's Florida (Q537803) item, so nothing needs to change on Q7245.
- **Burial.** Find a Grave gives Woodlawn Cemetery, Elmira (cemetery 66781, 42.1063, −76.8255) and describes the 12-foot monument erected by Clara. Wikidata already has P119 Woodlawn Cemetery and a P1442 grave image.

### 2.4 Dates

Sites add nothing usable beyond Wikidata's day-precision dates. GND 548 has the note "Todestag auch 21.02.1910" (a variant death date also recorded); this is a cataloguing footnote, not evidence. Wien Geschichte Wiki's 12 May 1910 is wrong (see `review.md`).

### 2.5 Descriptions

- Wikidata has descriptions in 71 languages; the English one is "American author and humorist (1835–1910)".
- **Languages Wikidata lacks:**
  - **da** (museum-digital, Lex.dk's Den Store Danske)
  - **nb/no** (SNL: "Mark Twain var en populær amerikansk forfatter …"; Geni)
  - **tr** (Sinemalar, Foto Atlas: "Amerikalı mizahçı, satirist, roman yazarı …")
  - **et** (ELNET: "Ameerika kirjanik ja ajakirjanik, kasutas kirjatöödes pseudonüümi.")
  - **lt** (NLL: "Rašytojas, humoristas, leidėjas, verslininkas, pedagogas")
  - **vi, th, ta, ur, tl, sw** (museum-digital, which copies Wikipedia leads dated 11.08.2021)
- **Long biographies, compared with Wikidata's one-liner:**
  - SNAC biogHist, the Find a Grave memorial bio, Geni (three user-written "About" texts with census transcriptions), Douban (zh), CiNii/openBD (ja), Arab Encyclopedia (ar), De Agostini (full Italian entry), SNL (full article), Gutenberg-DE (de), Larousse and Universalis (fr), Portal da Literatura (pt), CineMagia (ro; contains factual errors), PORT (hu), FantLab (ru), CBDB (cs), Klexikon (children's German), BookBub, Poets.org, PRH, IMDb mini-bio.
  - Most of these restate Wikipedia. The independent ones are ANB, Grove (both paywalled) and Britannica.
- Not descriptions (noise): BnF, Evene, openMLOL and Cultureel Woordenboek boilerplate; the Encyclopedia of Surfing paragraphs about Jack London; and PDB's Tolstoy text.

### 2.6 Works

Wikidata has only 2 P800 values, though separate work items exist with P50 (author). Sites offer the following.

**Published works and editions:**
- VIAF (20 work clusters with URIs)
- The VIAF-derived national copies, each with 910/912 title strings: LAC (Library and Archives Canada) and the Slovak National Library 40, Flemish Public Libraries 40 (Dutch translations), NLI 37, BAnQ 34, NLL 10
- GND (20 titles, plus 20 MARC 672 title fields)
- Gutenberg-DE (34 German translations)
- Project Gutenberg (21 on the first feed page of 25)
- Open Library (20)
- BNE (12 work resources)
- NLK (1,346 linked bibliographic resources)
- CiNii (2,006 related books)
- Douban (196 book subjects)
- Zhihu, EGAXA, the Lebanese National Library and Piraeus Bank Library (titles in Chinese, Arabic and Greek translation)

**Archival items, not works:**
- SNAC: 1,010 archival resources. Examples: "ALS, 1895 August 21: Victoria, B.C., to Mr. Harper", "Letter, 1880 November 3, Hartford, to Herbert E. Hill", "Century Magazine. Correspondence of the editors …". The pipeline capped extraction at 400.
- NARA: patent file 121992, a court case file and a slide series.
- Getty Museum: one photo album, but the record is conflated.

**Adaptations and media:**
- MusicBrainz (60 releases, e.g. "Tom Sawyer und Huckleberry Finn: Folge 1", "1957: Princ a žobrák")
- FilmAffinity (9), TV Maze, IMDb ("Big River"), TMDB
- KulturNav: 10 Swedish stage works ("Adams dagbok (Teaterpjäs)", "Huckleberry Finns äventyr (Teaterpjäs)")
- Radio France (8 podcast episodes)
- Songkick: a 2026 St. Pauli Theater show about Twain
- Tor.com/Reactor (2012 reprint of "A Ghost Story")

Only a handful of these are candidates for P800, such as *A Connecticut Yankee*, *Life on the Mississippi*, *The Innocents Abroad* and *Pudd'nhead Wilson*. The rest belongs on work items via P50 and P144 (based on), not on Q7245.

### 2.7 Relatives and associates

Wikidata has a spouse, 3 daughters, both parents and 2 siblings (Orion and Pamela).

- **Family Wikidata lacks:**
  - Son **Langdon Clemens** (1870–1872): FamilySearch PMBC-9GN, Find a Grave, Geni, WeRelate.
  - Siblings **Henry Clemens** (1838–1858, died after the steamboat *Pennsylvania* explosion), **Margaret Lampton Clemens** (1830–1839), **Benjamin L. Clemens** (1832–1842) and **Pleasant Hannibal Clemens**. Sources: FamilySearch, Find a Grave, Geni, WikiTree, WeRelate and GeneaStar.
  - Paternal grandparents Samuel B. Clemens and Pamela Goggin (GeneaStar).
  - None of these people has a Wikidata item (a search for Henry Clemens and Langdon Clemens found none), so adding them needs new items, or P1038 (relative) with a kinship qualifier.
- **Associates:**
  - SNAC lists **40 correspondents**, among them Thomas Bailey Aldrich, Andrew Carnegie, Joel Chandler Harris, Robert G. Ingersoll, William James, Augustin Daly, Daniel Carter Beard, Richard Watson Gilder, Houghton Mifflin and Century Company. It also has 16 families (Howells, Langdon kin and others) and his spouse.
  - BookBrainz names Henry Huttleston Rogers and the **American Anti-Imperialist League**. Twain was a vice-president of the League, and Wikidata's P463 lists only the American Academy of Arts and Letters.
  - NARA names Charles L. Webster (his publishing partner).
  - Co-author **Charles Dudley Warner** appears on Open Library, Project Gutenberg, SNL, BookBrainz and BookBub.
  - Illustrators: E. W. Kemble (BAnQ, ELNET), True W. Williams (ELNET), Dan Beard (NLI).
  - Employers: *Territorial Enterprise* (CineMagia, BookBrainz, museum-digital) and the Hannibal *Courier* (De Agostini). The item has no P108 (employer).
- **Not relations of the person:**
  - BNE's 127 OP5001 links and the translator and editor names on EGAXA, the Lebanese National Library, ELNET, Goodreads and CiNii are bibliographic contributors.
  - Open Library subject facets (Henry James, Hemingway) are co-occurrences.
  - LC/GND/VIAF links to Clemens, Snodgrass and Conte are his own pseudonym records.

### 2.8 Images

Wikidata has 2 P18 values plus P109 (signature), P1442 (grave) and 4 P1801 (plaque) images. 115 sites returned "image" values, but most of them are site logos, placeholders, ad thumbnails or covers. The surfing site's 136 images, Dimensions.com's 69 and Santiago de Compostela's 38 are all chrome or other entries.

| Kind | Sites | Notes |
|---|---|---|
| Portraits not obviously on Commons | NPG London (mw35538), Britannica (1907 photo), SNL, Lex.dk, Wien Geschichte Wiki (Marktwain.jpg), Douban (7), FamilySearch (8 patron uploads, incl. the 1907 photo with Dorothy Quick), Geni (11; mostly family members), Goodreads, Babelio, Tebeosfera, CineMagia, FantLab, Ben Yehuda, LOA, Poetry Foundation, Famous Birthdays, NNDB | Originals before 1910 are public domain, but these copies are site-hosted and rights-reserved or of unknown rights. They are leads for finding originals, not uploads. NPG's images are CC BY-NC-ND. |
| Grave and family photos | Find a Grave (21) | The photos are copyrighted by the users who uploaded them. Wikidata already has a grave image. |
| Reuse of Commons files | Parsifal, PMB, Japan Search, BVMC, FID, Klexikon, Online Nevada, CoBiS, NLP | Nothing new. |
| Other | Google Arts & Culture (6, from partner collections); Dimensions.com height drawings (SVG); Open Library (3 author photos and covers); IMDb (25 stills from adaptations) | — |

### 2.9 Identifiers

Wikidata already carries 420 identifier values (318 properties), including all six ISNIs, both SNAC ARKs, both Find a Grave memorials and 4 VIAF clusters. Missing and wrong identifiers are listed in `review.md`. These include the second "Conte" ISNI, FAST 1986616, the NACSIS-CAT and NTA real-name records, the stale CiNii crid, the Yale *Spirit* agent and the wrong Open Plaques ID. One addition not in `review.md`:

- **MusicBrainz artist 09b5de5d-52cf-426e-b457-ceba78379502**, the "Samuel Langhorne Clemens" artist. Both the main MusicBrainz artist and ISNI 0000000108003124 list it as same-as. Add it as a second P434 qualified "named as: Samuel Langhorne Clemens".

## 3. Kinds of data Wikidata does not hold

| Kind of data | Sites, and what it looks like | Wikidata property? |
|---|---|---|
| **Library classification** | LC and FAST 053: **PS1300–PS1348**, "Clemens, Samuel Langhorne ('Mark Twain')", assigner DLC. GND 065: subject category **12.2p** (English/American literature, persons). IdRef 686: collection tag "FONDS_BASTAIRE" (BIBNUM Omeka-S). | **P1149** (Library of Congress Classification) for PS1300–PS1348. GND subject categories have no property. The IdRef tag is a local collection tag, so it is out of scope. |
| **Cataloguing sources ("found in", 670/810)** | LC 25 citations (DAB 1930; title pages in Russian, Japanese, Persian, Bengali, Armenian, Mongolian and Hebrew; "OCLC, May 13, 2024"); NLI and UAE copies; BAnQ (Klinck, NUC vol. 112, Wallace, Wikipedia 2014-12-01); NLL (Britannica 15th ed. 2002, LTE 1983 t. 11, БСЭ 1976 t. 25); NSK (Proleksis, Hrvatska enciklopedija, cited 6.12.2016); SBN; IdRef (BN Cat. gén. 1960–1969); BNE ("Dic. de escritores célebres, 1995"); NARA (DAB, NUCMC/Stowe-Day) | References (P248 stated in, plus P1683 quotation) on P742 statements. **P1343** (described by source) for reference works not yet listed: Wikidata's 17 values lack the *Dictionary of American Biography*, the *Great Soviet Encyclopedia*, the *Lithuanian Soviet Encyclopedia*, *Eesti entsüklopeedia*, ANB and Grove. Aliases themselves cannot carry references. |
| **Authority notes and structure** | LC 663/667: "For works of this author written under other names, search also under …", "SUBJECT USAGE: This heading is not valid for use as a subject …", "Pseudonym not established: Jean François Alden". GND 500 $4 "nawi" (real identity) and "pseu" (pseudonym) links to separate pseudonym records. NTA, SNK, NKC and NARA all keep separate real-name and pseudonym records. | Partly. Wikidata has P742 and a single item, and does not model the "pseudonym record ↔ real-name record" split. Out of scope, apart from the pseudonym values. |
| **Archival holdings and finding aids** | SNAC: 1,010 archival resources and 168 finding-aid sources. By repository: Harvard (Houghton) 55, NYPL 20, LC Manuscript Division 11, Yale 11, Virginia 8, Bancroft 7, Stanford 5, Duke, Cornell and Columbia 4 each, plus about 25 more. Other sources: Kalliope (German manuscript union catalogue); Archives at Yale agents; NARA (patent, court case, slides); Europeana (2 digitised manuscripts, e.g. a PDF at BVAU Iași). | **P485** (archives at), qualified with **P8091** (ARK) or P973 (described at URL), for the main repositories. Today it holds only Beinecke, UW–Madison and the Harry Ransom Center; it lacks Houghton, NYPL, LC Manuscript Division and **Bancroft (the Mark Twain Papers)**. Item-level letters are out of scope. |
| **Museum object holdings** | Getty Museum: one photo album (conflated record). ANMM, Stedelijk, the Swedish History Museum (1 object), DigitaltMuseum, Google Arts & Culture. | **P6379** (has works in the collection) already lists ANMM, Stedelijk and Getty. Nothing more is needed. |
| **Performance and stage records** | Carnegie Hall Data Lab agent 2088 (role 946, birth place GeoNames; event data not captured because the SPARQL endpoint was offline). KulturNav "actorIn": 10 Swedish stage works. Les Archives du spectacle, Sceneweb, Kunstenpunt ("Uitvoerder"), GTAA (Dutch broadcast thesaurus), FID performing arts, DAHR. Songkick: one 2026 show *about* Twain. | No property on the person. Productions are modelled on work and production items (P144 based on, P50). Out of scope for Q7245. |
| **Film and TV credits** | IMDb, TMDB (13 credit roles), FilmAffinity, ČSFD, Kinobox, CineMagia, Sinemalar, PORT, TV Maze, MyAnimeList, CINE21: "Original Story", "Novel", "Characters" credits on adaptations | Out of scope on the person. Adaptations are covered by P144 on film items. |
| **Music and audio releases** | MusicBrainz: 60 "album" releases (audiobooks and radio plays). Genius: 92 text pages. Discogs "Mark Twain (2)". Hoopla. DAHR. | Out of scope on the person. Use release-group items with P50 or P175 if needed. |
| **Genealogy** | FamilySearch: tree IDs for parents, children and siblings, 15 vital-date pairs, and a surname-origin note (noise). Geni: transcriptions of the 1850–1910 US federal censuses (e.g. 1860, "Saml Clemmens", St Louis Ward 6; 1900 "Saul L Clemens"). Find a Grave: 13 family memorials, the cemetery and plot. WikiTree: Clemens-1/-2/-6/-7/-8/-9. WeRelate. GeneaStar. | Relatives fit P22/P25/P40/P3373/P1038. Burial is already in P119. Census transcriptions and tree IDs of relatives belong on the relatives' items (P2889, P535, P2949), so they are out of scope here. |
| **Plaques, doodles, commemoration** | Google Doodle: "Mark Twain's 176th Birthday Doodle" (2011). Open Plaques: wrong person (see `review.md`). Wien Geschichte Wiki: computed anniversary years ("Jubiläum" 1885, 1895, 1905 …). | The Doodle ID (P4431) and plaque images (P1801) are already present. The anniversary years are derived data, so out of scope. |
| **Awards and honours** | ULAN and Getty scope note: "awarded honorary degree by Oxford University" (1907) | **P166** currently holds only a Yale honorary doctorate (plus two Nevada halls of fame). Add an Oxford honorary doctorate (D.Litt. 1907) and cite a better source than ULAN. |
| **Physical description** | Dimensions.com: height 5′9″ (1.75 m) | **P2048** (height) exists and is absent here. Dimensions.com is a weak source. |
| **Personality typing** | Personality Database: "ENTP 7w6", crowd-voted, 107 comments | Not a fact. Out of scope. |
| **Mentions in periodicals and diaries** | PMB (Austrian Academy of Sciences): mentioned in *Die Fackel*, *Die Schaubühne*, *Der Brenner*, Schnitzler's readings and diary | Out of scope, unless the periodicals have their own index-ID properties. |
| **Record administration** | LC: record created 1979-04-18, last changed 2026-09-13, sources DLC and HU, 40 change notes. Libris: recordStatus, descriptionCreator, catalogingSource, descriptionConventions. IdRef 801: Abes 2025-10-12, AFNOR. GND: descriptionLevel, maintainer, "Basic Heading". GTAA: status, dateAccepted/Submitted. K-samsök: dataQuality, lastChangedDate. KulturNav: createdAt/updatedAt. | Out of scope. Wikidata does not record the state of external records. |
| **VIAF cluster membership** | VIAF 998 fields carried in every VIAF-derived copy, listing about 60 member records (LC, DNB, BnF, NKC, PLWABN, J9U, BAV, NLA, RSL, BIBSYS, BNCHL …). The 996 entries are records VIAF placed in *other* clusters. | The identifiers are already on Wikidata (checked against `identifiers.json`). The 998 data is useful for auditing, not for adding. Never use 996 (see `review.md`). |
| **Usage and popularity counts** | CiNii (2,006 related books), NLK (1,346), Douban (196), the Open Library subject page (edition counts by year), Zhihu Q&A counts, PDB votes, Project Gutenberg download counts | Out of scope. |
| **Subjects and genres** | LC and FAST fields of activity: "Wit and humor", genre forms "Humor". BookBub genres. NLK: 영미 문학 (English-American literature), 아동 문학 (children's literature). SNAC: 91 associated subjects, mostly about the archival materials (Copyright, Lectures and lecturing, Publishers and publishing, Business failures). | P101 already has literature and humor. **P136** (genre) has only "historical fiction"; satire, humor, travel literature and children's literature are reasonable additions. The SNAC subjects describe the archives, not the person. |

## 4. Site by site: what each offers beyond Wikidata

| Site (property) | Distinctive offering beyond Wikidata |
|---|---|
| SNAC (P3430) | 1,010 archival resources across about 35 repositories, 168 finding aids, 783 related agents (40 correspondents, 16 families), 91 archival subjects, a biogHist |
| LC NAF (P244) | 115 variant headings in about 20 scripts, 25 dated "found in" citations, the Alden note, PS1300–PS1348, associated place Hannibal, record history from 1979 |
| FAST (P2163) | The same 053 class and 370 place in FAST form; 18 variants |
| GND (P227) | 105 variants (with language tags in Kalliope: "chines.", "japan.", "lett.", "litauische Namensform"), 5 linked pseudonym/real-name records, 20 publication titles, subject category 12.2p, occupation hierarchy (characteristic vs other) |
| Kalliope (P9964) | GND name forms plus the entry point to German manuscript holdings |
| VIAF (P214) | Cluster membership (998), 20 work clusters, name forms from about 60 sources, glued given/family pairs (noisy) |
| VIAF-derived national copies (UAE P10021, NLI P10227, LAC P8179, BAnQ P3280, Slovak P7700, NLL P7699, Flemish P7024, EGAXA P1309, Lebanon P7026, ELNET P6394) | Local 670/810 citations, local-language notes (lt, et), title lists of 10–40 each, translators and illustrators |
| ISNI (P213) | 68 variants, the deprecated-ISNI chain, MusicBrainz source links (the second MB artist) |
| BNE (P950) | Full place hierarchy for birth and death, sources (P1002/P1003), affiliation "Academia Estadounidense de las Artes y las Letras", 127 contributor links, 12 works |
| IdRef (P269) | French "Marc Twain", 810 sources (BN Cat. gén.), Chinese 吐温, 马克, a French biographical note |
| NLL (P7699) | Lithuanian historical forms (Tvainas, Twainas, Tvėnas), 9 sources incl. БСЭ and LTE, lt description, occupations publisher and businessman |
| NLK (P5034) | Korean variants (마아크 트웨인, 마커 투원), 1,346 bibliographic links, inventor occupation, Korean subject fields |
| Archives at Yale (P8902) | 23 variants; the 87456 agent is the real one, 56569 is the *Spirit* agent (see `review.md`) |
| NARA (P1225) | Separate real-name (10574508) and pseudonym (10581697) authorities, patent 121992, court case file, NUCMC citation |
| Getty ULAN / Museum (P245, P12040) | Scope note with the Oxford honorary degree. The Museum record is conflated with a Plainfield, NJ photographer. |
| FamilySearch (P2889) | Tree IDs for relatives incl. son Langdon, vital dates, "Josh Clemens" alias, patron photos |
| Find a Grave (P535) | Woodlawn plot and monument, 13 linked family memorials, grave photos, a long biography |
| Geni (P2600) | 1850–1910 census transcriptions, family links, 40 works, he/no biographies |
| WikiTree / WeRelate / GeneaStar (P2949, P4159, P8094) | Sibling set and grandparents |
| Open Library (P648) | 84 variants (some junk), 20 works, author bio, remote IDs (LibriVox, LibraryThing, Goodreads) |
| museum-digital (P12597) | Wikipedia leads in 35 languages (source of the missing-language descriptions), 10 authority links |
| CiNii / Douban / Zhihu (P11496, P6441, P3553) | Japanese and Chinese biographies, real name in Chinese, translated-title bibliographies (2,006 / 196 items) |
| SNL / Lex.dk / De Agostini / Arab Encyclopedia (P4342, P8313, P6706, P13750) | Full encyclopedia articles in nb, da, it and ar, with residence places and work lists |
| Carnegie Hall (P4104) / KulturNav (P1248) | Performance-history entry point and Swedish stage works |
| MusicBrainz (P434) | 60 audio releases, second (real-name) artist ID, Monroe County birthplace hierarchy |
| IMDb / TMDB / FilmAffinity (P345, P4985, P12153) | Adaptation credits; not facts about the person |

## 5. Suggested additions to Wikidata

Each of these looks safe, and the sources are named.

- **P742 pseudonym "Jean François Alden"**, plus an alias. Sources: LC n79021164 (667, 670), Santa Croce 80295, NLI, GND.
- **Aliases:**
  - pl "Marek Twain" (LC 670, *Przygody Huck'a*, 1912)
  - fr "Marc Twain" (IdRef 027171876)
  - lt "Markas Tvainas", "Morkas Tvėnas" (NLL)
  - lv "Marks Tvēns" (GND)
  - he "מרק טוויין" (LC, ISNI) and the Yiddish forms "מארק טװײן", "מארק טווען" under yi (LC, Yale)
  - zh "萨缪尔·兰亨·克莱门" (Douban)
  - ar "صامويل لانغهورن كليمنز" (Arab Encyclopedia)
  - ko "마아크 트웨인" (NLK)
  - mul "Make Teviin" (LC 670, Mongolian colophon)
- **Occupations (P106):** publisher, businessperson and inventor (NARA patent 121992). Typesetter and miner are optional.
- **Residence (P551) with dates:** Hannibal (LC and FAST 370), Virginia City, San Francisco, Buffalo, Hartford.
- **P1149** Library of Congress Classification **PS1300-PS1348** (LC n79021164 053).
- **P485 archives at:** Houghton Library, NYPL, LC Manuscript Division, Bancroft Library (Mark Twain Papers), with P8091 ARKs or finding-aid URLs from SNAC w6dg7gd6.
- **P434:** add the second MusicBrainz artist 09b5de5d-52cf-426e-b457-ceba78379502 ("Samuel Langhorne Clemens"). Also the identifier fixes in `review.md` (FAST 1986616, the NACSIS-CAT and NTA real-name records, removing Yale people/56569 and the wrong Open Plaques ID).
- **P166:** honorary doctorate from the University of Oxford, 1907. ULAN 500020427 mentions it; cite a primary source.
- **P1343 described by source:** *Dictionary of American Biography* (cited by LC, NARA and NLI), *Great Soviet Encyclopedia* and *Lithuanian Soviet Encyclopedia* (NLL).
- **Descriptions** in languages Wikidata lacks (write them fresh; don't copy the source wording):
  - da: "amerikansk forfatter og humorist (1835–1910)"
  - nb: "amerikansk forfatter og humorist (1835–1910)"
  - tr: "Amerikalı yazar ve mizahçı (1835–1910)"
  - et: "Ameerika kirjanik ja humorist (1835–1910)"
  - lt: "amerikiečių rašytojas ir humoristas (1835–1910)"
  - vi: "nhà văn và nhà hài hước người Mỹ (1835–1910)"
  - Also th, ta, ur, tl and sw, written from the respective Wikipedias.
- **Family (needs new items):** son Langdon Clemens (1870–1872), and brothers Henry (1838–1858) and Benjamin (1832–1842). Sources: FamilySearch, Find a Grave, WikiTree.
