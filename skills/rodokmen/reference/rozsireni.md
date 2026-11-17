# Rozšíření forku (jandadik) – podrobnosti k pravidlům v SKILL.md

Fork skillu sarsonj/rodokmen-skill. Navíc oproti původnímu skillu: pravidla „pracuj sám“ a vytěžení všeho, co řekl
uživatel (převzato z micl79/rodokmen-skill), nástroje `fronta.py`, `kmotri.py`, `oprav_odkazy.py`, `knihovna.py`,
návody `pomocnici.md`, `souvislosti.md`, `lokalni_knihovna.md` a rozšíření webu (Celý strom, více příběhů, portréty).

## Fáze 0.5 – Okamžité vytěžení všeho, co uživatel řekl (před čímkoli dalším)
Každý údaj od uživatele (jméno, rok, místo, příjmení matky, „pocházela z…“, „bratři byli…“) je **hotová stopa do matriky**.
Nečekej, až tě uživatel navede. Hned po prvním rozhovoru (a po každé nové informaci):
1. **Fronta výchozích osob.** Do `data/STAV.md` → „Fronta“ zapiš KAŽDOU osobu, o které uživatel něco řekl (i manželku, tchána,
   babičku z druhé strany), s tím, co víš: rok, místo, rodiče, sourozenci. Žádná větev se nevynechá jen proto, že je „vedlejší“.
2. **Pro každou osobu urči nejbližší přístupný zápis** (lhůty: narození 100 let, sňatek 75, úmrtí 30) a hned ho hledej:
   - narozen před ~1925 → **zápis o narození** v místě, které uživatel řekl;
   - narozen později → **sňatek rodičů** (online po 75 letech) v místě a letech kolem narození, případně narození
     starších sourozenců; tím získáš jména rodičů i jejich původ;
   - rok úmrtí > 30 let zpět → úmrtní zápis (uvádí narození a rodiče).
   Příklad: „Jan Novák * 1946, maminka Ludmila z Lhoty“ → hned sňatky Novák × Ludmila ve Lhotě a okolí 1935–1946
   (katolické, evangelické i civilní), ne až na pokyn.
3. **Místo převeď na všechny možné obce a archivy.** Stejný název (Sázava, Libčice, Lhota…) bývá v několika krajích – vypiš
   všechny kandidáty (`aron_search.py`, `portafontium.py obec`, vyhledávání obcí v prohlížeči SOA Třeboň, SOA Praha a MZA)
   a seřaď je podle toho, co uživatel řekl („na Vysočině“, „pod Křemešníkem“, „u Kralup“). Skutečná chyba: Sázava u Žďáru
   (MZA) místo Sázavy pod Křemešníkem (SOA Třeboň). Když hledání v jednom kandidátovi selže, zkus ostatní dřív, než začneš
   listovat knihy bez rejstříku.
4. **Nejdřív lokální knihovna a rejstříky** (`reference/lokalni_knihovna.md`, indexy v knihách), teprve pak listování.
5. **Každý nález hned rozvětvi:** rodiče, prarodiče a sourozence do fronty a pokračuj generaci po generaci všemi větvemi
   souběžně (pomocníci). Nečekej, až se uživatel zeptá „a co dál?“.
6. Teprve když fronta nemá žádný přístupný zápis, který by šel hledat, se ptej uživatele na další údaje.

## Brána před listováním naslepo
Než začneš listovat víc než ~20 snímků bez rejstříku, zapiš do deníku, že jsi vyčerpal: lokální knihovnu, rejstříky,
jiné stejnojmenné obce, jiná vyznání (evangelíci, církev československá, civilní matriky od 1919), sňatek rodičů,
doklady u rodiny, matriční úřad. U negativního výsledku vždy zapiš spolehlivost čtení (s dokladem / orientačně).

## Slepá ulice
Když dvě kola po sobě nic nepřinesou, nepouštěj další podobné hledání, ale:
1. `python -I -X utf8 tools/fronta.py` – kdo má nejlevnější další krok (`pracovni/fronta.md`),
2. `tools/kmotri.py` – síť kmotrů a svědků (kmotr často ukáže rodinu matky),
3. zdroje jiné než matriky (`reference/souvislosti.md`: mlýny, pozemkové knihy, katastry, sčítání, noviny),
4. kontrola, že žádný předek nevisí odpojený: `[k for k in P if k>1 and k//2 not in P]` musí vrátit jen osoby,
   které odpojené být mají.
Větve, které uživatel označí za uzavřené, nehledej bez nové stopy od rodiny.

## Před „nenalezeno“ u předků před 1800
Projdi `reference/souvislosti.md` oddíl E a F: (a) **vrchnost** – panství obce a jeho knihy (pozemkové knihy, urbáře,
svatební smlouvy, dědická řízení, kontrakty – jedna smlouva vypíše sourozence s podíly); (b) **soupisy poddaných**
(1651, berní rula 1654, tereziánský a josefský katastr, svobodnické knihy, vodní mlýny pro mlynáře); (c) **vojenské
prameny** (poznámky „miles/voják“, Grundbuchsblätter, VÚA); (d) síť kmotrů. Každý z nich je jen vodítko – osoba se
zapisuje až z matriky nebo vrchnostenské knihy přečtené na snímku. Do deníku zapiš, které zdroje jsi zkusil.

## Poučení z praxe
- **20. století:** u lidí narozených po 1900 je nejrychlejší sňatek rodičů a poznámky na okrajích křtů (sňatek,
  biřmování, vystoupení z církve). Okrajové poznámky čti v plném rozlišení; název obce se v náhledu snadno přečte špatně.
- **Kniha řazená po obcích:** číslo strany v rejstříku platí uvnitř oddílu obce; posun „snímek ≈ folio + N“ ověř na dvou snímcích.
- **Neúspěch v jedné faře velkoměsta neznamená nic** – zjisti přesné místo z dokladů nebo od rodiny.
- **Doklady, které rodina má doma** (rodný list syna, úmrtní list, vojenská knížka) jsou rychlejší než den listování.
- **Čísla osob jsou Kekulé** (otec 2n, matka 2n+1). Nového předka nikdy nečísluj „na další volné číslo“; čísla vedlejších
  osob mimo přímou linii vol tak, aby `k//2` existovalo, nebo je dej do `SIDE`.
- **Zápis z knihy → osoby hned.** Jmenuje-li zápis rodiče (otec ženicha, otec nevěsty), zapiš je jako osoby s číslem
  podle Kekulé a odkazem na zápis, ne jen do poznámky.
- **Při hlášení vždy řekni nejstarší dochovaný zápis** (nejmenší rok v `zaznamy.json` → `datum`); zmínky bez zápisu zvlášť.
- **Rejstřík bývá jen vodítko** – může uvádět jiný rok nebo osobu než skutečný zápis; vždy čti knihu.
- **FamilySearch:** index „Česká republika, Církevní knihy“ nemá obec, fulltext tam české knihy nemá – jen nápověda.
- **Zajímavosti** v `data/zajimavosti.md` řaď podle roku děje, nejnovější nahoře.

## Kontrola faktů (slepé druhé čtení) a stránka rozhodnutí
Po velkém kole nebo před zveřejněním se vyplatí **slepé kontrolní čtení**: pomocník čte každý výřez `zdroje/<klíč>.jpg`
bez dosavadního přepisu, výsledek se porovná s `prepisy.json`, `zaznamy.json` a `osoby.py`; kde se čtení rozcházejí
v datu, domě, jménu nebo příbuzenství, přečti snímek sám (třetí čtení). Nálezy dej do zprávy po osobách (`osoba.pořadí`,
závažnost A/B/C) a z ní jednu **stránku rozhodnutí** (výřez + současná data + kontrolní čtení + volba opravit / ponechat /
dohledat / jinak, s odkazem na lokální stránku knihy). Data se mění až podle uložených rozhodnutí uživatele.
