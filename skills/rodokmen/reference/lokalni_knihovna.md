# Lokální knihovna matrik a pramenů

Někteří uživatelé si stahují **celé svazky** (ARON nabízí u každé knihy i sčítání tlačítko „Stáhnout všechny snímky“ =
jeden ZIP). Desítky GB snímků na disku jsou nejrychlejší a nejšetrnější zdroj: snímek je hned, archiv nedostane žádný
dotaz, pomocníci si nepřekážejí a výpadek archivu (noc, údržba, prošlý certifikát) práci nezastaví. Platí proto:

## Pravidlo: nejdřív disk, pak archiv
1. Než stáhneš jakýkoli snímek nebo otevřeš knihu v prohlížeči, podívej se do knihovny:
   `python -I -X utf8 tools/knihovna.py najdi <signatura> [<snímek>]` (nebo část názvu složky, např. `inv231`),
   případně do soupisu `dokumenty/Matriky/SOUPIS.md` a `dokumenty/Prameny/SOUPIS.md`.
2. Je-li svazek na disku, **čti z disku** (snímky prohlížej nástrojem Read, výřezy `vyrez.py` přímo ze souboru knihovny –
   nekopíruj celé stránky do `pracovni/`).
3. Do zápisu dej odkaz na archiv jako vždy (trvalý odkaz na knihu / snímek) **a** cestu ke stránce na disku: pole
   `lokalne` (`knihovna.py zaznam <klíč> --uloz`), v poznámce název souboru a číslo snímku.
   Číslo snímku na disku = poslední skupina číslic v názvu souboru; u ARONu bývá shodné s číslem snímku v prohlížeči
   archivu, ale ověř si to (`aron_img.py <apu> link <n>`) – u některých svazků je posun.
4. Pomocníkům dávej do zadání cestu ke složce svazku (šablona A v `reference/pomocnici.md`).
5. Chybí-li svazek, který budeš listovat víc než pár snímků, je levnější ho stáhnout celý (jeden ZIP = jeden dotaz)
   než stahovat snímek po snímku. Navrhni to uživateli – stahování desítek až stovek MB nech na něm (prohlížečem),
   nebo jeden dotaz přes brzdu (`tools/slusne.py curl … -o dokumenty/Matriky/new/<soubor>.zip`).

## Jak najít ZIP celé jednotky v ARONu
`GET https://aron.vychodoceskearchivy.cz/api/aron/apu/<id>` (přes brzdu) → `parts[].items[]` s `type == "URL"`
(„Stáhnout všechny snímky“), `href` vede na `storage.vychodoceskearchivy.cz/ds/…zip` (knihy) nebo `…/scitani/…zip`
(sčítání). Nematriční digitalizáty (městské knihy, katastry, sčítání) najdeš hledáním bez filtru „Sbírka matrik“
a s filtrem „pouze s digitalizáty“ (`reference/souvislosti.md` → D).

## Pořádek v knihovně
```
dokumenty/Matriky/
  SOUPIS.md                         signatura | druh | roky | obce | snímků | v datech | odkaz do archivu
  new/                              schránka: sem uživatel ukládá stažené ZIPy (a rozpracované *.crdownload)
  zip/                              původní ZIPy po rozbalení (uživatel si je může odnést mimo projekt)
  <farnost>/<signatura> <druh> <roky>/   snímky přímo uvnitř (bez dvojitého vnoření)
dokumenty/Prameny/
  SOUPIS.md
  <obec>/<název, např. „inv231 drzitele usedlosti do 1828“, „scitani 1921“>/
```
- Nový ZIP: `python -I -X utf8 tools/knihovna.py rozbal dokumenty/Matriky/new/<soubor>.zip "dokumenty/Matriky/<farnost>/<signatura> <druh> <roky>"`
  – rozbalí, ověří počet snímků a ZIP přesune do `zip/`. Pak doplň řádek do `SOUPIS.md` (druh, roky a obce z popisu
  svazku v archivu). `knihovna.py soupis` ukáže složky, které v soupisu chybí.
- **Rozpracované stahování (`*.crdownload`, `*.part`) nikdy nemaž** – uživatel by ho stahoval znovu.
- Knihovna patří do `.gitignore` (velikost); zálohu ZIPů si drží uživatel.
- Snímky z knihovny jsou pracovní kopie – na web jdou jen výřezy (`vyrezy/`, `zdroje/`) jako u snímků ze sítě.
