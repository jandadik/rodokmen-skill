# Pomocníci (subagenti) – hotová zadání

Pomocník = další kopie Claude, která souběžně na pozadí hledá v matrikách podle přesného zadání. Výsledky píše jen do
`pracovni/pom_<větev>/vysledky.md`, **nikdy do `data/`**. Hlavní model (ty) každý nález ověří na snímku (aspoň výřez
hlavního řádku) a teprve pak zapíše do dat, na web a do deníku. Obecná pravidla (záporný výsledek jen s dokladem,
ověření `overit.py`, brzda) jsou v `SKILL.md` → Pomocníci; tady jsou zkušenosti a hotová zadání.

## Pravidla (osvědčená v rodinných projektech)
- Spouštěj přes Agent s `model: "sonnet"` a `run_in_background: true`. Pokud je uživatel schválil, neptej se, jen jednou větou řekni, co běží.
- **Souběžně 2–4 pomocníci na různé větve, na jeden archiv nejvýš jeden.** Nejdřív **lokální knihovna** (`reference/lokalni_knihovna.md`) –
  snímky na disku archiv nezatěžují a pomocníci si nepřekážejí. Ze sítě jen nástroje s brzdou (`aron_img.py`, `portafontium.py`).
  **Prohlížeč (MZA, SOA Praha, SOA Třeboň) smí mít v jednu chvíli jen jeden pomocník** a ty ho mezitím nepoužívej.
- Zadání musí být samostatné (pomocník nezná konverzaci): složka projektu, technické pasti, přesná id knih / cesta ke složce
  v lokální knihovně, co je už doloženo (jména, data, domy), úkoly v pořadí od nejdůležitějšího a formát výsledku.
- Chtěj u neúspěchů **rozsah a co na snímcích skutečně bylo** (první a poslední jméno a data z každého snímku) –
  „nenalezeno“ od pomocníka je jen upozornění, ne důkaz.
- Pomocník v malém okně prohlížeče čte hůř – v prohlížeči mu napiš, ať čte malé výřezy.
- Pomocník občas omylem zavolá `… svazek` (zapisuje do data/svazky.json) – v zadání to výslovně zakaž; po návratu zkontroluj `git status data`.
- **Zakaž pomocníkům příkazy na pozadí a čekání (sleep, hromadné stahování).** Jednou se takhle zasekli všichni čtyři najednou
  („Agent stalled: no progress for 600s“) a nic neodevzdali. Ať píšou do vysledky.md průběžně po každém nálezu.
- `aron_img.py` úroveň: **0 = plné rozlišení**, 2 = čtvrtina. Do zadání to napiš správně. ARON bývá hodiny nedostupný – pak větev odlož.
- Na těžký rukopis (18. století, slabé mikrofilmy, kurent) pouštěj pomocníka bez `model: "sonnet"` (silnější model) – sonnet to často vzdá po pár snímcích.
- **Zakaž hromadné zkoušení adres** (procházení stovek čísel knih / id po sobě). Pomocník tak jednou zkusil ~350 id
  na mza.cz a archiv počítač zablokoval. Čísla knih hledej přes seznam knih obce nebo vyhledávání archivu, nejvýš pár dotazů.
- **Model podle jistoty vodítka:** slepé prohledávání = `sonnet`; dobré vodítko bez potvrzení (křest bez sňatku rodičů,
  opakovaný kmotr, rejstřík ukazuje list) = silnější model (`opus` nebo bez `model`). Do zadání napiš přesnou stopu a co už je prohledáno.
- **Webové zdroje ve vestavěném prohlížeči často ukazují ověření robota** (vodnimlyny.cz). Pomocník ho **neobchází**; web čte přes Chrome
  (`mcp__claude-in-chrome__*`, vlastní záložka, po sobě zavřít) nebo ohlásí, že se nedostal dál.
- **Nové typy zadání:** (a) síť kmotrů (ze `tools/kmotri.py` → křty dětí hledané rodiny, kmotr ukáže rodinu matky); (b) mlýny a statky
  (veřejné seznamy majitelů, pozemkové knihy); (c) ověření: „přečti znovu v plném rozlišení a potvrď“ u čtení jiného pomocníka.
- Po návratu: ověř, zapiš (`zapis.py`, `osoby.py`), deník, `kontrola.py`, uložení (commit), obnov web – a hned pusť další kolo.

## Šablona A – lokální knihovna a ARON / Porta fontium (bez prohlížeče)
```
Jsi pomocník při genealogickém výzkumu (soukromý rodokmen). Složka: <kořen projektu>
(Windows: Git Bash, Python VŽDY `python -I -X utf8`, ImageMagick jen `magick`; macOS/Linux `python3 -I`).
Do data/ NIC NEZAPISUJ (ani příkazy `svazek`) – výsledky jen do pracovni/pom_<větev>/ (obrázky + vysledky.md).
NEJDŘÍV DISK: svazek hledej v lokální knihovně `python -I -X utf8 tools/knihovna.py najdi <signatura> [<snímek>]`
(soupis `dokumenty/Matriky/SOUPIS.md`). Snímky na disku čti přímo, nic nestahuj.
SÍŤ JEN PŘES BRZDU (archivy jinak blokují IP): nástroje v tools/ ji mají samy; vlastní skript
`python -I -X utf8 tools/slusne.py pracovni/x.py …`, curl `python -I -X utf8 tools/slusne.py curl …` (jedna adresa).
Hláška „slusne: … je zastavený“ = archiv nás odmítl: ten web NEZKOUŠEJ žádnou cestou, pokračuj jiným úkolem nebo skonči.
ARON: `python -I -X utf8 tools/aron_img.py <apu> <snímek> 0 pracovni/pom_<větev>/x.jpg` (0 = plné rozlišení).
Náhled jen na orientaci (roky); jména čti z plného rozlišení a výřezu `magick in.jpg -crop WxH+X+Y -resize 2000x out.jpg`,
obrázek prohlédni nástrojem Read. Nejdřív rejstříky, pak kniha. Stahuj jen snímky, které čteš.
Doloženo: <osoby, data, čísla domů, rodiče>.
Knihy: <signatura / apu – druh – roky – složka na disku – kde je který rok>.
Úkoly (v pořadí): 1. … 2. … 3. …
Ke každému nálezu do vysledky.md: kniha, snímek, datum, úplný přepis (jména, stavy, domy, rodiče, prarodiče, kmotři/svědci),
„(?)“ u nejistot, souřadnice zápisu (zlomky 0–1). U neúspěchů rozsah a u každého snímku první a poslední jméno a data.
Nic nevymýšlej. Na konci krátké shrnutí.
```

## Šablona B – archiv jen v prohlížeči (MZA, SOA Praha, SOA Třeboň; jen jeden pomocník najednou)
```
Jsi pomocník … (stejný úvod jako A). Do data/ NIC NEZAPISUJ – výsledky jen do pracovni/pom_<větev>/vysledky.md.
Pracuješ v prohlížeči podle `reference/portaly.md` (oddíl archivu): tempo aspoň 5 s mezi stránkami, při listování 10 s,
žádné souběžné dotazy ani smyčky přes celé svazky. Při 403/429/503 nebo bílém snímku hned skonči a zapiš
`python -I -X utf8 tools/slusne.py zastav <web> "HTTP … v prohlížeči"`.
Snímek, který čteš, ulož do mezipaměti (`tools/cache.py uloz …`, postup v portaly.md) – podruhé se už neotvírá.
Doloženo: … Knihy: … Úkoly: … (formát výsledku jako v šabloně A)
```

## Co se osvědčilo zadávat
- Hledání rodičů u osoby narozené po ~1925: sňatek rodičů v místě a letech kolem narození (katolické, evangelické, civilní).
- Starší generace: narození (z věku ve sňatku), sňatek rodičů, úmrtí s věkem (uvádí narození a rodiče).
- Sourozenci z rejstříku – rychle dají celou rodinu z jednoho domu.
