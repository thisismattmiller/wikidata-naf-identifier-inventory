# Vocabulary mapping: site predicates / fields → canonical element → Wikidata

Aggregated over the 297 profiled sites. *sites* = how many sites supply that element through that predicate/field. Prefixes: `json:` = key in an ad-hoc JSON API; `llm:` = extracted by the LLM pass (`llm:og:*` = OpenGraph page metadata, `llm:MARC nnn` = a MARC field inside a JSON record, `llm:free text` = parsed out of a biography/description); bare three-digit numbers = MARC authority fields; `mads:` / `eac:` = MADS XML / EAC-CPF; otherwise the RDF predicate's local name.

| element | Wikidata | predicate / field | sites | examples |
|---|---|---|---|---|
| name_preferred | label | `llm-page:page heading` | 71 | AniList staff ID, Armeniapedia ID, Artists of the World ID |
| name_preferred | label | `llm:og:title` | 63 | Adelphi author ID, American National Biography ID, Arab Encyclopedia concept ID |
| name_preferred | label | `name` | 41 | Archives at Yale agent ID, Artists of the World ID, CBDB.cz author ID |
| name_preferred | label | `llm:json field` | 36 | BHCL UUID, Babelio author ID, BookBrainz author ID |
| name_preferred | label | `json:name` | 32 | Australian National Maritime Museum person ID, BHCL UUID, BVMC person ID |
| name_preferred | label | `100` | 16 | BAnQ authority ID, Canadiana Name Authority ID, DBC author ID |
| name_preferred | label | `label` | 9 | Armeniapedia ID, ISNI, Kunstenpunt Knowledge Graph ID |
| name_preferred | label | `json:title` | 9 | BookBrainz author ID, BookBub author ID, Encyclopedia of Surfing ID |
| name_preferred | label | `prefLabel` | 7 | Europeana entity, FID performing arts ID, GTAA ID |
| name_preferred | label | `llm-page:page heading ` | 6 | Library of Congress JukeBox ID (former scheme), Obálky knih ID, PUG authority ID |
| name_preferred | label | `llm-page:heading` | 6 | Famous Birthdays ID, J9U entity ID, KBR person ID |
| name_preferred | label | `llm-page:article heading` | 6 | Arab Encyclopedia concept ID, Great Russian Encyclopedia Online ID (2017), Hrvat |
| name_variant | alias / P742 / P1477 | `llm:json field` | 36 | Arabic Ontology lexical concept ID, BHCL UUID, BookBrainz author ID |
| name_variant | alias / P742 / P1477 | `400` | 15 | DBC author ID, EGAXA ID, ELNET ID |
| name_variant | alias / P742 / P1477 | `llm:og:description` | 14 | Arab Encyclopedia concept ID, Babelio author ID, CineMagia person ID |
| name_variant | alias / P742 / P1477 | `alternateName` | 10 | Archives at Yale agent ID, CineMagia person ID, DBNL author ID |
| name_variant | alias / P742 / P1477 | `llm:free text` | 9 | BookBub author ID, CiNii Research ID, De Agostini ID |
| name_variant | alias / P742 / P1477 | `altLabel` | 7 | Europeana entity, FID performing arts ID, JudaicaLink person (GND) ID |
| name_variant | alias / P742 / P1477 | `llm-page:MARC 400` | 6 | Lebanese National Library ID, Pontifical University of Salamanca ID, Pontificia  |
| name_variant | alias / P742 / P1477 | `llm:MARC 998` | 4 | BAnQ authority ID, DBC author ID, EGAXA ID |
| name_variant | alias / P742 / P1477 | `llm-page:bio first sentence` | 4 | DAHR artist ID, LibriVox author ID, Obálky knih ID |
| name_variant | alias / P742 / P1477 | `llm-page:400` | 4 | American Academy in Rome ID, Angelicum ID, UCA authority ID |
| name_variant | alias / P742 / P1477 | `variantNameForThePerson` | 3 | BVMC person ID, GND ID, Open Library ID |
| name_variant | alias / P742 / P1477 | `llm-page:article first sentence` | 3 | Gran Enciclopèdia Catalana ID (former scheme), Online PWN Encyclopedia ID, Trecc |
| pseudonym | P742 | `llm:json field` | 21 | BHCL UUID, BookBrainz author ID, CANTIC ID |
| pseudonym | P742 | `llm:og:description` | 9 | Arab Encyclopedia concept ID, CineMagia person ID, Comic Vine ID |
| pseudonym | P742 | `llm:free text` | 6 | De Agostini ID, Geni profile ID, Nationale Thesaurus voor Auteursnamen ID |
| pseudonym | P742 | `llm-page:bio` | 3 | LibriVox author ID, MyAnimeList people ID, Poetry Foundation ID |
| pseudonym | P742 | `llm-page:Pseudonym` | 3 | DDB person (GND) ID, FID performing arts ID, Golden ID (archived) |
| pseudonym | P742 | `llm-page:400` | 3 | Angelicum ID, SEARCH on line catalogue ID, UOM ID |
| pseudonym | P742 | `llm:MARC 998` | 2 | EGAXA ID, ELNET ID |
| pseudonym | P742 | `llm-page:bio: 'better known by his pen name Mark T` | 2 | Listal ID, Obálky knih ID |
| pseudonym | P742 | `llm-page:MARC 400` | 2 | Pontificia Università della Santa Croce ID, RERO ID (legacy) |
| pseudonym | P742 | `llm-page:Biography` | 2 | TMDB person ID, WikiTree person ID |
| pseudonym | P742 | `llm-page:500 see also` | 2 | SEARCH on line catalogue ID, UOM ID |
| pseudonym | P742 | `realIdentity` | 1 | GND ID |
| given_name | P735 | `llm:json field` | 8 | Geni profile ID, Great Norwegian Encyclopedia ID, Nationale Thesaurus voor Auteu |
| given_name | P735 | `givenName` | 8 | DBNL author ID, Famous Birthdays ID, IdRef ID |
| given_name | P735 | `llm-page:page heading` | 4 | Dansk Forfatterleksikon ID, Roglo person ID, az.lib.ru author ID |
| given_name | P735 | `llm-page:heading` | 2 | Prabook ID, WikiTree person ID |
| given_name | P735 | `llm-page:bio` | 2 | Poetry Foundation ID, Projekt Gutenberg-DE author ID |
| given_name | P735 | `variantNameEntityForThePerson` | 1 | GND ID |
| given_name | P735 | `preferredNameEntityForThePerson` | 1 | GND ID |
| given_name | P735 | `llm:og:description` | 1 | National Historical Museums of Sweden ID |
| given_name | P735 | `llm:MARC 100` | 1 | BAnQ authority ID |
| given_name | P735 | `llm-page:stub heading` | 1 | NE.se ID |
| given_name | P735 | `llm-page:relation GIVEN NAME` | 1 | BabelNet ID |
| given_name | P735 | `llm-page:real-name reference form` | 1 | NL CR AUT ID |
| family_name | P734 | `llm:json field` | 8 | Geni profile ID, Great Norwegian Encyclopedia ID, Nationale Thesaurus voor Auteu |
| family_name | P734 | `familyName` | 6 | DBNL author ID, Famous Birthdays ID, IdRef ID |
| family_name | P734 | `llm-page:page heading` | 4 | Dansk Forfatterleksikon ID, Roglo person ID, az.lib.ru author ID |
| family_name | P734 | `surname` | 2 | Münzkabinett ID, Swedish Open Cultural Heritage URI |
| family_name | P734 | `llm-page:bio` | 2 | Poetry Foundation ID, Projekt Gutenberg-DE author ID |
| family_name | P734 | `json:familyName` | 2 | WikiTree person ID, ‎HAND ID |
| family_name | P734 | `variantNameEntityForThePerson` | 1 | GND ID |
| family_name | P734 | `preferredNameEntityForThePerson` | 1 | GND ID |
| family_name | P734 | `llm:og:description` | 1 | National Historical Museums of Sweden ID |
| family_name | P734 | `llm:MARC 100` | 1 | BAnQ authority ID |
| family_name | P734 | `llm-page:stub heading` | 1 | NE.se ID |
| family_name | P734 | `llm-page:relation FAMILY NAME` | 1 | BabelNet ID |
| birth_date | P569 | `llm:json field` | 30 | Arabic Ontology lexical concept ID, BHCL UUID, BookBrainz author ID |
| birth_date | P569 | `birthDate` | 25 | Artists of the World ID, CBDB.cz author ID, Carnegie Hall Agent ID |
| birth_date | P569 | `llm-page:heading dates` | 16 | BNMM authority ID, CCAB ID, CONOR.BG ID |
| birth_date | P569 | `llm:free text` | 9 | BookBub author ID, CiNii Research ID, De Agostini ID |
| birth_date | P569 | `json:birthDate` | 9 | FamilySearch person ID, FantLab author ID, Goodreads author ID |
| birth_date | P569 | `046$f` | 9 | BAnQ authority ID, Canadiana Name Authority ID, DBC author ID |
| birth_date | P569 | `llm:og:description` | 8 | Arab Encyclopedia concept ID, CineMagia person ID, FactGrid item ID |
| birth_date | P569 | `llm-page:bio` | 7 | BookBub author ID, Klexikon article ID, LibriVox author ID |
| birth_date | P569 | `llm:og:title` | 6 | American National Biography ID, Diamond Catalog ID for persons and organisations |
| birth_date | P569 | `llm-page:Born` | 6 | FilmAffinity person or company ID, GCD creator ID, Goodreads author ID |
| birth_date | P569 | `llm-page:100 $d` | 5 | American Academy in Rome ID, Cyprus University of Technology ID, PUG authority I |
| birth_date | P569 | `dateOfBirth` | 5 | BVMC person ID, Europeana entity, GND ID |
| death_date | P570 | `llm:json field` | 29 | Arabic Ontology lexical concept ID, BHCL UUID, BookBrainz author ID |
| death_date | P570 | `deathDate` | 22 | Artists of the World ID, CBDB.cz author ID, Carnegie Hall Agent ID |
| death_date | P570 | `llm-page:heading dates` | 17 | BNMM authority ID, BiblioNet author ID, CCAB ID |
| death_date | P570 | `json:deathDate` | 10 | FamilySearch person ID, Find a Grave memorial ID, Geni profile ID |
| death_date | P570 | `llm:free text` | 9 | BookBub author ID, CiNii Research ID, De Agostini ID |
| death_date | P570 | `046$g` | 9 | BAnQ authority ID, Canadiana Name Authority ID, DBC author ID |
| death_date | P570 | `llm-page:Died` | 8 | FilmAffinity person or company ID, GCD creator ID, Goodreads author ID |
| death_date | P570 | `llm:og:title` | 6 | American National Biography ID, Diamond Catalog ID for persons and organisations |
| death_date | P570 | `llm-page:bio` | 6 | LibriVox author ID, Penguin Random House author ID, Perlentaucher ID |
| death_date | P570 | `llm:og:description` | 5 | Arab Encyclopedia concept ID, CineMagia person ID, FactGrid item ID |
| death_date | P570 | `llm-page:100 $d` | 5 | American Academy in Rome ID, Cyprus University of Technology ID, PUG authority I |
| death_date | P570 | `dateOfDeath` | 5 | BVMC person ID, Europeana entity, GND ID |
| birth_place | P19 | `llm:json field` | 15 | CoBiS author ID, Geni profile ID, Great Norwegian Encyclopedia ID |
| birth_place | P19 | `birthPlace` | 11 | CBDB.cz author ID, Carnegie Hall Agent ID, FID performing arts ID |
| birth_place | P19 | `llm:og:description` | 6 | Arab Encyclopedia concept ID, CineMagia person ID, FactGrid item ID |
| birth_place | P19 | `llm:free text` | 6 | BookBub author ID, CiNii Research ID, De Agostini ID |
| birth_place | P19 | `370$a` | 5 | EGAXA ID, FAST ID, National Library of Ireland ID |
| birth_place | P19 | `llm-page:bio` | 4 | Encyclopædia Universalis ID, Fancyclopedia 3 ID, Perlentaucher ID |
| birth_place | P19 | `llm-page:Born` | 4 | GCD creator ID, Goodreads author ID, Internet Broadway Database person ID |
| birth_place | P19 | `P98i_was_born` | 4 | J. Paul Getty Museum agent ID, KulturNav-ID, Union List of Artist Names ID |
| birth_place | P19 | `llm-page:Place of birth` | 3 | BookBrainz author ID, Douban author ID, J9U entity ID |
| birth_place | P19 | `llm-page:Naissance` | 3 | BD Gest' author ID, Bibliothèque nationale de France ID, NooSFere author ID |
| birth_place | P19 | `llm-page:Birthplace` | 3 | Famous Birthdays ID, Golden ID (archived), NNDB people ID |
| birth_place | P19 | `json:birthPlace` | 3 | Find a Grave memorial ID, PORT person ID, ‎HAND ID |
| death_place | P20 | `llm:json field` | 13 | CoBiS author ID, Great Norwegian Encyclopedia ID, National Library of Ireland ID |
| death_place | P20 | `deathPlace` | 7 | FID performing arts ID, KulturNav-ID, LTit person ID |
| death_place | P20 | `370$b` | 5 | FAST ID, National Library of Ireland ID, RILM ID |
| death_place | P20 | `llm:og:description` | 4 | Arab Encyclopedia concept ID, CineMagia person ID, FactGrid item ID |
| death_place | P20 | `llm:free text` | 4 | De Agostini ID, Geni profile ID, NSK ID |
| death_place | P20 | `llm-page:bio` | 4 | Encyclopædia Universalis ID, Perlentaucher ID, Poetry Foundation ID |
| death_place | P20 | `llm-page:Died` | 4 | FilmAffinity person or company ID, GCD creator ID, Internet Broadway Database pe |
| death_place | P20 | `P100i_died_in` | 4 | J. Paul Getty Museum agent ID, KulturNav-ID, Union List of Artist Names ID |
| death_place | P20 | `llm-page:lead sentence` | 2 | Arab Encyclopedia concept ID, Encyclopædia Britannica Online ID |
| death_place | P20 | `llm-page:header` | 2 | Tebeosfera ID, ČSFD person ID |
| death_place | P20 | `llm-page:biography` | 2 | FantLab author ID, SNAC ARK ID |
| death_place | P20 | `llm-page:article first sentence` | 2 | Online PWN Encyclopedia ID, Treccani's Enciclopedia Italiana ID |
| activity_place | P937 / P551 | `llm-page:bio` | 13 | Arab Encyclopedia concept ID, Babelio author ID, DAHR artist ID |
| activity_place | P937 / P551 | `llm:json field` | 9 | BookBrainz author ID, Great Norwegian Encyclopedia ID, J. Paul Getty Museum agen |
| activity_place | P937 / P551 | `llm:free text` | 5 | CiNii Research ID, De Agostini ID, Geni profile ID |
| activity_place | P937 / P551 | `llm-page:article text` | 5 | Enciclopedia Galega Universal ID, Encyclopædia Britannica Online ID, Gran Encicl |
| activity_place | P937 / P551 | `llm-page:biography` | 4 | FantLab author ID, Fantastic Fiction author ID, Latter-day Saint Literature data |
| activity_place | P937 / P551 | `llm-page:article` | 3 | Lex ID, Treccani's Enciclopedia Italiana ID, Vienna History Wiki ID |
| activity_place | P937 / P551 | `llm:og:description` | 2 | CineMagia person ID, Portal da Literatura ID |
| activity_place | P937 / P551 | `llm-page:miejsce powiązane` | 2 | NLP ID, National Library of Poland MMS ID |
| activity_place | P937 / P551 | `llm-page:bio: grew up in` | 2 | Fancyclopedia 3 ID, Obálky knih ID |
| activity_place | P937 / P551 | `370$e` | 2 | FAST ID, Library of Congress Authorities ID |
| activity_place | P937 / P551 | `location` | 1 | MusicBrainz artist ID |
| activity_place | P937 / P551 | `llm-page:地域` | 1 | Media Arts Database ID |
| gender | P21 | `llm:json field` | 11 | KulturNav-ID, Lebanese National Library ID, Les Archives du spectacle person ID |
| gender | P21 | `llm-page:Gender` | 10 | AniList staff ID, Comic Vine ID, Douban author ID |
| gender | P21 | `gender` | 10 | Evene ID, GND ID, IdRef ID |
| gender | P21 | `json:gender` | 9 | FamilySearch person ID, Les Archives du spectacle person ID, PMB – Personen der  |
| gender | P21 | `375` | 8 | BAnQ authority ID, DBC author ID, EGAXA ID |
| gender | P21 | `llm:MARC 375` | 3 | BAnQ authority ID, DBC author ID, EGAXA ID |
| gender | P21 | `P2_has_type` | 3 | J. Paul Getty Museum agent ID, Union List of Artist Names ID, ‎Yale LUX ID |
| gender | P21 | `llm:free text` | 2 | Geni profile ID, Zhihu topic ID |
| gender | P21 | `llm-page:płeć` | 2 | NLP ID, National Library of Poland MMS ID |
| gender | P21 | `llm-page:MARC 375` | 2 | Lebanese National Library ID, Slovak National Library (VIAF) ID |
| gender | P21 | `llm-page:Gender row` | 2 | PMB – Personen der Moderne Basis person ID, Union List of Artist Names ID |
| gender | P21 | `llm-page:성별` | 1 | CINE21 person ID |
| occupation | P106 | `llm:json field` | 27 | Arabic Ontology lexical concept ID, BHCL UUID, BookBrainz author ID |
| occupation | P106 | `llm-page:bio` | 23 | AniList staff ID, Arab Encyclopedia concept ID, Babelio author ID |
| occupation | P106 | `llm:og:description` | 22 | Africultures person ID, Arab Encyclopedia concept ID, Babelio author ID |
| occupation | P106 | `llm:free text` | 11 | BookBub author ID, CiNii Research ID, De Agostini ID |
| occupation | P106 | `374` | 9 | BAnQ authority ID, EGAXA ID, FAST ID |
| occupation | P106 | `jobTitle` | 8 | CineMagia person ID, Evene ID, Famous Birthdays ID |
| occupation | P106 | `llm-page:biography` | 7 | BiblioNet author ID, Douban personage ID, FantLab author ID |
| occupation | P106 | `llm-page:Occupation` | 7 | Alvin ID, Douban author ID, FID performing arts ID |
| occupation | P106 | `llm-page:description` | 6 | CoBiS author ID, GeneaStar person ID, LBT person ID |
| occupation | P106 | `llm-page:Biography` | 5 | Alexander Turnbull Library ID, Archives at Yale agent ID, At the Circulating Lib |
| occupation | P106 | `hasOccupation` | 5 | Artists of the World ID, CBDB.cz author ID, Carnegie Hall Agent ID |
| occupation | P106 | `llm-page:article` | 4 | Lex ID, NE.se ID, Treccani's Enciclopedia Italiana ID |
| field_of_activity | P101 | `llm:json field` | 9 | BookBub author ID, Great Norwegian Encyclopedia ID, Lex ID |
| field_of_activity | P101 | `372` | 4 | EGAXA ID, FAST ID, Library of Congress Authorities ID |
| field_of_activity | P101 | `053` | 4 | FAST ID, Library of Congress Authorities ID, National Library of Ireland ID |
| field_of_activity | P101 | `llm:og:description` | 2 | Africultures person ID, Douban author ID |
| field_of_activity | P101 | `llm-page:obszar działalności` | 2 | NLP ID, National Library of Poland MMS ID |
| field_of_activity | P101 | `llm-page:breadcrumb 文学 > 外国文学 > 美国文学` | 2 | Encyclopedia of China (Third Edition) ID (2026), Encyclopedia of China (Third Ed |
| field_of_activity | P101 | `llm-page:Campo de actividad` | 2 | BNMM authority ID, National Library of Spain SpMaBN ID |
| field_of_activity | P101 | `llm-page:Author Tags` | 2 | At the Circulating Library ID, ISFDB author ID |
| field_of_activity | P101 | `P50100` | 2 | KANTO ID, National Library of Spain SpMaBN ID |
| field_of_activity | P101 | `mads:fieldOfActivity` | 1 | Library of Congress Authorities ID |
| field_of_activity | P101 | `llm:free text` | 1 | De Agostini ID |
| field_of_activity | P101 | `llm:MARC 372` | 1 | EGAXA ID |
| nationality | P27 | `llm:json field` | 19 | Arabic Ontology lexical concept ID, BHCL UUID, BookBrainz author ID |
| nationality | P27 | `llm:og:description` | 18 | Arab Encyclopedia concept ID, Babelio author ID, CineMagia person ID |
| nationality | P27 | `llm:free text` | 9 | CiNii Research ID, De Agostini ID, Geni profile ID |
| nationality | P27 | `llm-page:bio` | 6 | AniList staff ID, DAHR artist ID, Goodreads author ID |
| nationality | P27 | `llm-page:article first sentence` | 4 | Gran Enciclopèdia Catalana ID (former scheme), Lex ID, Literary Encyclopedia ID |
| nationality | P27 | `nationality` | 3 | Evene ID, George Eastman Museum people ID, Libris-URI |
| nationality | P27 | `llm-page:first sentence` | 3 | Gran Enciclopèdia Catalana ID, Krugosvet article (archived), Treccani ID |
| nationality | P27 | `llm-page:description line` | 3 | Europeana entity, Runeberg author ID, gravsted.dk ID |
| nationality | P27 | `llm-page:description` | 3 | LBT person ID, Wellcome Collection concept ID, ‎Darwin Correspondence ID |
| nationality | P27 | `llm-page:Biography` | 3 | Alexander Turnbull Library ID, Archives at Yale agent ID, TMDB person ID |
| nationality | P27 | `P2_has_type` | 3 | J. Paul Getty Museum agent ID, Union List of Artist Names ID, ‎Yale LUX ID |
| nationality | P27 | `llm-page:line under heading` | 2 | George Eastman Museum people ID, Les Archives du spectacle person ID |
| language | P1412 / P103 / P6886 | `377` | 8 | BAnQ authority ID, Canadiana Name Authority ID, EGAXA ID |
| language | P1412 / P103 / P6886 | `llm:json field` | 7 | KulturNav-ID, Lebanese National Library ID, National Library of Korea ID |
| language | P1412 / P103 / P6886 | `json:language` | 4 | BookBrainz author ID, Kunstenpunt Knowledge Graph ID, SNARC ID |
| language | P1412 / P103 / P6886 | `llm-page:język` | 2 | NLP ID, National Library of Poland MMS ID |
| language | P1412 / P103 / P6886 | `llm-page:MARC 377` | 2 | Lebanese National Library ID, Pontificia Università della Santa Croce ID |
| language | P1412 / P103 / P6886 | `llm-page:Associated Language` | 2 | J9U entity ID, Library of Congress Authorities ID |
| language | P1412 / P103 / P6886 | `language` | 2 | IdRef ID, WeRelate person ID |
| language | P1412 / P103 / P6886 | `P50102` | 2 | KANTO ID, National Library of Spain SpMaBN ID |
| language | P1412 / P103 / P6886 | `mads:languageOfCataloging` | 1 | Library of Congress Authorities ID |
| language | P1412 / P103 / P6886 | `llm:free text` | 1 | Geni profile ID |
| language | P1412 / P103 / P6886 | `llm:MARC 940` | 1 | DBC author ID |
| language | P1412 / P103 / P6886 | `llm-page:言語` | 1 | Media Arts Database ID |
| description | description | `og:description` | 37 | Africultures person ID, American National Biography ID, Arab Encyclopedia concep |
| description | description | `llm:og:description` | 27 | Arab Encyclopedia concept ID, Babelio author ID, CineMagia person ID |
| description | description | `llm:json field` | 21 | Arabic Ontology lexical concept ID, BHCL UUID, BookBrainz author ID |
| description | description | `description` | 18 | Archives at Yale agent ID, CBDB.cz author ID, Databazeknih.cz author ID |
| description | description | `json:description` | 14 | CiNii Research ID, CoBiS author ID, De Agostini ID |
| description | description | `llm:free text` | 13 | BookBub author ID, CiNii Research ID, CoBiS author ID |
| description | description | `json:text` | 9 | BHCL UUID, CBDB.cz author ID, Encyclopedia of Surfing ID |
| description | description | `llm-page:bio paragraph` | 8 | Ben Yehuda author ID, DAHR artist ID, Fancyclopedia 3 ID |
| description | description | `llm-page:Biography` | 8 | Alexander Turnbull Library ID, Archives at Yale agent ID, At the Circulating Lib |
| description | description | `llm-page:bio` | 7 | AniList staff ID, Goodreads author ID, Google Arts & Culture entity ID |
| description | description | `678` | 6 | GND ID, IdRef ID, Lebanese National Library ID |
| description | description | `llm-page:article text` | 5 | Enciclopedia Galega Universal ID, Gran Enciclopèdia Catalana ID (former scheme), |
| work | P800 | `llm:json field` | 37 | BHCL UUID, BookBrainz author ID, BookBub author ID |
| work | P800 | `llm-page:bio` | 18 | AniList staff ID, Arab Encyclopedia concept ID, Babelio author ID |
| work | P800 | `llm-page:article text` | 10 | Enciclopedia Galega Universal ID, Enciclopédia Açoriana ID, Encyclopædia Britann |
| work | P800 | `llm:free text` | 8 | BookBub author ID, CiNii Research ID, Geni profile ID |
| work | P800 | `llm:og:description` | 7 | Africultures person ID, Arab Encyclopedia concept ID, CineMagia person ID |
| work | P800 | `creator` | 5 | BHCL UUID, BVMC person ID, GND ID |
| work | P800 | `llm:MARC 910` | 4 | BAnQ authority ID, DBC author ID, EGAXA ID |
| work | P800 | `llm-page:biography` | 4 | BD Gest' author ID, BiblioNet author ID, FantLab author ID |
| work | P800 | `llm-page:910` | 4 | BAnQ authority ID, DBC author ID, EGAXA ID |
| work | P800 | `llm:MARC 912` | 3 | BAnQ authority ID, EGAXA ID, ELNET ID |
| work | P800 | `llm-page:entry text` | 3 | Encyclopedia of Science Fiction ID, Encyclopedia of Surfing ID, The Encyclopedia |
| work | P800 | `llm-page:book list` | 3 | Internet Sacred Text Archive ID, Perlentaucher ID, Project Gutenberg author ID |
| subject_of | - (works about the person; not on the item) | `json:title` | 6 | BookBub author ID, CiNii Research ID, Douban author ID |
| subject_of | - (works about the person; not on the item) | `json:name` | 4 | De Agostini ID, FamilySearch person ID, PMB – Personen der Moderne Basis person  |
| subject_of | - (works about the person; not on the item) | `subjectOf` | 1 | Nationale Thesaurus voor Auteursnamen ID |
| subject_of | - (works about the person; not on the item) | `llm:json field` | 1 | KANTO ID |
| subject_of | - (works about the person; not on the item) | `llm-page:Norwegian section` | 1 | Geni profile ID |
| subject_of | - (works about the person; not on the item) | `llm-page:Hebrew section` | 1 | Geni profile ID |
| subject_of | - (works about the person; not on the item) | `llm-page:Further Reading` | 1 | Online Nevada Encyclopedia ID |
| subject_of | - (works about the person; not on the item) | `llm-page:About: Bibliography` | 1 | Geni profile ID |
| subject_of | - (works about the person; not on the item) | `llm-page:About this article` | 1 | Online Nevada Encyclopedia ID |
| subject_of | - (works about the person; not on the item) | `llm-page:About` | 1 | Geni profile ID |
| subject_of | - (works about the person; not on the item) | `json:label` | 1 | Library of Congress Authorities ID |
| subject_of | - (works about the person; not on the item) | `eac:resourceRelation[None]` | 1 | SNAC ARK ID |
| related_agent | P26 / P40 / P22 / P25 / P3373 | `llm:json field` | 26 | BHCL UUID, BookBrainz author ID, BookBub author ID |
| related_agent | P26 / P40 / P22 / P25 / P3373 | `llm-page:bio` | 13 | Arab Encyclopedia concept ID, Babelio author ID, DAHR artist ID |
| related_agent | P26 / P40 / P22 / P25 / P3373 | `llm-page:article text` | 7 | Enciclopedia Galega Universal ID, Enciclopédia Açoriana ID, Encyclopædia Britann |
| related_agent | P26 / P40 / P22 / P25 / P3373 | `500` | 7 | BAnQ authority ID, Canadiana Name Authority ID, GND ID |
| related_agent | P26 / P40 / P22 / P25 / P3373 | `llm-page:950` | 6 | BAnQ authority ID, DBC author ID, EGAXA ID |
| related_agent | P26 / P40 / P22 / P25 / P3373 | `llm:free text` | 5 | BookBub author ID, De Agostini ID, Goodreads author ID |
| related_agent | P26 / P40 / P22 / P25 / P3373 | `llm:og:description` | 4 | Africultures person ID, CineMagia person ID, GeneaStar person ID |
| related_agent | P26 / P40 / P22 / P25 / P3373 | `llm:MARC 950` | 4 | BAnQ authority ID, DBC author ID, EGAXA ID |
| related_agent | P26 / P40 / P22 / P25 / P3373 | `llm-page:work list` | 4 | Dansk Forfatterleksikon ID, IMSLP ID, Libris-URI |
| related_agent | P26 / P40 / P22 / P25 / P3373 | `llm:MARC 955` | 3 | BAnQ authority ID, EGAXA ID, ELNET ID |
| related_agent | P26 / P40 / P22 / P25 / P3373 | `llm-page:works list` | 3 | Aozora Bunko author ID, Encyclopedia of Science Fiction ID, Open Library ID |
| related_agent | P26 / P40 / P22 / P25 / P3373 | `llm-page:byline` | 3 | American National Biography ID, The Literary Encyclopedia person ID, Treccani's  |
| same_as | external identifiers | `llm:json field` | 26 | CANTIC ID, Canadiana Name Authority ID, CoBiS author ID |
| same_as | external identifiers | `sameAs` | 18 | Archives at Yale agent ID, BVMC person ID, Europeana entity |
| same_as | external identifiers | `exactMatch` | 7 | Carnegie Hall Agent ID, GTAA ID, Library of Congress Authorities ID |
| same_as | external identifiers | `llm:free text` | 4 | CoBiS author ID, Geni profile ID, Pontificia Università della Santa Croce ID |
| same_as | external identifiers | `llm:MARC 998` | 4 | BAnQ authority ID, DBC author ID, EGAXA ID |
| same_as | external identifiers | `page` | 3 | Armeniapedia ID, GND ID, Vienna History Wiki ID |
| same_as | external identifiers | `llm-page:Permalink` | 3 | J. Paul Getty Museum agent ID, SNAC ARK ID, VIAF cluster ID |
| same_as | external identifiers | `llm-page:998 VIAF cluster member` | 3 | EGAXA ID, ELNET ID, Flemish Public Libraries ID |
| same_as | external identifiers | `equivalent` | 3 | J. Paul Getty Museum agent ID, Union List of Artist Names ID, ‎Yale LUX ID |
| same_as | external identifiers | `llm-page:VIAF cluster link` | 2 | Lebanese National Library ID, Slovak National Library (VIAF) ID |
| same_as | external identifiers | `llm-page:URI` | 2 | KANTO ID, WorldCat Entities ID |
| same_as | external identifiers | `llm-page:References` | 2 | DigitaltMuseum ID, museum-digital person/organization ID |
| identifier | external identifiers | `llm:og:url` | 58 | Adelphi author ID, American National Biography ID, Arab Encyclopedia concept ID |
| identifier | external identifiers | `llm:json field` | 53 | Arabic Ontology lexical concept ID, BHCL UUID, Babelio author ID |
| identifier | external identifiers | `llm-page:page URL` | 30 | Ben Yehuda author ID, BookBrainz author ID, CBDB.cz author ID |
| identifier | external identifiers | `035` | 15 | BAnQ authority ID, Canadiana Name Authority ID, DBC author ID |
| identifier | external identifiers | `identifier` | 11 | American National Biography ID, DBNL author ID, Grove Music Online ID |
| identifier | external identifiers | `024` | 9 | BAnQ authority ID, FAST ID, GND ID |
| identifier | external identifiers | `llm-page:page URL ` | 8 | Douban author ID, GCD creator ID, Harper's tag |
| identifier | external identifiers | `llm-page:URL` | 7 | BHL creator ID, Brockhaus Enzyklopädie online ID, Dictionary of Sydney ID |
| identifier | external identifiers | `llm-page:001 control number` | 5 | American Academy in Rome ID, Cyprus University of Technology ID, Pontifical Urba |
| identifier | external identifiers | `llm:MARC 035` | 4 | BAnQ authority ID, DBC author ID, EGAXA ID |
| identifier | external identifiers | `llm-page:page URL https:` | 4 | George Eastman Museum people ID, Lex ID, Projekt Gutenberg-DE author ID |
| identifier | external identifiers | `llm-page:page URL slug ` | 3 | Encyclopedia of Science Fiction ID, Jeugdliteratuur ID, RPO poet ID |
| see_also | P856 / sitelinks | `url` | 23 | Artists of the World ID, CBDB.cz author ID, CiNii Research ID |
| see_also | P856 / sitelinks | `json:url` | 21 | Babelio author ID, BookBub author ID, De Agostini ID |
| see_also | P856 / sitelinks | `seeAlso` | 5 | J. Paul Getty Museum agent ID, KulturNav-ID, Library of Congress Authorities ID |
| see_also | P856 / sitelinks | `image` | 3 | CineMagia person ID, Evene ID, Famous Birthdays ID |
| see_also | P856 / sitelinks | `describedby` | 2 | GND ID, KulturNav-ID |
| see_also | P856 / sitelinks | `856` | 2 | National Library of Lithuania ID, Slovak National Library (VIAF) ID |
| see_also | P856 / sitelinks | `P129i_is_subject_of` | 1 | ‎Yale LUX ID |
| image | P18 | `og:image` | 19 | Africultures person ID, Arab Encyclopedia concept ID, CBDB.cz author ID |
| image | P18 | `llm:og:image` | 18 | BD Gest' author ID, Ben Yehuda author ID, CineMagia person ID |
| image | P18 | `image` | 14 | Databazeknih.cz author ID, Discogs artist ID, Fandom article ID |
| image | P18 | `json:image` | 11 | Babelio author ID, FantLab author ID, Find a Grave memorial ID |
| image | P18 | `llm:json field` | 7 | CoBiS author ID, Geni profile ID, Great Norwegian Encyclopedia ID |
| image | P18 | `thumbnailUrl` | 2 | LOA ID, Vienna History Wiki ID |
| image | P18 | `depiction` | 2 | FID performing arts ID, Open Library ID |
| image | P18 | `photo` | 1 | Vienna History Wiki ID |
| image | P18 | `logo` | 1 | De Agostini ID |
| image | P18 | `llm-page:profile photo caption` | 1 | Geni profile ID |
| image | P18 | `json:thumbnailUrl` | 1 | FamilySearch person ID |
| image | P18 | `json:picURL` | 1 | Personality Database profile ID |
| source | references | `llm:json field` | 24 | Arabic Ontology lexical concept ID, BHCL UUID, CANTIC ID |
| source | references | `670` | 10 | BAnQ authority ID, Canadiana Name Authority ID, EGAXA ID |
| source | references | `llm-page:670` | 7 | American Academy in Rome ID, Angelicum ID, EGAXA ID |
| source | references | `llm-page:040` | 7 | American Academy in Rome ID, Angelicum ID, BAnQ authority ID |
| source | references | `llm-page:Sources` | 6 | BabelNet ID, FamilySearch person ID, Library of Congress Authorities ID |
| source | references | `source` | 5 | American National Biography ID, Grove Music Online ID, ISNI |
| source | references | `llm-page:MARC 670` | 4 | NSK (VIAF) ID, Pontifical University of Salamanca ID, RERO ID (legacy) |
| source | references | `llm:MARC 670` | 3 | BAnQ authority ID, EGAXA ID, ELNET ID |
| source | references | `llm-page:źródło ` | 2 | NLP ID, National Library of Poland MMS ID |
| source | references | `llm-page:Zdroj` | 2 | Obálky knih ID, SNK ID |
| source | references | `llm-page:Source` | 2 | IdRef ID, Interlingual Index ID |
| source | references | `llm-page:References` | 2 | At the Circulating Library ID, WeRelate person ID |
| record_created | - | `llm:json field` | 18 | BAnQ authority ID, BHCL UUID, CANTIC ID |
| record_created | - | `created` | 8 | BVMC person ID, GND ID, IdRef ID |
| record_created | - | `llm-page:008` | 5 | American Academy in Rome ID, PUG authority ID, Pontifical Urbaniana University I |
| record_created | - | `dateCreated` | 3 | American National Biography ID, Grove Music Online ID, Vienna History Wiki ID |
| record_created | - | `llm-page:data utworzenia` | 2 | NLP ID, National Library of Poland MMS ID |
| record_created | - | `llm-page:MARC 008 date entered` | 2 | NSK (VIAF) ID, Pontifical University of Salamanca ID |
| record_created | - | `llm-page:MARC 008` | 2 | Lebanese National Library ID, RedBA Granada authority ID |
| record_created | - | `llm-page:008 field` | 2 | Cyprus University of Technology ID, Vatican Library ID (former scheme) |
| record_created | - | `llm-page:008 date entered` | 2 | Angelicum ID, UOM ID |
| record_created | - | `llm-page:sidebar` | 1 | subreddit |
| record_created | - | `llm-page:record footer` | 1 | Bibliothèque nationale de France ID |
| record_created | - | `llm-page:footer of card` | 1 | Tebeosfera ID |
| record_modified | - | `llm:json field` | 29 | BAnQ authority ID, BHCL UUID, CANTIC ID |
| record_modified | - | `modified` | 9 | GND ID, GTAA ID, IdRef ID |
| record_modified | - | `llm-page:footer` | 8 | Armeniapedia ID, FactGrid item ID, Fancyclopedia 3 ID |
| record_modified | - | `llm-page:005` | 8 | American Academy in Rome ID, Angelicum ID, Flemish Public Libraries ID |
| record_modified | - | `llm-page:MARC 005` | 6 | Lebanese National Library ID, NSK (VIAF) ID, Pontifical University of Salamanca  |
| record_modified | - | `llm-page:page footer` | 5 | Dansk Forfatterleksikon ID, Kunstenpunt Knowledge Graph ID, LiederNet author ID |
| record_modified | - | `json:dateModified` | 3 | De Agostini ID, Geni profile ID, WikiTree person ID |
| record_modified | - | `dateModified` | 3 | Kunstenpunt Knowledge Graph ID, LOA ID, SNARC ID |
| record_modified | - | `llm-page:page header` | 2 | Encyclopedia of China (Third Edition) old ID (2021), WeRelate person ID |
| record_modified | - | `llm-page:data aktualizacji` | 2 | NLP ID, National Library of Poland MMS ID |
| record_modified | - | `llm:og:updated_time` | 1 | Poets.org poet ID |
| record_modified | - | `llm-page:データ更新年月日` | 1 | Media Arts Database ID |
| license | - | `llm-page:footer` | 21 | At the Circulating Library ID, Carnegie Hall Agent ID, CoBiS author ID |
| license | - | `license` | 5 | GND ID, ISNI, Kunstenpunt Knowledge Graph ID |
| license | - | `llm-page:page footer` | 3 | Online Books Page author ID, Vegetti Catalog of Fantastic Literature NILF ID, Wo |
| license | - | `llm:json field` | 2 | Great Norwegian Encyclopedia ID, WordNet 3.1 Synset ID |
| license | - | `llm-page:article footer` | 2 | Treccani ID, Treccani's Enciclopedia Italiana ID |
| license | - | `rights` | 1 | WeRelate person ID |
| license | - | `llm-page:site footer` | 1 | abART person ID |
| license | - | `llm-page:sidebar License` | 1 | ISFDB author ID |
| license | - | `llm-page:sdo:sdLicense` | 1 | GTAA ID |
| license | - | `llm-page:rights badge under heading` | 1 | Ben Yehuda author ID |
| license | - | `llm-page:photo caption` | 1 | Geni profile ID |
| license | - | `llm-page:page text licence note` | 1 | J. Paul Getty Museum agent ID |
| type | P31 | `type` | 72 | Archives at Yale agent ID, Armeniapedia ID, Artists of the World ID |
| type | P31 | `368` | 2 | FAST ID, Library of Congress Authorities ID |
| type | P31 | `P2_has_type` | 1 | Union List of Artist Names ID |

## Unmapped predicates / fields (seen on the entity, not assigned to an element)

| predicate | sites |
|---|---|
| `(og chrome: tagline / site image)` | 73 |
| `(no node about the entity in this file)` | 52 |
| `('(Spirit)' heading via page text, dropped)` | 13 |
| `MARC 998` | 11 |
| `MARC 997` | 11 |
| `MARC 999` | 10 |
| `MARC 950` | 10 |
| `MARC 921` | 10 |
| `MARC 901` | 10 |
| `MARC 910` | 10 |
| `MARC 940` | 10 |
| `MARC 912` | 10 |
| `MARC 920` | 10 |
| `MARC 944` | 10 |
| `MARC 930` | 10 |
| `MARC 996` | 9 |
| `MARC 922` | 9 |
| `MARC 943` | 9 |
| `inScheme` | 8 |
| `MARC 969` | 8 |
| `(VIAF 996: not clustered with him, dropped)` | 7 |
| `MARC 955` | 7 |
| `MARC 951` | 7 |
| `MARC 945` | 7 |
| `MARC 946` | 7 |
| `MARC 948` | 7 |
| `https://api.w.org/` | 7 |
| `MARC 947` | 7 |
| `primaryTopic` | 5 |
| `MARC 700` | 5 |
| `MARC 941` | 5 |
| `MARC 993` | 5 |
| `publisher` | 5 |
| `inLanguage` | 5 |
| `MARC 960` | 5 |
| `MARC 942` | 4 |
| `MARC 909` | 4 |
| `MARC 919` | 4 |
| `about` | 4 |
| `mainEntity` | 4 |
| `inDataset` | 3 |
| `MARC 042` | 3 |
| `date` | 3 |
| `breadcrumb` | 3 |
| `isPartOf` | 3 |
| `isDefinedBy` | 3 |
| `usesVocabulary` | 3 |
| `isIdentifiedByAuthority` | 2 |
| `publication` | 2 |
| `altLabel/literalForm` | 2 |

## Vocabularies and formats (sites using each)

| vocabulary | sites |
|---|---|
| `LLM extraction` | 281 |
| `http://www.w3.org/1999/xhtml/vocab#` | 167 |
| `http://ogp.me/ns#` | 113 |
| `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | 72 |
| `http://schema.org/` | 50 |
| `http://www.w3.org/2004/02/skos/core#` | 20 |
| `http://ogp.me/ns/fb#` | 20 |
| `http://www.w3.org/2000/01/rdf-schema#` | 19 |
| `http://purl.org/dc/terms/` | 17 |
| `MARC21 authority` | 17 |
| `MARC 100` | 17 |
| `MARC 400` | 15 |
| `MARC 035` | 15 |
| `http://xmlns.com/foaf/0.1/` | 13 |
| `MARC 040` | 13 |
| `http://www.w3.org/2002/07/owl#` | 12 |
| `MARC 998` | 11 |
| `MARC 997` | 11 |
| `MARC 670` | 10 |
| `MARC 046` | 10 |
| `MARC 999` | 10 |
| `MARC 950` | 10 |
| `MARC 921` | 10 |
| `MARC 901` | 10 |
| `MARC 910` | 10 |
| `MARC 940` | 10 |
| `MARC 912` | 10 |
| `MARC 920` | 10 |
| `MARC 944` | 10 |
| `MARC 930` | 10 |
| `MARC 024` | 9 |
| `MARC 370` | 9 |
| `MARC 374` | 9 |
| `MARC 377` | 9 |
| `https://dev.twitter.com/cards#` | 9 |
| `MARC 996` | 9 |
| `MARC 922` | 9 |
| `MARC 943` | 9 |
| `MARC 375` | 8 |
| `MARC 969` | 8 |
| `MARC 500` | 7 |
| `MARC 955` | 7 |
| `MARC 951` | 7 |
| `MARC 945` | 7 |
| `MARC 946` | 7 |
