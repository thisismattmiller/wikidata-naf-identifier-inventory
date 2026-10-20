# Q7245 (Mark Twain): sites vs Wikidata

297 sites with data representations compared against Wikidata.

## Element coverage and agreement

| element | sites with it | match | partial | mismatch | URI only | site only | Wikidata has |
|---|---|---|---|---|---|---|---|
| name_preferred | 281 | 274 | 6 | 1 | 0 | 0 | 88 values |
| name_variant | 222 | 216 | 5 | 1 | 0 | 0 | 71 values |
| given_name | 67 | 29 | 38 | 0 | 0 | 0 | 2 values |
| family_name | 66 | 61 | 5 | 0 | 0 | 0 | 3 values |
| pseudonym | 134 | 132 | 0 | 2 | 0 | 0 | 5 values |
| birth_date | 250 | 148 | 101 | 1 | 0 | 0 | 1 values |
| death_date | 245 | 145 | 96 | 4 | 0 | 0 | 1 values |
| birth_place | 139 | 49 | 88 | 1 | 1 | 0 | 1 values |
| death_place | 108 | 50 | 55 | 3 | 0 | 0 | 1 values |
| gender | 68 | 66 | 0 | 0 | 2 | 0 | 1 values |
| occupation | 202 | 179 | 17 | 6 | 0 | 0 | 16 values |
| nationality | 156 | 128 | 27 | 1 | 0 | 0 | 1 values |
| language | 51 | 45 | 2 | 4 | 0 | 0 | 2 values |
| work | 213 | 133 | 0 | 80 | 0 | 0 | 2 values |
| related_agent | 170 | 53 | 0 | 117 | 0 | 0 | 8 values |
| image | 62 | 0 | 0 | 0 | 0 | 0 | 2 values |
| description | 197 | 0 | 0 | 0 | 0 | 0 | 71 values |
| source | 135 | 0 | 0 | 0 | 0 | 135 | 0 values |
| see_also | 51 | 0 | 0 | 0 | 0 | 0 | 252 values |
| field_of_activity | 70 | 0 | 0 | 0 | 0 | 0 | 2 values |
| activity_place | 91 | 0 | 0 | 0 | 0 | 0 | 2 values |
| subject_of | 15 | 0 | 0 | 0 | 0 | 15 | 0 values |

## Mismatches worth a look

- **Freebase ID** death_place: site `Stormfield@en` vs Wikidata `Redding`
- **DBNL author ID** birth_place: site `Missiouri@nl` vs Wikidata `Florida`
- **Enciclopédia Açoriana ID** death_date: site `1910-04-02@pt` vs Wikidata `1910-04-21`
- **Filmportal ID** death_date: site `1910-02-21@en` vs Wikidata `1910-04-21`
- **Vienna History Wiki ID** death_date: site `1910-05-12 ‖ 2418803.5 ‖ 1910-05-12@de` vs Wikidata `1910-04-21`
- **Media Arts Database ID** name_preferred: site `TwainMark@en` vs Wikidata `ማርክ ትዌይን@am ‖ مارك توين@ar ‖ مارك توين@arz ‖ মাৰ্ক টোৱেইন@as ‖ Mark Tven@az ‖ Ма`
- **Union Catalog of Armenian Libraries authority ID** death_place: site `Ռեդդինգ, Քոնեքթիքութի նահանգ@hy` vs Wikidata `Redding`
- **Encyclopedia of China (Third Edition) old ID (2021)** birth_date: site `1835-11-31` vs Wikidata `1835-11-30`
- **Kinobox person ID** death_date: site `1910-04-20@cs` vs Wikidata `1910-04-21`
- **Arab Encyclopedia concept ID** death_place: site `ريدنغ في ولاية كونيتكت@ar ‖ ريدنغ، كونيتكت@ar` vs Wikidata `Redding`

## Partial agreement (less precise, or different form)

- VIAF cluster ID birth_place: `Florida, Mo.@en` ~ `Florida`
- VIAF cluster ID death_place: `Redding, Conn.@en` ~ `Redding`
- GND ID birth_place: `https://d-nb.info/gnd/110640968X ‖ Florida, MO.@en` ~ `Florida`
- GND ID death_place: `https://d-nb.info/gnd/1025527097 ‖ Redding, CON.@en` ~ `Redding`
- Library of Congress Authorities ID birth_place: `Florida (Mo.) ‖ Florida (Mo.)@en` ~ `Florida`
- Library of Congress Authorities ID death_place: `Redding (Conn.) ‖ http://id.loc.gov/rwo/agents/n85137334 ‖ Redding (Conn.)@en` ~ `Redding`
- Union List of Artist Names ID birth_date: `1835` ~ `1835-11-30`
- Union List of Artist Names ID death_date: `1910` ~ `1910-04-21`
- Bibliothèque nationale de France ID birth_place: `Florida (Missouri, États-Unis)@fr` ~ `Florida`
- Bibliothèque nationale de France ID death_place: `Redding (Connecticut, États-Unis)@fr` ~ `Redding`
- IMDb ID birth_place: `Florida, Missouri, USA@en` ~ `Florida`
- IMDb ID death_place: `Redding, Connecticut, USA@en` ~ `Redding`
- NDL Authority ID birth_date: `1835` ~ `1835-11-30`
- NDL Authority ID death_date: `1910` ~ `1910-04-21`
- SBN author ID death_place: `Redding, Connetticut@it` ~ `Redding`
- MusicBrainz artist ID birth_place: `Monroe County ‖ http://musicbrainz.org/area/079b04ff-50c6-4c30-a88b-1d3b813182aa ‖ Monroe County, Mi` ~ `Florida`
- MusicBrainz artist ID nationality: `US / American@en` ~ `United States`
- Find a Grave memorial ID birth_place: `Florida, Monroe County, Missouri, USA ‖ Florida, Monroe County, Missouri, USA@en` ~ `Florida`
- Find a Grave memorial ID death_place: `Redding, Fairfield County, Connecticut, USA ‖ Redding, Fairfield County, Connecticut, USA@en` ~ `Redding`
- NL CR AUT ID birth_date: `1835` ~ `1835-11-30`
- NL CR AUT ID death_date: `1910` ~ `1910-04-21`
- NL CR AUT ID nationality: `americký@cs` ~ `United States`
- DBNL author ID occupation: `boekdrukker/uitgever ‖ journalist/redacteur` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- Perlentaucher ID birth_date: `1835@en` ~ `1835-11-30`
- Perlentaucher ID death_date: `1910@en` ~ `1910-04-21`
- Perlentaucher ID birth_place: `Florida, USA@en` ~ `Florida`
- SELIBR ID birth_date: `1835` ~ `1835-11-30`
- SELIBR ID death_date: `1910` ~ `1910-04-21`
- SELIBR ID occupation: `Skönlitterär författare@sv ‖ tidningsman@sv` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- RSL ID (person) birth_date: `1835` ~ `1835-11-30`
- RSL ID (person) death_date: `1910` ~ `1910-04-21`
- National Library of Spain SpMaBN ID birth_date: `1835` ~ `1835-11-30`
- National Library of Spain SpMaBN ID death_date: `1910` ~ `1910-04-21`
- National Library of Spain SpMaBN ID birth_place: `Estados Unidos, Missouri (Estado), Monroe (Condado), Florida ‖ Estados Unidos, Missouri (Estado), Mo` ~ `Florida`
- National Library of Spain SpMaBN ID death_place: `Estados Unidos, Connecticut (Estado), Fairfield (Condado), Redding ‖ Estados Unidos, Connecticut (Es` ~ `Redding`
- Nationale Thesaurus voor Auteursnamen ID birth_date: `1835` ~ `1835-11-30`
- Nationale Thesaurus voor Auteursnamen ID death_date: `1910` ~ `1910-04-21`
- BIBSYS ID birth_date: `1835` ~ `1835-11-30`
- BIBSYS ID death_date: `1910` ~ `1910-04-21`
- Vatican Library ID (former scheme) birth_date: `1835` ~ `1835-11-30`
- Vatican Library ID (former scheme) death_date: `1910` ~ `1910-04-21`
- Rodovid ID birth_place: `Florida (Missouri), Missouri@en` ~ `Florida`
- Rodovid ID death_place: `Redding (Connecticut), Connecticut@en` ~ `Redding`
- NUKAT ID birth_date: `1835` ~ `1835-11-30`
- NUKAT ID death_date: `1910` ~ `1910-04-21`
- NLC authorities birth_date: `1835` ~ `1835-11-30`
- NLC authorities death_date: `1910` ~ `1910-04-21`
- NLC authorities birth_place: `Florida, Missouri, USA@en` ~ `Florida`
- Internet Broadway Database person ID birth_place: `Florida, Missouri, USA@en` ~ `Florida`
- Internet Broadway Database person ID death_place: `Redding, Connecticut, USA@en` ~ `Redding`
- Internet Broadway Database person ID occupation: `Writer Source Material@en` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- U.S. National Archives Identifier birth_date: `1835 ‖ 1835-01-01` ~ `1835-11-30`
- U.S. National Archives Identifier death_date: `1910 ‖ 1910-12-31 ‖ 1910-01-01` ~ `1910-04-21`
- ISFDB author ID birth_place: `Florida, Missouri, USA@en` ~ `Florida`
- KulturNav-ID nationality: `amerikansk@sv` ~ `United States`
- Swedish Open Cultural Heritage URI birth_date: `1835` ~ `1835-11-30`
- CONOR.SI ID birth_date: `1835` ~ `1835-11-30`
- CONOR.SI ID death_date: `1910` ~ `1910-04-21`
- EGAXA ID birth_place: `ميسوري ‖ ميسوري@ar` ~ `Florida`
- NLA Trove people ID birth_date: `1835` ~ `1835-11-30`
- NLA Trove people ID death_date: `1910` ~ `1910-04-21`
- NSK (VIAF) ID nationality: `američki@hr` ~ `United States`
- Enciclopédia Açoriana ID birth_place: `Florida, Missouri, Estados Unidos da América@pt` ~ `Florida`
- Enciclopédia Açoriana ID death_place: `Redding, Connecticut, Estados Unidos da América@pt` ~ `Redding`
- Encyclopædia Britannica Online ID birth_place: `Florida, Missouri, U.S.@en` ~ `Florida`
- Open Plaques subject ID birth_date: `1835` ~ `1835-11-30`
- Open Plaques subject ID death_date: `1910` ~ `1910-04-21`
- At the Circulating Library ID birth_date: `1835` ~ `1835-11-30`
- At the Circulating Library ID death_date: `1910` ~ `1910-04-21`
- National Portrait Gallery (London) person ID birth_date: `1835` ~ `1835-11-30`
- National Portrait Gallery (London) person ID death_date: `1910` ~ `1910-04-21`
- CCAB ID birth_date: `1835` ~ `1835-11-30`
- CCAB ID death_date: `1910` ~ `1910-04-21`
- Discogs artist ID birth_place: `Florida, Missouri, USA@en` ~ `Florida`
- Discogs artist ID death_place: `Redding, Connecticut, USA@en` ~ `Redding`
- FAST ID birth_place: `Florida (Mo.)` ~ `Florida`
- FAST ID death_place: `Redding (Conn.)` ~ `Redding`
- FAST ID occupation: `Authors Lecturers Humorists` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- BiblioNet author ID birth_date: `1835@el` ~ `1835-11-30`
- BiblioNet author ID death_date: `1910@el` ~ `1910-04-21`
- PORT person ID birth_place: `Amerikai Egyesült Államok, Florida, Missouri ‖ Amerikai Egyesült Államok, Florida, Missouri@hu` ~ `Florida`
- PORT person ID death_place: `Amerikai Egyesült Államok, Redding, Connecticut ‖ Amerikai Egyesült Államok, Redding, Connecticut@hu` ~ `Redding`
- BabelNet ID birth_date: `1835@en` ~ `1835-11-30`
- BabelNet ID death_date: `1910@en` ~ `1910-04-21`
- ČSFD person ID birth_place: `Florida, Missouri, USA ‖ Florida, Missouri, USA@cs` ~ `Florida`
- ČSFD person ID death_place: `Redding, Connecticut, USA ‖ Redding, Connecticut, USA@cs` ~ `Redding`
- ČSFD person ID nationality: `Americký@cs` ~ `United States`
- BookBrainz author ID birth_place: `Monroe County@en` ~ `Florida`
- Filmportal ID birth_place: `Florida, Missouri, USA@en` ~ `Florida`
- Filmportal ID death_place: `Redding, Connecticut, USA@en` ~ `Redding`
- Filmportal ID occupation: `script@en` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- BVMC person ID birth_date: `https://data.cervantesvirtual.com/date/1835 ‖ 1835` ~ `1835-11-30`
- BVMC person ID death_date: `https://data.cervantesvirtual.com/date/1910 ‖ 1910` ~ `1910-04-21`
- FamilySearch person ID birth_place: `Florida, Monroe, Missouri, United States ‖ Florida, Monroe, Missouri, United States@en` ~ `Florida`
- FamilySearch person ID death_place: `Redding, Fairfield, Connecticut, United States ‖ Redding, Fairfield, Connecticut, United States@en` ~ `Redding`
- Great Russian Encyclopedia Online ID (2017) birth_place: `Флорида, штат Миссури@ru` ~ `Florida`
- Great Russian Encyclopedia Online ID (2017) death_place: `Реддинг, штат Коннектикут@ru` ~ `Redding`
- Great Russian Encyclopedia Online ID (2017) nationality: `американский@ru` ~ `United States`
- WikiTree person ID birth_place: `Florida, Monroe, Missouri, United States@en` ~ `Florida`
- WikiTree person ID death_place: `Redding, Fairfield, Connecticut, United States@en` ~ `Redding`
- Goodreads author ID birth_place: `Florida, Missouri, The United States@en` ~ `Florida`
- National Library of Wales Authority ID birth_date: `1835` ~ `1835-11-30`
- National Library of Wales Authority ID death_date: `1910` ~ `1910-04-21`
- RERO ID (legacy) birth_date: `1835` ~ `1835-11-30`
- RERO ID (legacy) death_date: `1910` ~ `1910-04-21`
- Encyclopædia Universalis ID birth_date: `1835` ~ `1835-11-30`
- Encyclopædia Universalis ID death_date: `1910` ~ `1910-04-21`
- Encyclopædia Universalis ID nationality: `Écrivains des États-Unis d'Amérique@fr` ~ `United States`
- NE.se ID nationality: `amerikansk@sv` ~ `United States`
- Encyclopedia of Surfing ID birth_date: `1835` ~ `1835-11-30`
- National Library of Greece ID birth_place: `Φλόριντα της πολιτείας Μιζούρι@el` ~ `Florida`
- National Library of Greece ID occupation: `Συγγραφείς@el ‖ Δημοσιογράφοι@el ‖ Τυπογράφοι@el` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- Prabook ID death_date: `1910@en` ~ `1910-04-21`
- Prabook ID birth_place: `Florida, Missouri, United States@en` ~ `Florida`
- BNMM authority ID birth_place: `Florida (Estados Unidos : Estado)@es ‖ Florida (Missouri)@es` ~ `Florida`
- BNMM authority ID death_place: `Connecticut (Estados Unidos : Estado)@es ‖ Redding, Conn@es` ~ `Redding`
- Dictionary of Sydney ID birth_place: `Florida, Missouri, United States of America@en` ~ `Florida`
- DBC author ID birth_date: `1835` ~ `1835-11-30`
- DBC author ID death_date: `1910` ~ `1910-04-21`
- Open Library subject ID birth_date: `1835` ~ `1835-11-30`
- Open Library subject ID death_date: `1910` ~ `1910-04-21`
- BHL creator ID birth_date: `1835` ~ `1835-11-30`
- BHL creator ID death_date: `1910` ~ `1910-04-21`
- WeRelate person ID birth_place: `Florida, Monroe, Missouri, United States@en` ~ `Florida`
- WeRelate person ID death_place: `Redding, Fairfield, Connecticut, United States@en` ~ `Redding`
- Treccani's Enciclopedia Italiana ID birth_place: `Florida (Missouri)@it` ~ `Florida`
- Great Norwegian Encyclopedia ID birth_place: `Florida, Missouri, USA@nb` ~ `Florida`
- Great Norwegian Encyclopedia ID death_place: `Redding, Conneticut, USA@nb` ~ `Redding`
- Great Norwegian Encyclopedia ID nationality: `amerikansk@nb` ~ `United States`
- gravsted.dk ID birth_place: `Florida, Missouri, USA@da` ~ `Florida`
- gravsted.dk ID death_place: `Redding, Connecticut, USA@da` ~ `Redding`
- gravsted.dk ID nationality: `amerikansk@da` ~ `United States`
- Itaú Cultural ID birth_place: `Estados Unidos / Missouri / Florida@pt` ~ `Florida`
- Itaú Cultural ID death_place: `Estados Unidos / Connecticut / Redding@pt` ~ `Redding`
- Itaú Cultural ID occupation: `Escritora / Escritor@pt` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- Google Doodle birth_date: `11-30@en` ~ `1835-11-30`
- Artists of the World ID birth_place: `Florida (Missouri)` ~ `Florida`
- DAHR artist ID birth_place: `Florida (village in Missouri, United States of America)@en` ~ `Florida`
- DAHR artist ID death_place: `Redding (town in Fairfield County, Connecticut, United States)@en` ~ `Redding`
- Africultures person ID occupation: `Ecrivain/ne@fr` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- Online Books Page author ID birth_date: `1835` ~ `1835-11-30`
- Online Books Page author ID death_date: `1910` ~ `1910-04-21`
- CineMagia person ID birth_place: `Florida, Missouri, S.U.A.@ro ‖ Florida, Missouri, USA@ro` ~ `Florida`
- TMDB person ID birth_place: `Florida, Missouri, USA@en` ~ `Florida`
- Brockhaus Enzyklopädie online ID birth_place: `Florida (Missouri)@en` ~ `Florida`
- National Library of Korea ID birth_date: `1835` ~ `1835-11-30`
- National Library of Korea ID death_date: `1910` ~ `1910-04-21`
- National Library of Korea ID birth_place: `미국 (플로리다) ‖ 미국 (플로리다)@ko` ~ `Florida`
- National Library of Korea ID occupation: `소설가[小說家] ‖ 발명가[發明家] ‖ 작가(사람)[作家] ‖ 소설가[小說家]@ko ‖ 작가(사람)[作家]@ko ‖ 발명가[發明家]@ko` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- Interlingual Index ID birth_date: `1835` ~ `1835-11-30`
- Interlingual Index ID death_date: `1910` ~ `1910-04-21`
- Poetry Foundation ID birth_date: `1835@en` ~ `1835-11-30`
- Poetry Foundation ID death_place: `near Redding, Connecticut@en` ~ `Redding`
- Poets.org poet ID death_place: `near Redding, Connecticut@en` ~ `Redding`
- Fantastic Fiction author ID death_place: `Stormfield, near Redding, Connecticut@en` ~ `Redding`
- Trading Card Database name ID birth_place: `Florida, Missouri, USA@en` ~ `Florida`
- Latter-day Saint Literature database artist ID (archived) birth_date: `1835@en` ~ `1835-11-30`
- Latter-day Saint Literature database artist ID (archived) death_date: `1910@en` ~ `1910-04-21`
- BD Gest' author ID birth_place: `ÉTATS-UNIS@fr` ~ `Florida`
- Tebeosfera ID birth_place: `Florida · Monroe · Misuri@es` ~ `Florida`
- Tebeosfera ID death_place: `Redding · New Haven · Connecticut@es` ~ `Redding`
- NooSFere author ID birth_place: `Florida, Missouri, États-Unis@fr` ~ `Florida`
- NooSFere author ID death_place: `Redding, Connecticut, États-Unis@fr` ~ `Redding`
- Libris-URI birth_date: `1835` ~ `1835-11-30`
- Libris-URI death_date: `1910` ~ `1910-04-21`
- Libris-URI occupation: `Skönlitterär författare@sv ‖ tidningsman@sv` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- Evene ID birth_place: `État du Missouri@fr` ~ `Florida`
- LOA ID birth_date: `1835` ~ `1835-11-30`
- LOA ID death_date: `1910` ~ `1910-04-21`
- Angelicum ID birth_date: `1835` ~ `1835-11-30`
- Angelicum ID death_date: `1910` ~ `1910-04-21`
- Angelicum ID birth_place: `Hannibal (Mo.) ‖ Hannibal, Mo. ‖ US` ~ `Florida`
- Pontificia Università della Santa Croce ID birth_place: `Florida, Missouri (Stati Uniti)@it` ~ `Florida`
- Pontificia Università della Santa Croce ID death_place: `Redding, Connecticut (Stati Uniti)@it` ~ `Redding`
- Larousse ID birth_date: `1835` ~ `1835-11-30`
- Larousse ID death_date: `1910` ~ `1910-04-21`
- Fandom article ID birth_place: `Florida, Missouri, United States@en` ~ `Florida`
- Fandom article ID death_place: `Redding, Connecticut, United States@en` ~ `Redding`
- Krugosvet article (archived) birth_place: `village of Florida (Missouri)@en` ~ `Florida`
- ELNET ID birth_date: `1835` ~ `1835-11-30`
- ELNET ID death_date: `1910` ~ `1910-04-21`
- Douban author ID birth_place: `Florida, Missouri, United States@en` ~ `Florida`
- Klexikon article ID birth_date: `1835@de ‖ 1835@en` ~ `1835-11-30`
- Stedelijk Museum Amsterdam ID birth_date: `1835@nl` ~ `1835-11-30`
- Stedelijk Museum Amsterdam ID death_date: `1910@nl` ~ `1910-04-21`
- Alexander Turnbull Library ID birth_date: `1835` ~ `1835-11-30`
- Alexander Turnbull Library ID death_date: `1910` ~ `1910-04-21`
- Japan Search name ID birth_date: `time:1835 (1835) ‖ https://jpsearch.go.jp/entity/time/1835 ‖ 1835` ~ `1835-11-30`
- Japan Search name ID death_date: `time:1910 (1910) ‖ https://jpsearch.go.jp/entity/time/1910 ‖ 1910` ~ `1910-04-21`
- De Agostini ID birth_date: `1835@it ‖ 1835` ~ `1835-11-30`
- De Agostini ID death_date: `1910@it ‖ 1910` ~ `1910-04-21`
- Alvin ID birth_date: `1835` ~ `1835-11-30`
- Alvin ID death_date: `1910` ~ `1910-04-21`
- abART person ID birth_place: `Florida, Spojené státy (United States)@cs ‖ Florida (Missouri)@cs` ~ `Florida`
- abART person ID death_place: `Connecticut, Spojené státy (United States)@cs` ~ `Redding`
- abART person ID nationality: `americká@cs` ~ `United States`
- Lebanese National Library ID occupation: `الروائيون الصحفيون ‖ الروائيون@ar ‖ الصحفيون@ar` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- National Library of Poland MMS ID birth_date: `1835` ~ `1835-11-30`
- National Library of Poland MMS ID death_date: `1910` ~ `1910-04-21`
- National Library of Poland MMS ID occupation: `Pisarze amerykańscy@pl` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- Online PWN Encyclopedia ID birth_place: `Florida (stan Missouri)@pl` ~ `Florida`
- Online PWN Encyclopedia ID death_place: `Redding (stan Connecticut)@pl` ~ `Redding`
- Online PWN Encyclopedia ID nationality: `amerykański@pl` ~ `United States`
- Jeugdliteratuur ID birth_place: `Missouri (Florida)@nl` ~ `Florida`
- Jeugdliteratuur ID nationality: `Amerikaans@nl` ~ `United States`
- Ben Yehuda author ID birth_date: `1835` ~ `1835-11-30`
- Ben Yehuda author ID death_date: `1910` ~ `1910-04-21`
- Estonian biographical database ID birth_date: `1835` ~ `1835-11-30`
- Estonian biographical database ID death_date: `1910` ~ `1910-04-21`
- Filmový přehled person or company ID birth_place: `Florida, Missouri, USA@cs` ~ `Florida`
- Filmový přehled person or company ID death_place: `Redding, Connecticut, USA@cs` ~ `Redding`
- Online Nevada Encyclopedia ID birth_date: `1835` ~ `1835-11-30`
- Online Nevada Encyclopedia ID death_date: `1910` ~ `1910-04-21`
- National Library of Lithuania ID birth_place: `US, Missouri, Florida ‖ US, Missouri, Florida@en` ~ `Florida`
- National Library of Lithuania ID death_place: `US, Connecticut, Redding ‖ US, Connecticut, Redding@en` ~ `Redding`
- Slovak National Library (VIAF) ID birth_place: `Florida (Mo.) ‖ Florida (Mo.)@sk ‖ Florida, Missouri, Spojené štáty americké@sk` ~ `Florida`
- Slovak National Library (VIAF) ID death_place: `Redding (Conn.) ‖ Redding (Conn.)@sk ‖ Redding, Connecticut, Spojené štáty americké@sk` ~ `Redding`
- Projekt Gutenberg-DE author ID birth_place: `Florida (Missouri)@de` ~ `Florida`
- Australian National Maritime Museum person ID birth_date: `1835@en` ~ `1835-11-30`
- Australian National Maritime Museum person ID death_date: `1910@en` ~ `1910-04-21`
- Vienna History Wiki ID birth_place: `Florida/Missouri ‖ Florida/Missouri@de` ~ `Florida`
- Vienna History Wiki ID death_place: `Redding, Connecticut, USA ‖ Redding, Connecticut, USA@de` ~ `Redding`
- DigitaltMuseum ID birth_date: `1835 ‖ 1835@sv` ~ `1835-11-30`
- DigitaltMuseum ID death_date: `1910 ‖ 1910@sv` ~ `1910-04-21`
- DigitaltMuseum ID nationality: `amerikansk@sv` ~ `United States`
- Media Arts Database ID birth_date: `1835` ~ `1835-11-30`
- Media Arts Database ID death_date: `1910` ~ `1910-04-21`
- Roglo person ID birth_place: `Hannibal, Marion Co., Missouri (USA)@en` ~ `Florida`
- Roglo person ID death_place: `Stormfield, Redding, Connecticut (USA)@en` ~ `Redding`
- Hrvatska enciklopedija ID nationality: `američki@hr` ~ `United States`
- Vatican Library VcBA ID birth_date: `1835` ~ `1835-11-30`
- Vatican Library VcBA ID death_date: `1910` ~ `1910-04-21`
- GeneaStar person ID birth_place: `Florida, Missouri, USA, United States@en` ~ `Florida`
- GeneaStar person ID death_place: `Redding, Connecticut, USA, United States@en` ~ `Redding`
- Canadiana Name Authority ID birth_date: `1835` ~ `1835-11-30`
- Canadiana Name Authority ID death_date: `1910` ~ `1910-04-21`
- J9U entity ID birth_place: `Florida (Montgomery County, N.Y. : Town)@en ‖ Florida [ מדינת Missouri, ארצות-הברית]@he` ~ `Florida`
- J9U entity ID death_place: `Redding (Conn. : Town)@en ‖ Redding [ מדינת Connecticut, ארצות הברית]@he` ~ `Redding`
- LiederNet author ID birth_date: `1835` ~ `1835-11-30`
- LiederNet author ID death_date: `1910` ~ `1910-04-21`
- Lex ID nationality: `amerikansk@da` ~ `United States`
- Archive Site Trinity College Cambridge ID birth_date: `1835` ~ `1835-11-30`
- Archive Site Trinity College Cambridge ID death_date: `1910` ~ `1910-04-21`
- Diamond Catalog ID for persons and organisations birth_date: `1835` ~ `1835-11-30`
- Diamond Catalog ID for persons and organisations death_date: `1910` ~ `1910-04-21`
- WordNet 3.1 Synset ID birth_date: `1835` ~ `1835-11-30`
- WordNet 3.1 Synset ID death_date: `1910` ~ `1910-04-21`
- Union Catalog of Armenian Libraries authority ID birth_place: `Ֆլորիդա, Միսսուրիի նահանգ@hy` ~ `Florida`
- CONOR.BG ID birth_date: `1835` ~ `1835-11-30`
- CONOR.BG ID death_date: `1910` ~ `1910-04-21`
- CONOR.SR ID birth_date: `1835` ~ `1835-11-30`
- CONOR.SR ID death_date: `1910` ~ `1910-04-21`
- CONOR.SR ID birth_place: `Флорида, Мисури@sr-Cyrl` ~ `Florida`
- CINE21 person ID occupation: `원작 (original author)@ko` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- Literary Encyclopedia ID birth_date: `1835` ~ `1835-11-30`
- Literary Encyclopedia ID death_date: `1910` ~ `1910-04-21`
- Literary Encyclopedia ID nationality: `американский@ru` ~ `United States`
- BHCL UUID birth_date: `1835` ~ `1835-11-30`
- BHCL UUID death_date: `1910` ~ `1910-04-21`
- BHCL UUID nationality: `Americký@cs` ~ `United States`
- SEARCH on line catalogue ID birth_date: `1835` ~ `1835-11-30`
- SEARCH on line catalogue ID death_date: `1910` ~ `1910-04-21`
- American Academy in Rome ID birth_date: `1835` ~ `1835-11-30`
- American Academy in Rome ID death_date: `1910` ~ `1910-04-21`
- Portal da Literatura ID birth_date: `1835@pt ‖ 1835` ~ `1835-11-30`
- Portal da Literatura ID death_date: `1910` ~ `1910-04-21`
- RILM ID death_place: `Redding, Connecticut, United States ‖ Redding, Connecticut, United States@en` ~ `Redding`
- RILM ID nationality: `American (US)@en` ~ `United States`
- Biblioteca Franco Serantini ID birth_date: `1835` ~ `1835-11-30`
- Biblioteca Franco Serantini ID death_date: `1910` ~ `1910-04-21`
- Provenio UUID birth_date: `1835` ~ `1835-11-30`
- Provenio UUID death_date: `1910` ~ `1910-04-21`
- Provenio UUID nationality: `Americký@cs` ~ `United States`
- Pontifical University of Salamanca ID birth_date: `1835` ~ `1835-11-30`
- Pontifical University of Salamanca ID death_date: `1910` ~ `1910-04-21`
- Cyprus University of Technology ID birth_date: `1835` ~ `1835-11-30`
- Cyprus University of Technology ID death_date: `1910` ~ `1910-04-21`
- SVKKL authority ID birth_date: `1835` ~ `1835-11-30`
- SVKKL authority ID death_date: `1910` ~ `1910-04-21`
- Portrait Archive ID occupation: `US-amerikanischer Schriftsteller@de` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- Portrait Archive ID nationality: `US-amerikanisch@de` ~ `United States`
- National Historical Museums of Sweden ID birth_date: `1835` ~ `1835-11-30`
- LTit person ID occupation: `Autore@it` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- GCD creator ID birth_place: `Florida, Missouri, United States@en` ~ `Florida`
- GCD creator ID death_place: `Redding, Connecticut, United States@en` ~ `Redding`
- Penguin Random House author ID birth_date: `1835 ‖ 1835@en` ~ `1835-11-30`
- Penguin Random House author ID death_date: `1910 ‖ 1910@en` ~ `1910-04-21`
- SNK ID birth_place: `Florida, Missouri, Spojené štáty americké@sk ‖ Florida (Mo.)@sk` ~ `Florida`
- SNK ID death_place: `Redding, Connecticut, Spojené štáty americké@sk ‖ Redding (Conn.)@sk` ~ `Redding`
- Kallías ID birth_date: `1835` ~ `1835-11-30`
- Kallías ID death_date: `1910` ~ `1910-04-21`
- Kalliope-Verbund (GND) ID birth_place: `Florida, Mo. ‖ Florida, Mo.@de` ~ `Florida`
- Kalliope-Verbund (GND) ID death_place: `Redding, Conn. ‖ Redding, Conn.@de` ~ `Redding`
- CANTIC ID birth_date: `1835` ~ `1835-11-30`
- CANTIC ID death_date: `1910` ~ `1910-04-21`
- George Eastman Museum people ID birth_date: `1835` ~ `1835-11-30`
- George Eastman Museum people ID death_date: `1910` ~ `1910-04-21`
- UAE University Libraries ID birth_place: `Florida, Mo. ‖ Florida, Mo.@en` ~ `Florida`
- UAE University Libraries ID death_place: `Redding, Conn. ‖ Redding, Conn.@en` ~ `Redding`
- Tabakalera ID birth_date: `1835` ~ `1835-11-30`
- Tabakalera ID death_date: `1910` ~ `1910-04-21`
- Academy of Athens authority ID birth_date: `1835` ~ `1835-11-30`
- Academy of Athens authority ID death_date: `1910` ~ `1910-04-21`
- National Library of Ireland ID birth_place: `Florida, Mo. ‖ Florida, Mo.@en` ~ `Florida`
- National Library of Ireland ID death_place: `Redding, Conn. ‖ Redding, Conn.@en` ~ `Redding`
- Sceneweb artist ID nationality: `Amerikansk@nb` ~ `United States`
- Mnemosine ID birth_date: `1835` ~ `1835-11-30`
- Mnemosine ID death_date: `1910` ~ `1910-04-21`
- Databazeknih.cz author ID birth_date: `1835-01-01 ‖ 1835` ~ `1835-11-30`
- Databazeknih.cz author ID death_date: `1910-01-01 ‖ 1910` ~ `1910-04-21`
- Databazeknih.cz author ID nationality: `americká@cs` ~ `United States`
- CBDB.cz author ID birth_place: `Florida (Missouri), USA ‖ Florida (Missouri), USA@cs` ~ `Florida`
- CBDB.cz author ID nationality: `americký@cs` ~ `United States`
- Encyclopedia of China (Third Edition) old ID (2021) birth_place: `密苏里州佛罗里达镇@zh` ~ `Florida`
- Encyclopedia of China (Third Edition) old ID (2021) death_place: `康涅狄格州雷丁@zh` ~ `Redding`
- FID performing arts ID birth_place: `Florida, Mo. ‖ Florida, Mo.@de` ~ `Florida`
- FID performing arts ID death_place: `Redding, Conn. ‖ Redding, Conn.@de` ~ `Redding`
- Radio France person ID birth_date: `1835@fr ‖ 1835` ~ `1835-11-30`
- Radio France person ID death_date: `1910@fr` ~ `1910-04-21`
- The Encyclopedia of Fantasy ID birth_date: `1835` ~ `1835-11-30`
- The Encyclopedia of Fantasy ID death_date: `1910` ~ `1910-04-21`
- Central Library of Volos authority ID birth_date: `1835` ~ `1835-11-30`
- Central Library of Volos authority ID death_date: `1910` ~ `1910-04-21`
- UOM ID birth_date: `1835` ~ `1835-11-30`
- UOM ID death_date: `1910` ~ `1910-04-21`
- AniList staff ID birth_place: `Florida, Missouri, USA@en` ~ `Florida`
- KBR person ID birth_date: `1835` ~ `1835-11-30`
- KBR person ID death_date: `1910` ~ `1910-04-21`
- Listal ID birth_place: `Florida Missouri USA@en` ~ `Florida`
- Ozon person ID birth_place: `Флорида, штат Миссури@ru` ~ `Florida`
- Pixiv Encyclopedia ID death_date: `1910@ja` ~ `1910-04-21`
- TV Maze person ID birth_place: `United States@en` ~ `Florida`
- TV Maze person ID occupation: `novelist (source material)@en` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- CiNii Research ID birth_place: `ミズーリ州フロリダ@ja` ~ `Florida`
- University of Barcelona authority ID birth_date: `1835` ~ `1835-11-30`
- University of Barcelona authority ID death_date: `1910` ~ `1910-04-21`
- The Literary Encyclopedia person ID birth_place: `United States@en` ~ `Florida`
- J. Paul Getty Museum agent ID birth_date: `1835` ~ `1835-11-30`
- J. Paul Getty Museum agent ID death_date: `1910` ~ `1910-04-21`
- WikiKids ID birth_place: `Florida (Missouri)@nl` ~ `Florida`
- WikiKids ID nationality: `Amerikaans@nl` ~ `United States`
- FilmAffinity person or company ID birth_place: `United States@en` ~ `Florida`
- FilmAffinity person or company ID death_place: `United States@en` ~ `Redding`
- Dansk Forfatterleksikon ID birth_date: `1835` ~ `1835-11-30`
- Dansk Forfatterleksikon ID death_date: `1910` ~ `1910-04-21`
- Arabic Ontology lexical concept ID birth_date: `1835` ~ `1835-11-30`
- Arabic Ontology lexical concept ID death_date: `1910` ~ `1910-04-21`
- PMB – Personen der Moderne Basis person ID occupation: `Schriftsteller/Schriftstellerin@de ‖ Journalist/Journalistin@de` ~ `journalist ‖ novelist ‖ autobiographer ‖ teacher ‖ humorist `
- UCA authority ID birth_date: `1835` ~ `1835-11-30`
- UCA authority ID death_date: `1910` ~ `1910-04-21`
- az.lib.ru author ID nationality: `американский@ru` ~ `United States`
- Vikidia article ID birth_place: `Florida, États-Unis@fr` ~ `Florida`
- Vikidia article ID death_place: `Redding, États-Unis@fr` ~ `Redding`
- Douban personage ID birth_place: `美国,密苏里州,佛罗里达州@zh` ~ `Florida`
- RedBA Granada authority ID birth_place: `Florida (Mo.)@es` ~ `Florida`
- RedBA Granada authority ID death_place: `Redding (Conn.)@es` ~ `Redding`
- DDB person (GND) ID birth_place: `Florida, Mo.@de` ~ `Florida`
- DDB person (GND) ID death_place: `Redding, Conn.@de` ~ `Redding`
- PUG authority ID birth_date: `1835` ~ `1835-11-30`
- PUG authority ID death_date: `1910` ~ `1910-04-21`
- JudaicaLink person (GND) ID birth_date: `1835` ~ `1835-11-30`
- JudaicaLink person (GND) ID death_date: `1910` ~ `1910-04-21`
- JudaicaLink person (GND) ID birth_place: `Florida, Mo.` ~ `Florida`
- JudaicaLink person (GND) ID death_place: `Redding, Conn.` ~ `Redding`
- Wellcome Collection concept ID birth_date: `1835` ~ `1835-11-30`
- Wellcome Collection concept ID death_date: `1910` ~ `1910-04-21`
- Arab Encyclopedia concept ID birth_date: `1835` ~ `1835-11-30`
- Arab Encyclopedia concept ID death_date: `1910` ~ `1910-04-21`
- Arab Encyclopedia concept ID birth_place: `فلوريدا وهي قرية صغيرة في ولاية ميسوري@ar ‖ فلوريدا، ميسوري@ar` ~ `Florida`
- ‎Sancho el Sabio Foundation ID birth_place: `Florida, Misuri@es` ~ `Florida`
- Library of the University of Santiago de Compostela authority ID birth_date: `1835` ~ `1835-11-30`
- Library of the University of Santiago de Compostela authority ID death_date: `1910` ~ `1910-04-21`
- Foto Atlas taxonomy ID birth_date: `1835 ‖ 1835@en` ~ `1835-11-30`
- Foto Atlas taxonomy ID death_date: `1910 ‖ 1910@en` ~ `1910-04-21`
- NSK ID nationality: `Američki@hr` ~ `United States`
- ‎Darwin Correspondence ID birth_date: `1835` ~ `1835-11-30`
- ‎Darwin Correspondence ID death_date: `1910` ~ `1910-04-21`
- FES digital collections entity ID birth_place: `Florida, Mo.@en` ~ `Florida`
- FES digital collections entity ID death_place: `Redding, Conn.@en` ~ `Redding`
- Encyclopedia of China (Third Edition) ID (2026) birth_date: `1835-11` ~ `1835-11-30`
- Pontifical Urbaniana University ID birth_date: `1835` ~ `1835-11-30`
- Pontifical Urbaniana University ID death_date: `1910` ~ `1910-04-21`
- ‎HAND ID birth_date: `1835 ‖ 11 ‖ 30@day` ~ `1835-11-30`
- ‎HAND ID death_date: `1910 ‖ 4 ‖ 21@day` ~ `1910-04-21`

## What sites have that Wikidata does not

- **name_variant**: 866 site values with no Wikidata counterpart across 84 sites; most from VIAF cluster ID (102: `Jean François Alden ‖ Samuel Langhorn Clemens ‖ Jean Francois Alden ‖ `); GND ID (75: `Clemens, Samuel Langhorn 1835-1910 ‖ Klemens, Samuėlʹ 1835-1910 ‖ Kle`); ‎Yale LUX ID (56: `Marc Twain (1835-1910) ‖ Klemens, Seĭmeul Lenghorn, 1835-1910 ‖ Kʻo-la`); Library of Congress Authorities ID (51: `Tuwayn, Mārk, 1835-1910 ‖ Twayn, Mārk, 1835-1910 ‖ Tʻu-wen, Ma-kʻo, 18`); Kalliope-Verbund (GND) ID (51: `Twain, Marc (1835-1910) ‖ Twayn, Mark (1835-1910) ‖ Tuwen, Make (1835-`); Open Library ID (44: `Marc Twain ‖ Mark Twain, Zerrin Ozalp Oztarhan, Muge Kalender, Azadeh `)
- **name_preferred**: 73 site values with no Wikidata counterpart across 38 sites; most from VIAF cluster ID (13: `Autobiography of Mark Twain ‖ Autobiography of Mark Twain 1 ‖ Autobiog`); ISNI (7: `ISNI 0000 0001 0797 3778 ‖ ISNI 0000 0001 0800 0249 ‖ ISNI 0000 0001 0`); FamilySearch person ID (5: `Dorothy Quick and Mark Twain (Samuel Clemens) in 1907. ‖ Clara, Samuel`); BookBub author ID (4: `The Autobiography of Mark Twain ‖ The Wit and Wisdom of Mark Twain ‖ M`); Larousse ID (3: `Mark Twain – Média LAROUSSE ‖ Samuel Langhorne Clemens dit Mark Twain `); Online Nevada Encyclopedia ID (3: `Mark Twain: A Life ‖ A Companion to Mark Twain ‖ Mark Twain: The Bache`)
- **occupation**: 247 site values with no Wikidata counterpart across 105 sites; most from TMDB person ID (9: `Short Story ‖ Story ‖ Actor ‖ Original Story ‖ Characters ‖ Thanks ‖ O`); Douban author ID (7: `演说家 ‖ 排字工人 ‖ 水手 ‖ Translator ‖ orator ‖ typesetter ‖ sailor`); BookBrainz author ID (6: `essayist ‖ typesetter ‖ miner ‖ speaker ‖ entrepreneur ‖ publisher`); Sinemalar person ID (6: `Oyuncu ‖ Yönetmen ‖ Senarist ‖ Yapımcı ‖ Senarist (Kitap) ‖ Oyuncu, Yö`); Roglo person ID (6: `essayiste ‖ apprenti typographe ‖ chercheur d'or ‖ reporter ‖ correspo`); PORT person ID (5: `író, forgatókönyvíró, rendező ‖ forgatókönyvíró ‖ rendező ‖ hajós ‖ ar`)
- **work**: 3363 site values with no Wikidata counterpart across 207 sites; most from Library of Congress Authorities ID (782: `"The man who thought himself a woman" and other queer ninete ‖ A colle`); Slovak National Library (VIAF) ID (56: `Adventures of Tom Sawyer ‖ The Adventures of Huckleberry Finn ‖ Huckle`); VIAF cluster ID (53: `Pudd'nhead Wilson ‖ http://viaf.org/viaf/178306412 ‖ comedy those extr`); Geni profile ID (49: `The Celebrated Jumping Frog of Calaveras County ‖ The Innocents Abroad`); NLP ID (45: `Przygody Tomka Sawyera ‖ Królewicz i żebrak ‖ Pamiętniki Adama i Ewy ‖`); National Library of Poland MMS ID (44: `Przygody Tomka Sawyera ‖ Królewicz i żebrak ‖ Pamiętniki Adama i Ewy ‖`)
- **pseudonym**: 48 site values with no Wikidata counterpart across 36 sites; most from GND ID (7: `https://d-nb.info/gnd/118624822 ‖ https://d-nb.info/gnd/1106406737 ‖ h`); Encyclopædia Britannica Online ID (3: `W. Epaminondas Adrastus Perkins ‖ Quintius Curtius Snodgrass ‖ Josh`); NLP ID (3: `J. W. Bothwell, Thomas Jefferson Snodgrass, Sieur Louis de C ‖ Jean Fr`); BabelNet ID (3: `Sergeant Fathom ‖ Soleather ‖ W. Epaminondas Adrastus Blab`); ISNI (1: `Jean François Alden`); VIAF cluster ID (1: `Alden, Jean François`)
- **given_name**: 56 site values with no Wikidata counterpart across 4 sites; most from VIAF cluster ID (38: `Jean François ‖ Jean Francois ‖ Mak'ŭ ‖ Ma-k`o ‖ Ma-khu ‖ Maku ‖ Māku `); GND ID (16: `Samuel Langhorn ‖ Samuėlʹ ‖ Seĭmeul Lenghorn ‖ Sai-mi-erh Lang-en ‖ `); KulturNav-ID (1: `Samuel Mark`); DigitaltMuseum ID (1: `Samuel Mark`)
- **family_name**: 79 site values with no Wikidata counterpart across 7 sites; most from VIAF cluster ID (55: `Alden ‖ Langhorn Clemens ‖ Klemèns ‖ T'ŭwein ‖ T`u-wen ‖ Tewin ‖ Tho-w`); GND ID (19: `Klemens ‖ Kʻo-lan-man-ssu ‖ Alden ‖ Twayn ‖ Tuwen ‖ Towein ‖ Tvein ‖ T`); KulturNav-ID (1: `Langhorne Clemens Twain`); Swedish Open Cultural Heritage URI (1: `Langhorne, Mark Twain`); Libris-URI (1: `Twen`); DigitaltMuseum ID (1: `Langhorne Clemens Twain`)
- source: 135 sites, e.g. ISNI (`https://musicbrainz.org/artist/09b5de5d-52cf-426e-`); VIAF cluster ID (`0000000107973778 ‖ n93099461 ‖ http://d-nb.info/gn`); GND ID (`LCAuth`); Library of Congress Authorities ID (`Geviksman, V. A. Print︠s︡ i nishchiĭ, 1984: t.p. (`)
- activity_place: 91 sites, e.g. ISNI (`Hannibal, Missouri@en`); Library of Congress Authorities ID (`Hannibal (Mo.) ‖ United States@en ‖ Hannibal (Mo.)`); IMDb ID (`Hannibal@en ‖ Mississippi River@en`); MusicBrainz artist ID (`United States ‖ http://musicbrainz.org/area/489ce9`)
- field_of_activity: 70 sites, e.g. ISNI (`fiction@en ‖ historical fiction@en ‖ children's li`); GND ID (`12.2p People related to literary history (writers)`); Library of Congress Authorities ID (`Literature Humor - ‖ Wit and humor - ‖ PS1300 PS13`); Open Library ID (`Fiction@en ‖ Children's fiction@en ‖ American lite`)
- related_agent: 170 sites, e.g. ISNI (`Lyman Beecher (descendants of; recipients of corre`); VIAF cluster ID (`Orion Clemens@en ‖ Edgar Marquess Branch (1913-)@e`); GND ID (`Twain, Mark 1835-1910 Pseudonym ‖ Snodgrass, Quint`); Library of Congress Authorities ID (`Clemens, Samuel Langhorne 
       1835-1910 ‖ Snod`)

## Name scripts

| script | Wikidata labels/aliases | sites with names in it |
|---|---|---|
| Latin | 47 | 277 (Academy of Athens authority ID, Adelphi author ID, Africultures person ID, Alexander Turnbull Library ID, Alvin ID, American Academy in Rome ID) |
| Cyrillic | 39 | 42 (Archives at Yale agent ID, BAnQ authority ID, CONOR.BG ID, CONOR.SR ID, DBC author ID, Discogs artist ID) |
| Hebrew | 6 | 27 (Angelicum ID, Archives at Yale agent ID, BAnQ authority ID, Ben Yehuda author ID, DBC author ID, EGAXA ID) |
| Han | 12 | 26 (Angelicum ID, Archives at Yale agent ID, Douban author ID, Douban personage ID, Encyclopedia of China (Third Edition) ID (2026), Encyclopedia of China (Third Edition) old ID (2021)) |
| Arabic | 13 | 21 (Angelicum ID, Arab Encyclopedia concept ID, BAnQ authority ID, DBC author ID, EGAXA ID, ELNET ID) |
| Kana | 6 | 19 (Angelicum ID, AniList staff ID, CiNii Research ID, FID performing arts ID, GND ID, Japan Search name ID) |
| Hangul | 2 | 10 (Angelicum ID, CINE21 person ID, Library of Congress Authorities ID, NACSIS-CAT author ID, NLC authorities, National Library of Korea ID) |
| Greek | 5 | 7 (BiblioNet author ID, Europeana entity, National Library of Greece ID, Piraeus Bank Group Cultural Foundation Library (A) ID, VIAF cluster ID, WorldCat Entities ID) |
| Bengali | 3 | 6 (IMSLP ID, Library of Congress Authorities ID, NLC authorities, VIAF cluster ID, WorldCat Entities ID, museum-digital person/organization ID) |
| Devanagari | 6 | 5 (NACSIS-CAT author ID, VIAF cluster ID, WorldCat Entities ID, museum-digital person/organization ID, ‎Yale LUX ID) |
| Armenian | 1 | 4 (NLC authorities, Union Catalog of Armenian Libraries authority ID, VIAF cluster ID, WorldCat Entities ID) |
| Thai | 1 | 4 (NACSIS-CAT author ID, VIAF cluster ID, WorldCat Entities ID, museum-digital person/organization ID) |
| Ethiopic | 1 | 4 (IMSLP ID, J9U entity ID, VIAF cluster ID, WorldCat Entities ID) |
| Tamil | 1 | 3 (VIAF cluster ID, WorldCat Entities ID, museum-digital person/organization ID) |
| Georgian | 4 | 3 (VIAF cluster ID, WorldCat Entities ID, museum-digital person/organization ID) |
| Telugu | 2 | 3 (VIAF cluster ID, WorldCat Entities ID, museum-digital person/organization ID) |
| Gurmukhi | 2 | 2 (VIAF cluster ID, WorldCat Entities ID) |
| Burmese | 2 | 2 (VIAF cluster ID, WorldCat Entities ID) |
| Malayalam | 1 | 2 (VIAF cluster ID, WorldCat Entities ID) |
| Ol | 2 | 2 (VIAF cluster ID, WorldCat Entities ID) |
| Kannada | 1 | 2 (VIAF cluster ID, WorldCat Entities ID) |
| Gujarati | 1 | 2 (VIAF cluster ID, WorldCat Entities ID) |
| Oriya | 1 | 2 (VIAF cluster ID, WorldCat Entities ID) |

## Languages

Wikidata has labels in 91 languages plus a `mul` label (`Mark Twain`) that covers every language where the name is spelled that way, aliases in 30, descriptions in 71.
Sites tag values with 228 distinct language codes; most used: en (546), he (77), ru (73), fr (61), cs (50), it (47), zh (45), ar (43), ja (42), de (37), ca (35), es (34), sv (33), el (29), nl (28), und-latn (24), pl (21), yi (19), da (19), zh-Latn (18).

Languages in which sites carry name forms that Wikidata has in no label or alias (count of forms; examples):

- en: 49 — `Twain, Mark, pseud.` (VIAF cluster ID); `Clemens, Samuel Langhorn, 1835-1910` (VIAF cluster ID); `Clemens, Mark Twain` (Union List of Artist Name)
- he: 26 — `טבןַ, מרק` (ISNI); `טוויין, מרק` (ISNI); `טווין, מרק` (ISNI)
- und-latn: 21 — `Twjen, Mark` (GND ID); `Tuwayn, Mārk, 1835-1910` (Library of Congress Autho); `Twayn, Mārk, 1835-1910` (Library of Congress Autho)
- zh-Latn: 18 — `Kʻo-lan-man-ssu, Sai-mi-erh Lang-en` (ISNI); `(mei) Ma, ke tu wen` (Open Library ID); `(mei) Tuwen, Make` (Open Library ID)
- yi: 17 — `טווען, מארק` (ISNI); `טווען, מארק, 1835-1910` (Library of Congress Autho); `קלעמענס, סאמואל לאנגהארן, 1835-1910` (Library of Congress Autho)
- ca: 11 — `Alden, Jean François, 1835-1910` (University of Barcelona a); `Touen, Maku, 1835-1910` (University of Barcelona a); `Tuwayn, Mark, 1835-1910` (University of Barcelona a)
- ko: 8 — `마트웨인, 크` (NACSIS-CAT author ID); `마크트웨인 (1835~1910)` (NLC authorities); `클레멘스, 새뮤얼 랭혼` (National Library of Korea)
- und-hebr: 7 — `טוין, צרק` (GND ID); `קלמנס, סמואל, 1835-1910` (Library of Congress Autho); `טוויין, מרק, 1835-1910` (Library of Congress Autho)
- fr: 6 — `Twain, Marc (1835-1910)` (Bibliothèque nationale de); `Twain, Marc` (IdRef ID); `Alden, Jean François` (Pontificia Università del)
- ja: 6 — `トウエン, マーク` (NACSIS-CAT author ID); `トーウェン` (NDL Authority ID); `トゥエン, マーク` (NDL Authority ID)
- ar: 6 — `توين، مرك` (EGAXA ID); `كليمنس، صمويل لانجهورن` (EGAXA ID); `صمويل لانغهورن كليمنس (Samuel Langhorne ` (Lebanese National Library)
- lt: 6 — `Tvainas, Markas` (National Library of Lithu); `Tvėnas, Morkas` (National Library of Lithu); `Twainas, Markas` (National Library of Lithu)
- hy: 6 — `Մարկ Թվեյն, 1835-1910` (Union Catalog of Armenian); `Մ. Թուէյն (Ս. Քլէմընս), (Մարկ) 1835-1910` (Union Catalog of Armenian); `Մ. Տուէն (Սամուէլ Կլէմէնս), (Մարկ) 1835-` (Union Catalog of Armenian)
- ru: 5 — `Клеменс, Самуэль Лангхорн` (ISNI); `Клеменс, Самюэл Лангхорн` (ISNI); `Самюэль Клеменс` (Geni profile ID)
- pl: 5 — `Twain, Marek` (NUKAT ID); `Twain, Marek (1835-1910)` (NLA Trove people ID); `Marek Twain` (NLP ID)
- el: 5 — `Σάμιουελ Λόνγκχορν Κλέμενς` (BiblioNet author ID); `Κλήμενς, Σάμουελ, 1835-1910` (National Library of Greec); `Κλέμενς, Σάμιουελ Λάνγκορν, 1835-1910` (National Library of Greec)
- it: 4 — `Dixon Wecter` (Vegetti Catalog of Fantas); `Samuel Langhorn Clemens` (LTit person ID); `Twain, Mark, pseud. di Samuel Lanhorne C` (Parsifal cluster ID)
- zh: 4 — `萨缪尔·兰亨·克莱门` (Zhihu topic ID); `萨缪尔·兰亨·克莱门` (Douban author ID); `塞缪尔·朗赫恩·克莱门斯` (Encyclopedia of China (Th)
- sr-Cyrl: 4 — `Клеменс, Самјуел Лангхорн, 1835-1910` (CONOR.SR ID); `Клеменс, Семјуел Лангхорн, 1835-1910` (CONOR.SR ID); `Клеменс, Семјуел Ленгхорн, 1835-1910` (CONOR.SR ID)
- fa: 3 — `تواين، مارک` (ISNI); `تواين، مارک` (Library of Congress Autho); `تواين، مارک` (Angelicum ID)
- bn: 3 — `মার্ক টোয়েইন (1835~1910)` (NLC authorities); `মার্ক টোয়েইন` (WorldCat Entities ID); `মার্ক টোয়েইন` (museum-digital person/org)
- sl: 3 — `Twain, Marc` (CONOR.SI ID); `Tuen, Mark` (CONOR.SI ID); `Twen, Mark` (CONOR.SI ID)
- ru-Latn: 2 — `Klemens, Sami︠u︡ėl` (ISNI); `Klemens, Seĭmeul Lenghorn` (ISNI)
- und-arab: 2 — `تواين، مارک` (Library of Congress Autho); `تواين، مارک` (Library of Congress Autho)
- ja-Latn: 2 — `Māku Tuein` (Open Library ID); `Touen, Makū (1835-1910)` (NLA Trove people ID)

Sites provide descriptions in 60 languages; Wikidata has no description in: bio (Open Library ID, SNK ID), da (Dansk Forfatterleksikon ID, Lex ID, gravsted.dk ID), et (ELNET ID), lt (National Library of Lithuania ID), nb (BIBSYS ID, Geni profile ID, Great Norwegian Encyclopedia ID), no (Geni profile ID), pnx (NSK ID), sw (museum-digital person/organization ID), ta (museum-digital person/organization ID), th (museum-digital person/organization ID), tl (museum-digital person/organization ID), tr (Foto Atlas taxonomy ID, Sinemalar person ID, museum-digital person/organization ID), ur (museum-digital person/organization ID), vi (museum-digital person/organization ID)

## Cross-links asserted by sites

553 links from 86 sites: match: 354, not an id of that system: 141, unknown system: 42, different value: 16


Identifiers where the site points at a different value than Wikidata holds:
- VIAF cluster ID → ISNI = `0000000418649406` (Wikidata: 0000000077209145, 0000000107973778, 0000000108000249, 0000000108003124, 00000001)
- GND ID → VIAF cluster ID = `9358167867532223060005` (Wikidata: 16444837, 305239133, 50566653, 53367783)
- Library of Congress Authorities ID → FAST ID = `1986616` (Wikidata: 31622)
- Library of Congress Authorities ID → ISNI = `0000000418649406` (Wikidata: 0000000077209145, 0000000107973778, 0000000108000249, 0000000108003124, 00000001)
- NACSIS-CAT author ID → NACSIS-CAT author ID = `DA03513635` (Wikidata: DA00300263)
- NACSIS-CAT author ID → NACSIS-CAT author ID = `DA04621156` (Wikidata: DA00300263)
- MusicBrainz artist ID → MusicBrainz artist ID = `09b5de5d-52cf-426e-b457-ceba78379502` (Wikidata: 4d584c99-249e-493f-8c5f-d022bd8de433)
- Nationale Thesaurus voor Auteursnamen ID → VIAF cluster ID = `280780420` (Wikidata: 16444837, 305239133, 50566653, 53367783)
- Nationale Thesaurus voor Auteursnamen ID → Nationale Thesaurus voor Auteursnamen ID = `068242956` (Wikidata: 068242964, 227880145)
- WikiTree person ID → WikiTree person ID = `Clemens-12` (Wikidata: Clemens-1)
- DBC author ID → ISNI = `0000000418649406` (Wikidata: 0000000077209145, 0000000107973778, 0000000108000249, 0000000108003124, 00000001)
- Archives at Yale agent ID → SNAC ARK ID = `w6988t7g` (Wikidata: w65h7dgf, w6dg7gd6)
- National Library of Ireland ID → IdRef ID = `137182333` (Wikidata: 027171876)
- CiNii Research ID → NACSIS-CAT author ID = `DA03513635` (Wikidata: DA00300263)
- CiNii Research ID → NACSIS-CAT author ID = `DA04621156` (Wikidata: DA00300263)
- ‎Yale LUX ID → Library of Congress Authorities ID = `n82045653` (Wikidata: n79021164, n93099439, n93099461, no2003079632)

Same-as targets not recognised as any Wikidata identifier property (top hosts): dbpedia.org (8), id.loc.gov (5), data.bnf.fr (4), id.ndl.go.jp (3), www.isni.org (2), nlg.okfn.gr (2), de.wikipedia.org (2), en.wikipedia.org (2), data.bibsys.no (1), fr.wikipedia.org (1), viaf.org (1), nla.gov.au (1), www.ibdb.com (1), api.discogs.com (1), data.muziekschatten.nl (1), ja.dbpedia.org (1), www.freebase.com (1), g.co (1), data.carnegiehall.org (1), www.britishmuseum.org (1), hub.culturegraph.org (1), de.wikisource.org (1)

## Data-quality observations in the sources

- VIAF's RDF emits `schema:alternateName` as given+family name concatenated without a space (`Jean FrançoisAlden`, `Samuel LanghorneClemens`).
- Several sites encode year-only dates as 1 January (Databazeknih `1835-01-01`) or as a range end (NARA `1910-12-31`).
- Genealogy sites (WikiTree, Find a Grave, FamilySearch) expose relatives' records as same-as/see-also links, which look like conflicting identifiers unless filtered.
- Wikidata's own property formatters route some sites through redirectors (toolforge) and several sites' TLS certificates or hosts are broken (see `inventory.md`).

## Judged disagreements (Opus review pass)

Every mismatch, partial date/place and cross-link disagreement above was judged individually; full verdicts in `review.json`, write-up in `review.md`. Summary:


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


## Files

- `comparison.csv` — site × element with values on both sides
- `comparison_matrix.csv` — status grid
- `crosslinks.csv` — every same-as link, resolved
- `vocabulary_mapping.csv` / `vocabulary_mapping.md` — site predicate/field → element → Wikidata property
- `review.json` / `review.md` — judged verdicts on every disagreement (Opus review pass)
- `wikidata_elements.json`, `profiles/*.json` — the two sides in full
