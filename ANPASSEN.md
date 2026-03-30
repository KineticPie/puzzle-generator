# Texte anpassen – so geht's

Du musst **nie** das Script anfassen. Alles was du ändern kannst steht in zwei Dateien:

---

## 📄 statisch.json – Texte die IMMER dabei sind

Öffne die Datei mit einem Texteditor (z.B. Notepad).

```json
{
  "tierhaushalt": "Wir leben in einem Tierhaushalt...",
  "rechtsparagraph": "Privatverkauf von privat..."
}
```

**Kein Tier?** Einfach den Text zwischen den Anführungszeichen löschen:
```json
"tierhaushalt": ""
```

**Rechtsparagraph ändern?** Text zwischen den Anführungszeichen ersetzen.  
`\n` bedeutet eine neue Zeile.

---

## 📄 bausteine.json – Zufällige Texte

Hier stehen alle Sätze die der Generator zufällig auswählt.  
Jede Kategorie ist eine Liste von Sätzen in `[ ]`.

**Neuen Satz hinzufügen** – einfach eine neue Zeile rein:
```json
"sorgfalt": [
  "Wir gehen sorgsam mit unseren Puzzles um.",
  "Alles wird sauber gelagert.",
  "→ Hier deinen Satz eintippen"
]
```

**Satz entfernen** – Zeile löschen. Mindestens 1 Satz muss drin bleiben.

**Wichtig:** Nach jedem Satz ein Komma – außer beim letzten vor der `]`.

---

## 🏷️ Hersteller-Liste ändern

In `puzzle_generator.py` ganz oben nach `HERSTELLER_LISTE` suchen:

```python
HERSTELLER_LISTE = [
    "Ravensburger", "Schmidt Spiele", ...
]
```

Namen hinzufügen oder entfernen. `"Eigene Eingabe"` immer am Ende lassen!

---

## ✅ Fehler nach dem Bearbeiten?

JSON-Syntax online prüfen: **https://jsonlint.com**  
Text reinkopieren → auf **Validate** klicken → Fehler werden angezeigt.

Häufigste Fehler:
- Komma nach dem letzten Satz vergessen oder zuviel
- Anführungszeichen `"` vergessen
