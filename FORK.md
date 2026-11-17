# Fork jandadik/rodokmen-skill

Základ je [sarsonj/rodokmen-skill](https://github.com/sarsonj/rodokmen-skill) (větev `main` = jeho vydání), naše úpravy
jsou ve větvi **`jan`** jako samostatné commity nad ním. Verze forku: `<verze sarsonje>+jan.<N>` (soubor `skills/rodokmen/VERZE`).

## Co je navíc
- **Pravidla uživatele** (pracuj sám, vytěžení všeho od uživatele, slepá ulice, prameny mimo matriky, pomocníci souběžně)
  – převzato z [micl79/rodokmen-skill](https://github.com/micl79/rodokmen-skill), upraveno na brzdu `slusne.py`.
  Blok na začátku `SKILL.md`, podrobnosti `reference/rozsireni.md`, `reference/pomocnici.md`, `reference/souvislosti.md`.
- **Lokální knihovna svazků** – celé svazky stažené z archivu na disku: `tools/knihovna.py`, `reference/lokalni_knihovna.md`,
  pole `lokalne` u zápisu.
- Nástroje `fronta.py`, `kmotri.py`, `oprav_odkazy.py` (z micl79).
- Web: stránka **Celý strom** (z micl79), **více příběhů** (`web.json → dalsi_pribehy`) s rozcestníkem `/pribehy/`,
  **portrét** osoby (`dokumenty.json → portret`), úvodní box se seznamem příběhů a fotkou.
- `verze.py` a `novy_projekt.py` rozumí verzi `x.y.z+jan.N`; u forku v gitu radí rebase.

## Instalace (Windows)
Klon do `D:\ClaudeCowork\Skills\rodokmen-skill`, větev `jan`; Claude Code ho čte přes odkaz (junction)
`%USERPROFILE%\.claude\skills\rodokmen2` → `…\rodokmen-skill\skills\rodokmen`.

## Aktualizace ze sarsonje
```
git fetch upstream
git checkout jan
git rebase upstream/main          # střety vyřešit, úpravy forku zachovat
# VERZE: <nová verze>+jan.1, testy: tests/aktualizace, tests/verze, tests/kontrola, ukázkový projekt + npm run build
git push --force-with-lease origin jan
```
Pak v projektu `python -I -X utf8 <skill>/tools/novy_projekt.py <projekt>` (data zůstanou, úpravy webu se sloučí),
`cd web && npm install && npm run data && npm run build`.
