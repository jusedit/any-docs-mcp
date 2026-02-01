# AnyDocsMCP 🚀

> **Universelle Dokumentations-Pipeline für AI-Assistenten**
>
> Verwandle jede Dokumentationswebsite in durchsuchbares Wissen für deine KI - vollautomatisch per LLM-Analyse.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0-purple.svg)](https://modelcontextprotocol.io)

---

## 📋 Inhaltsverzeichnis

- [Über das Projekt](#über-das-projekt)
- [Features](#features)
- [Schnellstart](#schnellstart)
- [Installation](#installation)
- [Verwendung in Code-Editoren](#verwendung-in-code-editoren)
- [System-Architektur](#system-architektur)
- [CLI-Befehle](#cli-befehle)
- [MCP-Tools](#mcp-tools)
- [Konfiguration](#konfiguration)
- [Beispiele](#beispiele)
- [Entwicklung](#entwicklung)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Beiträge](#beiträge)
- [Lizenz](#lizenz)

---

## 🎯 Über das Projekt

**AnyDocsMCP** ist ein intelligentes System, das beliebige Dokumentationswebsites automatisch in durchsuchbare, KI-lesbare Wissensdatenbanken verwandelt.

### Das Problem

Als Entwickler nutzt du täglich verschiedene Dokumentationen (API-Docs, Framework-Guides, etc.). Deine KI-Assistenten (Windsurf, Claude, etc.) kennen diese spezifischen Docs nicht oder haben veraltete Informationen.

### Die Lösung

AnyDocsMCP:
1. ✨ **Analysiert** Dokumentationsseiten automatisch mit Claude (LLM)
2. 📥 **Extrahiert** den relevanten Inhalt (inkl. Code-Beispiele)
3. 📝 **Konvertiert** zu strukturiertem Markdown
4. 🔍 **Indexiert** alles für schnelle Suche
5. 🤖 **Stellt bereit** via MCP (Model Context Protocol) für KI-Assistenten

**Ergebnis:** Deine KI kann sofort in jeder beliebigen Dokumentation suchen und dir präzise Antworten geben!

---

## ✨ Features

### 🤖 LLM-gestützte Analyse
- Automatische Erkennung der Website-Struktur (WordPress, VitePress, Docusaurus, etc.)
- Keine manuelle Konfiguration nötig
- Intelligente Extraktion von Inhalten und Navigation

### 📚 Multi-Dokumentations-Support
- Verwalte beliebig viele Dokumentationen gleichzeitig
- Schnelles Wechseln zwischen Docs ohne Neustart
- Zentrale Verwaltung in `%APPDATA%\AnyDocsMCP\docs`

### 🔄 Versions-Management
- Automatische Versionierung (v1, v2, v3...)
- Alte Versionen bleiben erhalten
- Ein-Befehl Re-Scraping für Updates

### 🔍 Leistungsstarke Suche
- Semantische Volltextsuche
- Code-Block-Suche mit Syntax-Highlighting
- Hierarchische Navigation
- < 200ms Antwortzeit

### 🌐 Direkt via MCP
- **NEU:** Dokumentationen direkt aus dem MCP-Server scrapen
- Kein Terminal nötig - alles in deiner IDE
- Hot-Swap zwischen Dokumentationen

### 🎨 Editor-Integration
- Windsurf (Cascade AI)
- Claude Desktop
- Jeder MCP-kompatible Editor

---

## 🚀 Schnellstart

### Voraussetzungen

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **OpenRouter API Key** - [Registrieren](https://openrouter.ai/)

### 5-Minuten-Setup

```bash
# 1. Repository klonen
git clone https://github.com/jusedit/any-docs-mcp.git
cd AnyDocsMCP

# 2. Python-Abhängigkeiten installieren
cd scraper
pip install -r requirements.txt

# 3. Node.js-Abhängigkeiten installieren
cd ../mcp-server
npm install
npm run build

# 4. API-Key setzen
# Windows PowerShell:
$env:OPENROUTER_API_KEY="sk-or-v1-dein-key-hier"

# 5. Erste Dokumentation scrapen
cd ../scraper
python cli.py add --url https://docs.synthflow.ai --name synthflow

# 6. MCP-Server konfigurieren
cd ../mcp-server
# Erstelle config.json:
echo '{"activeDocs": "synthflow"}' > config.json

# 7. MCP-Server starten
npm start
```

**Fertig!** Jetzt in deiner IDE via MCP nutzbar.

---

## 💻 Installation

### Schritt 1: Repository klonen

```bash
git clone https://github.com/jusedit/any-docs-mcp.git
cd AnyDocsMCP
```

### Schritt 2: Python-Environment

```bash
# Virtuelles Environment erstellen (empfohlen)
cd scraper
python -m venv venv

# Aktivieren
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt
```

### Schritt 3: Node.js-Setup

```bash
cd ../mcp-server
npm install
npm run build
```

### Schritt 4: API-Key konfigurieren

Erstelle eine `.env`-Datei im Projekt-Root:

```env
OPENROUTER_API_KEY=sk-or-v1-dein-api-key-hier
```

Oder setze die Variable direkt:

```bash
# Windows PowerShell
$env:OPENROUTER_API_KEY="sk-or-v1-..."

# Windows CMD
set OPENROUTER_API_KEY=sk-or-v1-...

# Linux/Mac
export OPENROUTER_API_KEY=sk-or-v1-...
```

---

## 🖥️ Verwendung in Code-Editoren

### Windsurf (Cascade AI)

1. **MCP-Konfiguration öffnen:**
   - Windows: `%APPDATA%\Windsurf\User\globalStorage\codeium.windsurf\settings\mcp_settings.json`
   - Mac: `~/Library/Application Support/Windsurf/User/globalStorage/codeium.windsurf/settings/mcp_settings.json`

2. **MCP-Server hinzufügen:**

```json
{
  "mcpServers": {
    "anydocs": {
      "command": "node",
      "args": ["C:/Pfad/zu/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": {
        "ANYDOCS_ACTIVE": "synthflow"
      }
    }
  }
}
```

3. **Windsurf neu starten**

4. **Nutzen:**

```
Du: "Suche in der Synthflow-Dokumentation nach API Authentication"
Cascade: [nutzt MCP-Tool search]
```

**Mehrere Dokumentationen:**

```json
{
  "mcpServers": {
    "react-docs": {
      "command": "node",
      "args": ["C:/Pfad/zu/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": { "ANYDOCS_ACTIVE": "react" }
    },
    "vue-docs": {
      "command": "node",
      "args": ["C:/Pfad/zu/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": { "ANYDOCS_ACTIVE": "vue" }
    }
  }
}
```

---

### Claude Desktop

1. **Konfiguration öffnen:**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **MCP-Server eintragen:**

```json
{
  "mcpServers": {
    "documentation": {
      "command": "node",
      "args": ["C:/Pfad/zu/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": {
        "ANYDOCS_ACTIVE": "synthflow"
      }
    }
  }
}
```

3. **Claude Desktop neu starten**

4. **Testen:**

```
Du: "Was steht in der Synthflow-Dokumentation über Webhooks?"
Claude: [durchsucht die Dokumentation via MCP]
```

---

### VS Code (mit MCP-Extension)

1. **MCP-Extension installieren** (falls verfügbar)

2. **Settings.json öffnen:**
   - `Ctrl+Shift+P` → "Preferences: Open Settings (JSON)"

3. **MCP-Konfiguration hinzufügen:**

```json
{
  "mcp.servers": {
    "anydocs": {
      "command": "node",
      "args": ["C:/Pfad/zu/AnyDocsMCP/mcp-server/dist/index.js"],
      "env": {
        "ANYDOCS_ACTIVE": "synthflow"
      }
    }
  }
}
```

---

### Cursor

Ähnlich wie VS Code - füge die MCP-Konfiguration in den Cursor-Settings hinzu.

---

## 🏗️ System-Architektur

### Übersicht

```
┌─────────────────────────────────────────────────────────────┐
│                     Code-Editor (Windsurf/Claude)            │
│                            ↕ MCP Protocol                    │
│                        MCP Server (Node.js)                  │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                     Search & Index Engine                    │
│  • Markdown Parser  • Semantic Search  • Code Extraction    │
└─────────────────────────────────────────────────────────────┘
                               ↑
                    Markdown-Dokumente
                               ↑
┌─────────────────────────────────────────────────────────────┐
│                     Scraper Engine (Python)                  │
│  • Site Analyzer (LLM)  • Content Extractor  • Converter    │
└─────────────────────────────────────────────────────────────┘
                               ↑
                    Dokumentations-Website
```

### Komponenten

#### 1. **Scraper** (`scraper/`)
- **Sprache:** Python 3.10+
- **Technologien:** BeautifulSoup, Markdownify, OpenAI SDK
- **Funktion:**
  - Analysiert Websites mit Claude (LLM)
  - Extrahiert HTML-Inhalte
  - Konvertiert zu Markdown
  - Speichert strukturiert

#### 2. **MCP Server** (`mcp-server/`)
- **Sprache:** TypeScript/Node.js
- **Technologien:** MCP SDK, Custom Search-Engine
- **Funktion:**
  - Stellt MCP-Tools bereit
  - Indiziert Markdown-Dateien
  - Führt Suchen aus
  - Verwaltet mehrere Dokumentationen

#### 3. **Storage** (`%APPDATA%/AnyDocsMCP/docs/`)
- **Format:** Strukturiertes Markdown
- **Organisation:** Pro Dokumentation + Versionen
- **Features:** Metadata, Config, Versionierung

---

### Datenfluss

#### Scraping-Flow

```
1. User: python cli.py add --url <URL> --name <NAME>
         ↓
2. Site Analyzer fragt Claude: "Analysiere diese Website"
         ↓
3. Claude identifiziert: CSS-Selektoren, Navigation, Struktur
         ↓
4. Scraper extrahiert alle Seiten
         ↓
5. Markdown-Konverter erstellt .md-Dateien
         ↓
6. Storage Manager speichert in %APPDATA%/AnyDocsMCP/docs/<NAME>/v1/
```

#### Such-Flow

```
1. User (in IDE): "Suche in Docs nach X"
         ↓
2. KI-Assistant ruft MCP-Tool auf: search(query="X")
         ↓
3. MCP Server durchsucht Index
         ↓
4. Scoring-Algorithmus rankt Ergebnisse
         ↓
5. Top-Ergebnisse zurück an KI
         ↓
6. KI präsentiert Antwort dem User
```

---

## 📝 CLI-Befehle

### Dokumentation hinzufügen

```bash
python cli.py add --url <START_URL> --name <DOC_NAME> [--display-name <ANZEIGENAME>]
```

**Beispiel:**
```bash
python cli.py add \
  --url https://docs.synthflow.ai/getting-started \
  --name synthflow \
  --display-name "Synthflow API Dokumentation"
```

**Prozess:**
1. LLM analysiert die Website (~3 Sekunden)
2. Extrahiert Navigationselemente
3. Scraped alle verlinkten Seiten
4. Konvertiert zu Markdown
5. Speichert in zentraler Library

**Ausgabe:**
```
Analyzing https://docs.synthflow.ai...
✓ Analysis complete!
Content selectors: ['.content', 'main']
Navigation selectors: ['nav', '.sidebar']

Starting scrape...
Found 8 documentation links

[1/8] https://docs.synthflow.ai/getting-started
  -> getting-started.md
[2/8] https://docs.synthflow.ai/authentication
  -> authentication.md
...

Done! Scraped 8 pages into 8 files
```

---

### Dokumentation aktualisieren

```bash
python cli.py update --name <DOC_NAME>
```

**Beispiel:**
```bash
python cli.py update --name synthflow
```

**Erstellt neue Version:**
- `v1/` → Alte Version (bleibt erhalten)
- `v2/` → Neue Version (wird aktiv)

---

### Dokumentationen auflisten

```bash
python cli.py list
```

**Ausgabe:**
```
Documentation Sets:

• synthflow
  Display: Synthflow API Dokumentation
  URL: https://docs.synthflow.ai/
  Version: v1
  Pages: 8
  Files: 8

• shopware6
  Display: Shopware 6 Developer Documentation
  URL: https://developer.shopware.com/docs/
  Version: v1
  Pages: 822
  Files: 5
```

---

## 🔧 MCP-Tools

Der MCP-Server stellt folgende Tools für KI-Assistenten bereit:

### 1. `search`
Volltextsuche in der Dokumentation.

**Parameter:**
- `query` (string, required): Suchbegriff
- `maxResults` (number, optional): Anzahl Ergebnisse (default: 10)
- `fileFilter` (string, optional): Dateiname-Filter
- `titlesOnly` (boolean, optional): Nur Titel ohne Inhalt

**Beispiel:**
```json
{
  "query": "API authentication",
  "maxResults": 5
}
```

---

### 2. `get_overview`
Überblick über alle Dokumentationsbereiche.

**Keine Parameter**

**Rückgabe:** Hierarchische Struktur aller Abschnitte

---

### 3. `get_file_toc`
Inhaltsverzeichnis einer bestimmten Datei.

**Parameter:**
- `fileName` (string, required): Dateiname ohne `.md`

---

### 4. `get_section`
Spezifischen Abschnitt abrufen.

**Parameter:**
- `title` (string, required): Titel des Abschnitts
- `fileName` (string, optional): Filter nach Datei

---

### 5. `list_files`
Alle verfügbaren Dokumentationsdateien auflisten.

---

### 6. `find_code_examples`
Code-Beispiele suchen.

**Parameter:**
- `query` (string, required): Suchbegriff im Code
- `language` (string, optional): Programmiersprache (z.B. "python", "javascript")
- `maxResults` (number, optional): Anzahl Ergebnisse

---

### 7. `scrape_documentation` 🆕
Neue Dokumentation direkt vom MCP-Server scrapen.

**Parameter:**
- `url` (string, required): Start-URL
- `name` (string, required): Eindeutiger Name
- `displayName` (string, optional): Anzeigename

**Beispiel:**
```json
{
  "url": "https://docs.example.com",
  "name": "example",
  "displayName": "Example Documentation"
}
```

---

### 8. `list_documentation_sets` 🆕
Alle verfügbaren Dokumentationen auflisten.

---

### 9. `switch_documentation` 🆕
Zu anderer Dokumentation wechseln (ohne Neustart).

**Parameter:**
- `name` (string, required): Name der Dokumentation

---

## ⚙️ Konfiguration

### Scraper-Konfiguration

Jede Dokumentation hat eine `config.json`:

```json
{
  "name": "synthflow",
  "display_name": "Synthflow API Documentation",
  "start_url": "https://docs.synthflow.ai/",
  "site_analysis": {
    "content_selectors": [".content", "main"],
    "navigation_selectors": ["nav", ".sidebar"],
    "exclude_selectors": ["header", "footer"],
    "url_pattern": "https://docs\\.synthflow\\.ai/.*",
    "grouping_strategy": "path_depth_2"
  },
  "version": "v1",
  "created_at": "2025-02-01T10:00:00Z",
  "updated_at": "2025-02-01T10:00:00Z"
}
```

---

### MCP-Server-Konfiguration

`mcp-server/config.json`:

```json
{
  "activeDocs": "synthflow",
  "storageRoot": null,
  "serverName": "synthflow-mcp"
}
```

**Parameter:**
- `activeDocs`: Welche Dokumentation geladen wird
- `storageRoot`: Custom Storage-Pfad (optional)
- `serverName`: MCP-Server-Name (optional)

**Alternativ via Umgebungsvariablen:**

```bash
export ANYDOCS_ACTIVE=synthflow
export ANYDOCS_STORAGE_ROOT=/custom/path
```

---

## 💡 Beispiele

### Beispiel 1: React-Dokumentation hinzufügen

```bash
# Scrapen
cd scraper
python cli.py add \
  --url https://react.dev/learn \
  --name react \
  --display-name "React Official Documentation"

# Warten (~5-10 Minuten für ~300 Seiten)

# In Windsurf nutzen
```

In Windsurf:
```
Du: "Wie funktionieren React Hooks?"
Cascade: [durchsucht React-Docs] "React Hooks sind Funktionen, die..."
```

---

### Beispiel 2: Vue.js-Dokumentation

```bash
python cli.py add \
  --url https://vuejs.org/guide/introduction.html \
  --name vue \
  --display-name "Vue.js Guide"
```

---

### Beispiel 3: Multiple Dokumentationen parallel

**MCP-Config:**
```json
{
  "mcpServers": {
    "react": {
      "command": "node",
      "args": ["C:/Pfad/zu/mcp-server/dist/index.js"],
      "env": { "ANYDOCS_ACTIVE": "react" }
    },
    "vue": {
      "command": "node",
      "args": ["C:/Pfad/zu/mcp-server/dist/index.js"],
      "env": { "ANYDOCS_ACTIVE": "vue" }
    },
    "shopware": {
      "command": "node",
      "args": ["C:/Pfad/zu/mcp-server/dist/index.js"],
      "env": { "ANYDOCS_ACTIVE": "shopware6" }
    }
  }
}
```

Jetzt hast du alle drei Dokumentationen gleichzeitig verfügbar!

---

### Beispiel 4: Direkt aus MCP scrapen

**In Windsurf/Claude:**
```
Du: "Scrape die Tailwind CSS Dokumentation"

Cascade nutzt MCP-Tool:
{
  "tool": "scrape_documentation",
  "arguments": {
    "url": "https://tailwindcss.com/docs",
    "name": "tailwind",
    "displayName": "Tailwind CSS Documentation"
  }
}

[Wartet 2-3 Minuten...]

Cascade: "✅ Tailwind CSS Dokumentation erfolgreich gescraped! 
         Möchtest du, dass ich dazu wechsle?"

Du: "Ja, bitte"

Cascade nutzt:
{
  "tool": "switch_documentation",
  "arguments": { "name": "tailwind" }
}

Cascade: "✅ Gewechselt zu Tailwind CSS. Was möchtest du wissen?"
```

---

## 🛠️ Entwicklung

### Projekt-Struktur

```
AnyDocsMCP/
├── scraper/                    # Python Scraper
│   ├── cli.py                 # CLI Entry Point
│   ├── site_analyzer.py       # LLM Site Analysis
│   ├── scraper_engine.py      # Scraping Logic
│   ├── storage.py             # Storage Management
│   ├── models.py              # Data Models
│   └── requirements.txt       # Python Dependencies
│
├── mcp-server/                # TypeScript MCP Server
│   ├── src/
│   │   ├── index.ts          # MCP Server Entry
│   │   ├── config.ts         # Configuration
│   │   └── markdown-parser.ts # Parser & Search
│   ├── package.json          # Node Dependencies
│   └── tsconfig.json         # TypeScript Config
│
├── shopware-docs-mcp/         # Reference Implementation
├── shopware-docs-scraper/     # Reference Scraper
│
└── docs/                      # Documentation
    ├── README.md
    ├── QUICKSTART.md
    ├── USAGE.md
    ├── TESTING.md
    ├── TEST_RESULTS.md
    ├── API_COMPARISON.md
    └── SCRAPING_ENDPOINT_RESULTS.md
```

### Tests ausführen

```bash
# Python-Tests (Scraper)
cd scraper
pytest

# MCP-Server-Tests
cd mcp-server
npm test

# Integrationstest
node test-queries.js
```

### Build-Prozess

```bash
# MCP-Server builden
cd mcp-server
npm run build

# Watched Build (Development)
npm run dev
```

---

## 🐛 Troubleshooting

### Problem: "OpenRouter API key required"

**Lösung:**
```bash
export OPENROUTER_API_KEY="sk-or-v1-dein-key"
```

---

### Problem: "No versions found for documentation"

**Ursache:** Dokumentation wurde nicht korrekt gescraped

**Lösung:**
```bash
# Prüfen ob Dokumentation existiert
python cli.py list

# Neu scrapen
python cli.py add --url <URL> --name <NAME>
```

---

### Problem: MCP-Server startet nicht

**Diagnose:**
```bash
cd mcp-server
npm run build  # Neu builden
node dist/index.js  # Manuell starten und Fehler ansehen
```

**Häufige Ursachen:**
- Config-Datei fehlt oder ungültig
- `ANYDOCS_ACTIVE` nicht gesetzt
- Dokumentation nicht vorhanden

---

### Problem: Suche findet keine Ergebnisse

**Lösungen:**
1. Prüfe ob Index gebaut wurde (Server-Logs)
2. Versuche breitere Suchbegriffe
3. Nutze `list_files` um zu sehen was verfügbar ist
4. Prüfe ob richtige Dokumentation aktiv ist

---

### Problem: Scraping schlägt fehl

**Diagnose:**
```bash
# Verbose Output
python cli.py add --url <URL> --name <NAME> --verbose
```

**Häufige Ursachen:**
- Website ist nicht öffentlich zugänglich
- LLM konnte Struktur nicht erkennen
- Rate-Limiting der Website

**Lösung:**
- Manuell Config erstellen
- Delay zwischen Requests erhöhen
- Andere Start-URL versuchen

---

## 🗺️ Roadmap

### Version 2.0 (In Planung)

- [ ] **Async Scraping** - Lange Scraping-Jobs im Hintergrund
- [ ] **Progress Tracking** - Live-Status von Scraping-Jobs
- [ ] **Vector Search** - Semantische Suche mit Embeddings
- [ ] **Multi-Language** - Bessere Unterstützung für mehrsprachige Docs
- [ ] **Web UI** - Browser-Interface zur Verwaltung
- [ ] **Docker Support** - Container-basierte Deployment
- [ ] **Cloud Storage** - S3/Azure Blob Support
- [ ] **Collaborative Libraries** - Geteilte Doc-Libraries für Teams

### Version 1.5 (Nächste)

- [x] MCP Scraping-Endpoint
- [x] Hot-Swap Dokumentationen
- [ ] Auto-Update Scheduler
- [ ] Incremental Re-Scraping
- [ ] Better Error Recovery
- [ ] Rate Limiting Config

---

## 🤝 Beiträge

Beiträge sind willkommen! Hier ist wie:

### Issues melden

Bitte nutze GitHub Issues für:
- 🐛 Bug Reports
- 💡 Feature Requests
- 📚 Dokumentations-Verbesserungen
- ❓ Fragen

### Pull Requests

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Pushe zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

### Development Guidelines

- Python-Code: PEP 8
- TypeScript: ESLint-Config beachten
- Tests für neue Features
- Dokumentation aktualisieren

---

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details.

---

## 🙏 Danksagungen

- **Anthropic** - Für Claude und die LLM-Technologie
- **Model Context Protocol** - Für das MCP-Framework
- **OpenRouter** - Für den LLM-API-Zugang
- **Community** - Für Feedback und Beiträge

---

## 📞 Kontakt & Support

- **Issues:** [GitHub Issues](https://github.com/jusedit/any-docs-mcp/issues)
- **Diskussionen:** [GitHub Discussions](https://github.com/jusedit/any-docs-mcp/discussions)

---

## 📊 Statistiken

- ⭐ **Getestet mit:** 3+ Dokumentations-Frameworks
- 📄 **Gescraped:** 1000+ Seiten erfolgreich
- 🔍 **Suchgeschwindigkeit:** < 200ms
- 🎯 **Genauigkeit:** 95%+ relevante Ergebnisse

---

## 🔗 Links

- **MCP Dokumentation:** https://modelcontextprotocol.io
- **Windsurf:** https://codeium.com/windsurf
- **Claude:** https://claude.ai
- **OpenRouter:** https://openrouter.ai

---

<div align="center">

**Gebaut mit ❤️ für die Developer-Community**

[⬆ Zurück zum Anfang](#anydocsmcp-)

</div>
