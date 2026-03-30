#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═════════════════════════════════════════════════════╗
║   KINETIC-IT · Puzzle Kleinanzeigen Generator v3    ║
║           github.com · bausteine.json               ║
╚═════════════════════════════════════════════════════╝

Dateien:
  puzzle_generator.py  — dieses Script (nicht anfassen)
  bausteine.json       — dynamische Texte (anpassen)
  statisch.json        — feste Texte: Tierhaushalt + Rechtsparagraph
  inserate/            — exportierte .txt Dateien (automatisch)
  verlauf.csv          — Verlauf aller Inserate (automatisch)
"""

import random, re, os, csv, json, subprocess, sys
from datetime import datetime

try:
    import readline
except ImportError:
    pass

# ─────────────────────────────────────────────────────────────
# PFADE
# ─────────────────────────────────────────────────────────────

BASIS          = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
INSERATE_DIR   = os.path.join(BASIS, "inserate")
VERLAUF_CSV    = os.path.join(BASIS, "verlauf.csv")
BAUSTEINE_JSON = os.path.join(BASIS, "bausteine.json")
STATISCH_JSON  = os.path.join(BASIS, "statisch.json")

# ─────────────────────────────────────────────────────────────
# DATEIEN LADEN
# ─────────────────────────────────────────────────────────────

def lade_bausteine():
    if os.path.exists(BAUSTEINE_JSON):
        with open(BAUSTEINE_JSON, encoding="utf-8") as f:
            return json.load(f)
    return {}

def lade_statisch():
    if os.path.exists(STATISCH_JSON):
        with open(STATISCH_JSON, encoding="utf-8") as f:
            return json.load(f)
    # Fallback
    return {
        "tierhaushalt": "Wir leben in einem Tierhaushalt – vollständige Tierhaarfreiheit können wir daher nicht garantieren.",
        "rechtsparagraph": "------------------------\nPrivatverkauf von privat – unter Ausschluss jeglicher Gewährleistung (§ 437 BGB).\nKeine Rücknahme, kein Umtausch.\nArtikel wird wie beschrieben verkauft, Irrtümer und Zwischenverkauf vorbehalten.\nVersandrisiko bei unversichertem Versand trägt der Käufer."
    }

B = lade_bausteine()
S = lade_statisch()

# ─────────────────────────────────────────────────────────────
# CLIPBOARD
# ─────────────────────────────────────────────────────────────

def in_clipboard(text):
    if sys.platform == "darwin":
        try:
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
            return True
        except Exception:
            pass
    if sys.platform == "win32":
        try:
            subprocess.run(["clip"], input=text.encode("utf-16"), check=True)
            return True
        except Exception:
            pass
    for cmd in [["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]]:
        try:
            subprocess.run(cmd, input=text.encode("utf-8"), check=True, stderr=subprocess.DEVNULL)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    return False

# ─────────────────────────────────────────────────────────────
# VERLAUF
# ─────────────────────────────────────────────────────────────

def verlauf_laden():
    if not os.path.exists(VERLAUF_CSV):
        return []
    with open(VERLAUF_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def verlauf_speichern(daten, dateiname):
    felder = ["datum", "hersteller", "motiv", "teile", "zustand", "datei"]
    neu = not os.path.exists(VERLAUF_CSV)
    with open(VERLAUF_CSV, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=felder)
        if neu:
            w.writeheader()
        w.writerow({
            "datum": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "hersteller": daten["hersteller"],
            "motiv": daten["motiv"],
            "teile": daten["teile"],
            "zustand": daten["zustand"],
            "datei": os.path.basename(dateiname),
        })

def duplikat_check(motiv):
    return [e for e in verlauf_laden() if e["motiv"].lower().strip() == motiv.lower().strip()]

# ─────────────────────────────────────────────────────────────
# TEXTGENERATOR
# ─────────────────────────────────────────────────────────────

def r(key, fallback=""):
    """Zufälligen Eintrag aus bausteine.json holen."""
    pool = B.get(key, [])
    return random.choice(pool) if pool else fallback

def generiere_text(daten):
    hersteller    = daten["hersteller"]
    motiv         = daten["motiv"]
    teile         = daten["teile"]
    beschreibung  = daten.get("beschreibung", "")
    schwierigkeit = daten.get("schwierigkeit", "mittel")
    zustand       = daten.get("zustand", "gut")
    besonderheit  = daten.get("besonderheit", "")

    # Teile-Kategorie
    try:
        t = int(teile)
        tk = "klein" if t <= 300 else "mittel" if t <= 1000 else "gross" if t <= 2000 else "riesig"
    except ValueError:
        tk = "mittel"

    # ── Zeile 1: Intro ────────────────────────────────────────
    intro = r("intro", f"Wir bieten ein {hersteller} Puzzle mit {teile} Teilen, Motiv \"{motiv}\".").format(
        hersteller=hersteller, teile=teile, motiv=motiv
    )

    # ── Zeile 2: Motivbeschreibung (optional) ────────────────
    motiv_zeile = ""
    if beschreibung:
        motiv_zeile = r("motiv_beschreibung", beschreibung).format(beschreibung=beschreibung)

    # ── Zeile 3: Schwierigkeit ───────────────────────────────
    schwier_pool = B.get("schwierigkeit", {}).get(schwierigkeit, [])
    schwier_text = random.choice(schwier_pool) if schwier_pool else ""

    # ── Zeile 4: Zustand ─────────────────────────────────────
    zustand_pool = B.get("zustand", {}).get(zustand.lower(), [])
    zustand_text = random.choice(zustand_pool) if zustand_pool else zustand

    # ── Zeile 5: Teile-Kommentar ─────────────────────────────
    teile_pool = B.get("teile_kommentar", {}).get(tk, [])
    teile_text = random.choice(teile_pool) if teile_pool else ""

    # ── Besonderheit ─────────────────────────────────────────
    besonder_zeile = f"\n⚠️  Hinweis: {besonderheit}" if besonderheit else ""

    # ── Verpackung + Abschluss ───────────────────────────────
    verpackung = r("verpackung", "Wird sicher verpackt versendet.")
    abschluss  = r("abschluss", "Bei Fragen einfach melden!")

    # ── Dynamischer Vertrauensblock (zufällig gemischt) ──────
    vertrauen = [
        r("vollstaendigkeit"),
        r("verbundene_teile"),
        r("sorgfalt"),
        r("herkunft"),
    ]
    random.shuffle(vertrauen)

    # ── STATISCHE Blöcke ─────────────────────────────────────
    tierhaushalt   = S.get("tierhaushalt", "")
    rechtsparagraph = S.get("rechtsparagraph", "")

    # ── Zusammensetzen ───────────────────────────────────────
    hauptblock = intro
    if motiv_zeile:
        hauptblock += f"\n{motiv_zeile}"
    if schwier_text:
        hauptblock += f"\n{schwier_text}"
    hauptblock += f"\n{zustand_text}"
    if teile_text:
        hauptblock += f"\n{teile_text}"
    if besonder_zeile:
        hauptblock += besonder_zeile

    vertrauens_block = "\n\n".join(vertrauen)

    return (
        f"{hauptblock}\n\n"
        f"{verpackung}\n"
        f"{abschluss}\n\n"
        f"---\n\n"
        f"{vertrauens_block}\n\n"
        f"{tierhaushalt}\n\n"
        f"{rechtsparagraph}\n"
    )

# ─────────────────────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────────────────────

def frage(text, pflicht=True, standard=None):
    hinweis = f" [{standard}]" if standard else " [leer = überspringen]" if not pflicht else ""
    while True:
        antwort = input(f"  {text}{hinweis}: ").strip()
        if antwort:
            return antwort
        if not pflicht:
            return standard or ""
        print("  ⚠  Pflichtfeld.")

def auswahl(text, optionen):
    print(f"\n  {text}")
    for i, o in enumerate(optionen, 1):
        print(f"    {i}) {o}")
    while True:
        raw = input("  Auswahl: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(optionen):
            return optionen[int(raw) - 1]
        print("  ⚠  Ungültige Eingabe.")

def sanitize(name):
    name = name.lower().replace(" ", "_")
    return re.sub(r"[^a-z0-9_]", "", name)[:40]

def trennlinie(z="─", b=54):
    print(z * b)

def clear():
    pass

def vorschau_anzeigen(text, nummer):
    trennlinie("─")
    print(f"  VORSCHAU — Variante {nummer}")
    trennlinie("─")
    print()
    print(text)
    trennlinie("─")

def verlauf_anzeigen():
    eintraege = verlauf_laden()
    if not eintraege:
        print("  Noch keine Einträge im Verlauf.")
        return
    trennlinie()
    print(f"  {'DATUM':<17} {'HERSTELLER':<15} {'MOTIV':<25} {'TEILE':<6} {'ZUSTAND'}")
    trennlinie("·")
    for e in eintraege[-20:]:
        print(f"  {e['datum']:<17} {e['hersteller']:<15} {e['motiv'][:24]:<25} {e['teile']:<6} {e['zustand']}")
    trennlinie()
    print(f"  Gesamt: {len(eintraege)} Inserate")
    print()

# ─────────────────────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────────────────────

def exportiere(text, daten):
    os.makedirs(INSERATE_DIR, exist_ok=True)
    datum = datetime.now().strftime("%Y%m%d_%H%M%S")
    pfad  = os.path.join(INSERATE_DIR, f"puzzle_{sanitize(daten['motiv'])}_{datum}.txt")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(text)
    return pfad

def exportiere_und_clipboard(text, daten, mit_clipboard):
    pfad = exportiere(text, daten)
    verlauf_speichern(daten, pfad)
    print(f"\n  ✅ Gespeichert: {pfad}")
    if mit_clipboard:
        if in_clipboard(text):
            print("  📋 In Zwischenablage kopiert!")
        else:
            print("  ⚠  Clipboard nicht verfügbar.")
            print("     Linux: sudo apt install xclip")
            print("     Mac:   pbcopy ist bereits dabei")
            print("     Alternativ: Datei direkt öffnen aus /inserate/")
    print()

# ─────────────────────────────────────────────────────────────
# HERSTELLER & TEILE AUSWAHL
# ─────────────────────────────────────────────────────────────

HERSTELLER_LISTE = [
    "Ravensburger", "Schmidt Spiele", "Clementoni", "Educa",
    "Jumbo", "Heye", "Castorland", "Bluebird Puzzle",
    "Trefl", "Eurographics", "No-Name", "Eigene Eingabe",
]

TEILE_LISTE = ["100", "200", "300", "500", "750", "1000", "1500", "2000", "3000", "5000", "Eigene Eingabe"]

def block_auswahl(titel, liste):
    print(f"\n  {titel}:")
    mitte = (len(liste) + 1) // 2
    for i in range(mitte):
        l_nr, l_txt = i + 1, liste[i]
        r_nr = i + 1 + mitte
        if r_nr <= len(liste):
            print(f"    {l_nr:>2}) {l_txt:<22}  {r_nr:>2}) {liste[r_nr - 1]}")
        else:
            print(f"    {l_nr:>2}) {l_txt}")
    print()
    while True:
        raw = input("  Auswahl (Nummer oder direkt eingeben): ").strip()
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(liste):
                gewählt = liste[idx - 1]
                if gewählt == "Eigene Eingabe":
                    return frage(f"{titel} eingeben")
                return gewählt
        elif raw:
            return raw
        print("  ⚠  Ungültige Eingabe.")

# ─────────────────────────────────────────────────────────────
# DUPLIKAT CHECK
# ─────────────────────────────────────────────────────────────

def duplikat_warnung(motiv):
    treffer = duplikat_check(motiv)
    if treffer:
        print()
        print(f"  ⚠  DUPLIKAT: '{motiv}' wurde bereits {len(treffer)}× exportiert:")
        for t in treffer:
            print(f"     → {t['datum']}  |  {t['zustand']}  |  {t['datei']}")
        print()
        return input("  Trotzdem fortfahren? [j/n]: ").strip().lower() == "j"
    return True

# ─────────────────────────────────────────────────────────────
# EINGABE — SCHNELL & MANUELL
# ─────────────────────────────────────────────────────────────

def eingabe_schnell():
    trennlinie()
    print("  ⚡ SCHNELLMODUS — 4 Eingaben, fertig")
    trennlinie()

    hersteller = block_auswahl("Hersteller", HERSTELLER_LISTE)
    motiv      = frage("Motiv / Titel")

    if not duplikat_warnung(motiv):
        return None

    teile   = block_auswahl("Teileanzahl", TEILE_LISTE)
    zustand = auswahl("Zustand?", ["neu", "wie neu", "gut", "gebraucht"])

    try:
        t = int(teile)
        schwierigkeit = "niedrig" if t <= 500 else "mittel" if t <= 1500 else "hoch"
    except ValueError:
        schwierigkeit = "mittel"

    return {"hersteller": hersteller, "motiv": motiv, "teile": teile,
            "beschreibung": "", "schwierigkeit": schwierigkeit,
            "zustand": zustand, "besonderheit": "", "_schnell": True}

def eingabe_manuell():
    trennlinie()
    print("  ✏️  MANUELL-MODUS — volle Kontrolle")
    trennlinie()

    hersteller   = block_auswahl("Hersteller", HERSTELLER_LISTE)
    motiv        = frage("Motiv / Titel")

    if not duplikat_warnung(motiv):
        return None

    teile        = block_auswahl("Teileanzahl", TEILE_LISTE)
    beschreibung = frage("Kurze Motivbeschreibung", pflicht=False)
    schwierigkeit = auswahl("Schwierigkeitsgrad?", ["niedrig", "mittel", "hoch"])
    zustand      = auswahl("Zustand?", ["neu", "wie neu", "gut", "gebraucht"])
    besonderheit = frage("Besonderheit? (z.B. 'fehlt 1 Teil', 'Holzpuzzle')", pflicht=False)

    return {"hersteller": hersteller, "motiv": motiv, "teile": teile,
            "beschreibung": beschreibung, "schwierigkeit": schwierigkeit,
            "zustand": zustand, "besonderheit": besonderheit, "_schnell": False}

def eingabe():
    modus = auswahl("Modus?", ["⚡ Schnell", "✏️  Manuell"])
    print()
    return eingabe_schnell() if "Schnell" in modus else eingabe_manuell()

# ─────────────────────────────────────────────────────────────
# EXPORT FLOW
# ─────────────────────────────────────────────────────────────

def export_flow(gewählt, daten):
    """Vorschau → Export → Clipboard."""
    print()
    vorschau_anzeigen(gewählt, "✓")
    aktion = auswahl("Alles gut?", [
        "Exportieren & in Clipboard kopieren",
        "Nur exportieren",
        "Neu generieren",
        "Neue Daten eingeben",
    ])
    if aktion == "Neue Daten eingeben":
        return "neu"
    if aktion == "Neu generieren":
        return "nochmal"
    exportiere_und_clipboard(gewählt, daten, "Clipboard" in aktion)
    return "fertig"

# ─────────────────────────────────────────────────────────────
# HAUPTSCHLEIFE
# ─────────────────────────────────────────────────────────────

def main():
    clear()

    s_status = "✅" if os.path.exists(STATISCH_JSON)  else "⚠  fehlt"
    b_status = "✅" if os.path.exists(BAUSTEINE_JSON) else "⚠  fehlt"

    print(f"""
╔═════════════════════════════════════════════════════╗
║   KINETIC-IT · Puzzle Kleinanzeigen Generator v3    ║
║           github.com · bausteine.json               ║
╚═════════════════════════════════════════════════════╝
  Ausgabe:     {INSERATE_DIR}
  bausteine:   {b_status}
  statisch:    {s_status}
""")

    while True:
        trennlinie("═")
        aktion = auswahl("Was möchtest du tun?", [
            "Neues Inserat erstellen",
            "Verlauf anzeigen",
            "Beenden",
        ])

        if aktion == "Beenden":
            print("\n  Tschüss! 👋\n")
            break

        if aktion == "Verlauf anzeigen":
            print()
            verlauf_anzeigen()
            continue

        print()
        daten = eingabe()
        if daten is None:
            continue

        # ── Schnellmodus: direkt ein Text ─────────────────────
        if daten.get("_schnell"):
            while True:
                gewählt = generiere_text(daten)
                result  = export_flow(gewählt, daten)
                if result == "fertig":
                    break
                if result == "neu":
                    daten = eingabe()
                    if daten is None:
                        break
                # "nochmal" → neue Variante generieren

        # ── Manuell: 3 Varianten zur Auswahl ─────────────────
        else:
            while True:
                print()
                trennlinie("═")
                print("  3 VARIANTEN — bitte wählen")
                trennlinie("═")

                varianten = [generiere_text(daten) for _ in range(3)]

                for i, v in enumerate(varianten, 1):
                    print(f"\n── Variante {i} " + "─" * 38)
                    zeilen = v.strip().split("\n")
                    for z in zeilen[:5]:
                        print(f"   {z}")
                    if len(zeilen) > 5:
                        print(f"   … ({len(zeilen)-5} weitere Zeilen)")

                print()
                wahl = auswahl("Auswahl:", [
                    "Variante 1",
                    "Variante 2",
                    "Variante 3",
                    "Alle neu generieren",
                    "🎲 Zufall entscheiden",
                ])

                if wahl == "Alle neu generieren":
                    continue

                idx = random.randint(0, 2) if "Zufall" in wahl else int(wahl.split()[1]) - 1
                result = export_flow(varianten[idx], daten)

                if result == "fertig":
                    break
                if result == "neu":
                    daten = eingabe()
                    if daten is None:
                        break

if __name__ == "__main__":
    main()
