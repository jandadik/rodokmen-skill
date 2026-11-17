#!/usr/bin/env python3
"""Lokální knihovna matrik a pramenů – celé svazky stažené z archivu (ZIP z ARONu) na disku projektu.

Svazky leží v `dokumenty/Matriky/<farnost>/<signatura> <druh> <roky>/` a prameny mimo matriky (sčítání, městské
a vrchnostenské knihy) v `dokumenty/Prameny/<obec>/<název>/`; snímky přímo ve složce. Snímek z disku archiv nezatěžuje
a je hned – proto se před každým stažením nejdřív hledá tady. Nástroj nic nestahuje a nikam nepřistupuje po síti.

Použití (z kořene projektu, Windows `python -I -X utf8`, jinde `python3 -I`):
  knihovna.py najdi <signatura|text> [<snímek>]   složky svazku (podle signatury nebo části názvu) a soubor snímku
  knihovna.py zaznam <klíč> [--uloz]              lokální stránka k zápisu z data/zaznamy.json (z poznámky „soubor …“,
                                                  signatury svazku a čísla snímku); --uloz zapíše pole `lokalne`
  knihovna.py zaznamy [--uloz]                    totéž pro všechny zápisy; vypíše, co se nenašlo
  knihovna.py soupis                              svazky na disku s počtem snímků; upozorní na složky chybějící v SOUPIS.md
  knihovna.py rozbal <zip> <cílová složka>        rozbalí ZIP svazku (bez dvojitého vnoření), ověří počet snímků a ZIP
                                                  přesune do dokumenty/Matriky/zip/ (rozpracované *.crdownload nikdy nemaže)
Číslo snímku = poslední skupina 4–5 číslic oddělená podtržítkem v názvu souboru (…_00072.jpg, …_00027_sign-25-3959.JPG).
"""
import json, os, re, shutil, subprocess, sys, tempfile, unicodedata, zipfile
from pathlib import Path

ROOT = Path.cwd()
KORENY = [ROOT / "dokumenty" / "Matriky", ROOT / "dokumenty" / "Prameny"]
VYNECH = {"zip", "new"}
IMG = re.compile(r"\.(jpe?g|png|tiff?)$", re.I)


def fold(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def cislo(nazev):
    g = re.findall(r"_(\d{4,5})(?=[_.])", nazev)
    if g:
        return int(g[-1])
    m = re.search(r"(\d+)\D*$", Path(nazev).stem)
    return int(m.group(1)) if m else None


_INDEX = None


def index():
    """[(relativní cesta s /, název)] všech snímků v knihovně."""
    global _INDEX
    if _INDEX is None:
        _INDEX = []
        for koren in KORENY:
            if not koren.is_dir():
                continue
            for dp, dn, fn in os.walk(koren):
                dn[:] = [d for d in dn if d not in VYNECH]
                for f in fn:
                    if IMG.search(f):
                        _INDEX.append((os.path.relpath(os.path.join(dp, f), ROOT).replace("\\", "/"), f))
        _INDEX.sort()
    return _INDEX


def slozky():
    d = {}
    for r, _ in index():
        d.setdefault(r.rsplit("/", 1)[0], []).append(r)
    return d


def slozky_svazku(sign):
    """Složky, jejichž název začíná signaturou (`4371 O 1862-1880`), jinak obsahují text."""
    S = slozky()
    p = [s for s in S if re.match(rf"{re.escape(sign)}(\s|$)", s.rsplit("/", 1)[1])]
    return p or [s for s in S if fold(sign) in fold(s.rsplit("/", 1)[1])]


def snimek(slozka, n):
    for r in slozky().get(slozka, []):
        if cislo(r.rsplit("/", 1)[1]) == int(n):
            return r
    return None


def najdi_zaznam(z, svazek):
    """(cesta ke stránce | None, složka | None, jak se našlo)."""
    pozn = z.get("pozn", "") or ""
    if z.get("lokalne") and (ROOT / z["lokalne"]).exists():
        return z["lokalne"], z["lokalne"].rsplit("/", 1)[0], "pole lokalne"
    sv = (svazek or {}).get("svazek", "")
    m = re.search(r"sign\.?:?\s*([\w-]+)", sv)
    sign = m.group(1) if m else None
    # 1) název souboru v poznámce („soubor …_00072.jpg“, „P1080623“)
    hints = re.findall(r"(?:soubor[y]?|fotografi\w*)\s*\(?\s*([…\.]*[\w\-\.]+\.(?:jpe?g|png))", pozn, re.I)
    hints += re.findall(r"\b(P\d{7})\b", pozn)
    roots = [ROOT / "dokumenty"]
    vse = None
    for h in hints:
        h = h.lstrip("….").lower()
        kand = [r for r, b in index() if b.lower() == h or b.lower().endswith(h)]
        if not kand and re.fullmatch(r"p\d{7}", h):
            if vse is None:  # rodinné fotky z archivu mohou být mimo knihovnu
                vse = [(os.path.relpath(os.path.join(dp, f), ROOT).replace("\\", "/"), f)
                       for rt in roots for dp, _, fn in os.walk(rt) for f in fn if IMG.search(f)]
            kand = [r for r, b in vse if b.lower().startswith(h + ".")]
        if sign:
            kand = [r for r in kand if sign in r] or kand
        if kand:
            return kand[0], kand[0].rsplit("/", 1)[0], "soubor z poznámky"
    # 2) složka podle signatury, u pramenů podle inv. č. / kartonu / roku sčítání
    folder = None
    if sign:
        f = [s for s in slozky_svazku(sign) if re.match(rf"{re.escape(sign)}\s", s.rsplit("/", 1)[1])]
        folder = f[0] if f else None
    if not folder:
        S = slozky()
        m_inv = re.search(r"inv\. ?č\. ?(\d+)", sv)
        m_kar = re.search(r"kart\. ?(\d+)", sv)
        m_sc = re.search(r"Sčítání lidu (\d{4}).*?:\s*(.+)$", sv)
        for d in S:
            jm = d.rsplit("/", 1)[1]
            prvni = S[d][0].rsplit("/", 1)[1]
            if m_inv and re.match(rf"inv{m_inv.group(1)}\b", jm):
                folder = d; break
            if m_kar and f"kar{m_kar.group(1)}-" in prvni:
                folder = d; break
            if m_sc and not m_kar and jm.startswith(f"scitani {m_sc.group(1)}"):
                if any(fold(w) in fold(d) for w in re.findall(r"\w{4,}", m_sc.group(2))):
                    folder = d; break
    if folder and z.get("snimek"):
        r = snimek(folder, z["snimek"])
        if r:
            return r, folder, "číslo snímku"
    return None, folder, "jen složka svazku" if folder else "nenalezeno"


def nacti():
    zaz = json.loads((ROOT / "data/zaznamy.json").read_text(encoding="utf-8-sig"))
    sv = json.loads((ROOT / "data/svazky.json").read_text(encoding="utf-8-sig"))
    return {z["klic"]: z for z in zaz}, sv


def uloz(klic, cesta):
    tmp = Path(tempfile.mkdtemp()) / "lokalne.json"
    tmp.write_text(json.dumps({"lokalne": cesta}, ensure_ascii=False), encoding="utf-8")
    nastroj = Path(__file__).with_name("zapis.py")
    subprocess.run([sys.executable, "-I", "-X", "utf8", str(nastroj), "zaznamy", klic, str(tmp), "--sloucit"], check=True)


def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return 0
    cmd = a[0]
    if cmd == "najdi" and len(a) >= 2:
        f = slozky_svazku(a[1])
        if not f:
            print("V lokální knihovně není:", a[1]); return 1
        for s in f:
            print(f"{s}  ({len(slozky()[s])} snímků)")
            if len(a) > 2:
                print("  snímek:", snimek(s, a[2]) or "není")
        return 0
    if cmd in ("zaznam", "zaznamy"):
        zaz, sv = nacti()
        klice = [a[1]] if cmd == "zaznam" and len(a) > 1 else list(zaz)
        ul = "--uloz" in a
        chybi = 0
        for k in klice:
            if k not in zaz:
                print("Neznámý klíč:", k); return 1
            r, d, jak = najdi_zaznam(zaz[k], sv.get(zaz[k].get("svazek")))
            if cmd == "zaznam" or not r:
                print(f"{k}: {r or d or '—'}  [{jak}]")
            chybi += not r
            if r and ul and zaz[k].get("lokalne") != r:
                uloz(k, r)
        if cmd == "zaznamy":
            print(f"{len(klice) - chybi} z {len(klice)} zápisů má lokální stránku.")
        return 0
    if cmd == "soupis":
        S = slozky()
        soupis = ""
        for koren in KORENY:
            if (koren / "SOUPIS.md").exists():
                soupis += (koren / "SOUPIS.md").read_text(encoding="utf-8")
        for s in sorted(S):
            jm = s.rsplit("/", 1)[1]
            sig = jm.split(" ")[0]
            zn = "" if (sig in soupis or jm in soupis) else "   ← chybí v SOUPIS.md"
            print(f"{len(S[s]):5}  {s}{zn}")
        return 0
    if cmd == "rozbal" and len(a) == 3:
        zp, cil = Path(a[1]), Path(a[2])
        if zp.suffix.lower() != ".zip" or not zp.exists():
            print("Čekám hotový soubor .zip (rozpracovaný .crdownload nech být, až se dostáhne)."); return 1
        cil.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zp) as z:
            jm = [n for n in z.namelist() if IMG.search(n)]
            for n in jm:
                with z.open(n) as src, open(cil / Path(n).name, "wb") as dst:
                    shutil.copyfileobj(src, dst)
        ma = len([f for f in os.listdir(cil) if IMG.search(f)])
        print(f"Rozbaleno {len(jm)} snímků do {cil} (ve složce je {ma}).")
        if ma < len(jm):
            print("POZOR: ve složce je méně snímků než v ZIPu – ZIP nepřesouvám."); return 1
        cz = ROOT / "dokumenty" / "Matriky" / "zip"
        cz.mkdir(parents=True, exist_ok=True)
        shutil.move(str(zp), str(cz / zp.name))
        print(f"ZIP přesunut do {cz.relative_to(ROOT)}. Doplň svazek do SOUPIS.md (signatura, druh, roky, obce, počet, odkaz).")
        return 0
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
