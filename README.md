# 🧩 Puzzle Kleinanzeigen Generator
**von KINETIC-IT**

Ein interaktives Python-Script das automatisch professionelle Verkaufstexte für Puzzle-Inserate generiert. Jedes Inserat klingt anders — Zufallsgenerator aus Textbausteinen.

---

## ✨ Features
- ⚡ **Schnellmodus** — 4 Eingaben, sofort fertig
- ✏️ **Manuell-Modus** — volle Kontrolle, 3 Varianten zur Auswahl
- 🎲 **Zufallsgenerator** — jedes Inserat klingt anders
- 👁️ **Vorschau** — Text ansehen vor dem Export
- 📋 **Clipboard** — Text direkt kopieren (siehe unten)
- ⚠️ **Duplikat-Warnung** — erkennt bereits inserierte Motive
- 📊 **Verlauf** — alle Inserate in `verlauf.csv`
- 🔧 **Anpassbar** — Texte in `bausteine.json`, kein Python nötig
- 🔒 **Statische Texte** — Tierhaushalt + Rechtsparagraph immer dabei (`statisch.json`)

---

## 📁 Dateien
```
puzzle-generator/
├── puzzle_generator.py   ← Script starten — nicht anfassen
├── bausteine.json        ← dynamische Texte anpassen
├── statisch.json         ← feste Texte (Tierhaushalt, Rechtsparagraph)
├── ANPASSEN.md           ← Anleitung
├── README.md             ← diese Datei
├── inserate/             ← exportierte Texte (automatisch)
└── verlauf.csv           ← Verlauf (automatisch)
```

---

## 🚀 Installation

**Voraussetzung:** Python 3.8+ — [python.org](https://www.python.org/downloads/)

```bash
git clone https://github.com/DEIN-NAME/puzzle-generator.git
cd puzzle-generator
python3 puzzle_generator.py
```

---

## 📋 Clipboard einrichten

| System | Was tun? |
|--------|----------|
| **Linux** | `sudo apt install xclip` |
| **macOS** | Funktioniert automatisch ✅ |
| **Windows** | Funktioniert automatisch ✅ |
| **Kein Clipboard** | Text liegt in `inserate/` als .txt — einfach öffnen |

---

## 🎲 Beispiel-Output

```
Zum Verkauf steht ein Ravensburger Puzzle – 1000 Teile, Motiv "Herbstwald".
Eine angenehme Herausforderung für Gelegenheits-Puzzler.
Wie neu – kaum benutzt.

Wird sicher verpackt versendet. Bei Fragen einfach melden!

---
Alle Teile wurden so gut wie möglich kontrolliert, ohne Garantie.
Wir achten darauf, dass keine Teile zusammenkleben.
Wir sind ordentliche Puzzler – alles sauber gelagert.
Meist einmal selbst gelegt.
Wir leben in einem Tierhaushalt – Tierhaarfreiheit können wir nicht garantieren.

------------------------
Privatverkauf von privat – unter Ausschluss jeglicher Gewährleistung (§ 437 BGB).
Keine Rücknahme, kein Umtausch.
Artikel wird wie beschrieben verkauft, Irrtümer vorbehalten.
Versandrisiko bei unversichertem Versand trägt der Käufer.
```

---

## 🔧 Anpassen
→ **[ANPASSEN.md](ANPASSEN.md)** für die vollständige Anleitung.

Kurzfassung:
- Neue Texte → `bausteine.json`
- Kein Tierhaushalt → `statisch.json` → `"tierhaushalt": ""`
- Hersteller → `puzzle_generator.py` → `HERSTELLER_LISTE`

---

## 📄 Lizenz
MIT — mach damit was du willst. Ein ⭐ freut uns! 😄

**Made with ❤️ by KINETIC-IT**

🤖 Dieses Projekt wurde mit Unterstützung von KI (Claude von Anthropic) entwickelt.
