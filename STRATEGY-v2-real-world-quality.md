# Strategie v2: Real-World Quality Upgrade

## Analyse-Ergebnis (Ist-Zustand)

### Datenbasis
- **46 Doc-Sets** in `%APPDATA%/AnyDocsMCP/docs`
- **2.103 Markdown-Dateien**, 54 MB Gesamtdaten
- Bandbreite: von 1 Datei (hyperapp-github) bis 645 Dateien (onoffice)
- Durchschnittsgröße: 26 KB/Datei, Extremwerte: 158 Bytes bis 7.7 MB

### Identifizierte Qualitätsprobleme (echte Daten)

| Problem | Betroffene Dateien | Schwere | Beispiel-Quellen |
|---------|-------------------|---------|------------------|
| **Broken Encoding** (`Â`, `â€™`, `â€œ`) | 622+ | KRITISCH | fastapi (100%), django (95%), react (100%) |
| **"Show more" Buttons** | 161 | HOCH | react, tailwind, synthflow |
| **"On this page" TOC-Reste** | 153 | HOCH | kubernetes, django, nextjs |
| **Permalink-Anker** (`¶` in Headings) | 622 | HOCH | fastapi, django, kubernetes |
| **Cookie-Banner-Reste** | 65 | MITTEL | synthflow, onoffice |
| **CodeSandbox/ReloadClear** | 6 | NIEDRIG | react |
| **sp-pre-placeholder Code-Tags** | 6 | NIEDRIG | react |
| **Leere/Stub-Seiten** (<500 Bytes) | 20+ | MITTEL | tailwind (docs-installation.md = 370B), fastapi (about.md = 220B) |
| **Monster-Dateien** (>1 MB) | ~10 | HOCH | nextjs (avg 2.3 MB), nodejs (avg 3 MB) |
| **Referenz-Tabellen-Bloat** | ~50 | MITTEL | tailwind border-color.md = 264 KB reine Farbtabellen |

### Was die bisherigen Tests NICHT abdecken
1. Tests verwenden **synthetische HTML-Fixtures** mit sauberem Markup
2. **Kein einziger Test** prüft gegen echte gescrapte Dokumente
3. **Search-Relevanz** wird gegen 2 kleine Fixture-Dateien gemessen (10 Sections)
4. **Encoding-Fixes** im ContentCleaner decken nur einen Bruchteil der echten Fälle ab
5. **Heading-Normalisierung** wurde nie gegen echte Permalink-Anker getestet
6. **MCP E2E-Tests** verwenden generierte Dummy-Docs, nicht reale Strukturen

---

## Architektur: Replay-basiertes Test-System

### Kernidee: "Scrape Once, Test Forever"

```
┌──────────────────────────────────────────────────────────────────┐
│                    EINMALIG (Setup-Phase)                        │
│                                                                  │
│  Echte URLs  ──▶  HTTP-Response-Capture  ──▶  Fixture-Archiv    │
│                   (Headers + Body + Status)     (lokales .har)   │
│                                                                  │
│  Scraper + echte Responses  ──▶  Golden Markdown Output         │
│                                    (erwartete Ergebnisse)        │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                   BEI JEDEM TEST-RUN                             │
│                                                                  │
│  Fixture-Archiv  ──▶  Local Mock Server  ──▶  Scraper Pipeline  │
│  (kein Netzwerk)      (responses replay)      (volle Pipeline)  │
│                                                                  │
│  Scraper Output  ──▶  vs. Golden Output  ──▶  PASS/FAIL         │
│                                                                  │
│  Golden Markdown  ──▶  MCP MarkdownParser  ──▶  Search Queries  │
│                        (Index + Search)         vs. Expected     │
└──────────────────────────────────────────────────────────────────┘
```

### Warum dieser Ansatz?
- **Deterministisch**: Gleicher Input → gleicher Output, immer
- **Offline**: Kein Netzwerkzugriff nach einmaligem Capture
- **Regressionssicher**: Jede Verbesserung wird gegen echte Daten validiert
- **Schnell**: Mock-Server ist lokal, keine Latenz
- **Ehrlich**: Testet die echte Pipeline, nicht vereinfachte Szenarien

---

## Gewählte Referenz-Dokumentationen (10 Stück)

Ausgewählt für maximale Diversity der Problemklassen:

| # | Doc-Set | Typ | Dateien | Primäres Testproblem |
|---|---------|-----|---------|---------------------|
| 1 | **react** | SPA + CodeSandbox | 13 | ReloadClear, sp-pre-placeholder, Show more |
| 2 | **fastapi** | MkDocs + Permalink-Anker | 132 | Encoding (`Â¶`, `â€™`), Permalink in Headings |
| 3 | **tailwind** | Utility-Referenz | 560 | Monster-Tabellen (264 KB), Leere Stubs |
| 4 | **kubernetes** | Hugo-basiert | 61 | "On this page" TOC, große Dateien (avg 111 KB) |
| 5 | **django** | Sphinx-basiert | 60 | Encoding, Navigation-Reste, "Show more" |
| 6 | **hyperapp-github** | GitHub Raw MD | 1 | RAW_MARKDOWN Source, Single-File 125 KB |
| 7 | **onoffice** | Custom API-Docs | 645 | Höchste Dateianzahl, viele Leere Stubs |
| 8 | **synthflow** | SPA + Cookie-Banner | 143 | Cookie-Reste, Encoding, "Show more" |
| 9 | **golang** | Custom Go-Docs | 18 | Mittelgroß, Encoding |
| 10 | **rust-book** | mdBook | 1 | Single-File Book-Format |

---

## Epic-Struktur für Ralph Deep Init

### Epic 1: HTTP-Response-Capture-System (Infrastruktur)

**Ziel:** Einmalig echte HTTP-Responses capturen und als Fixtures speichern.

- **Task 1.1:** `ResponseCapture` Klasse — Speichert Response (Status, Headers, Body) als JSON+HTML-Paar pro URL
- **Task 1.2:** Capture-Script für die 10 Referenz-Docs — Pro Doc-Set: 5 repräsentative Seiten capturen (Startseite, Tutorial, API-Ref, Code-Example, Edge-Case)
- **Task 1.3:** Fixture-Verzeichnis-Struktur — `tests/fixtures/real-world/{doc-name}/{url-hash}.json` + `.html`
- **Task 1.4:** `MockHTTPServer` Klasse — `http.server`-basiert, replayed Fixtures nach URL-Pattern, für pytest verfügbar

### Epic 2: Encoding-Qualität (Kritischstes Problem)

**Ziel:** Die 622 Dateien mit Broken Encoding auf 0 reduzieren.

- **Task 2.1:** Encoding-Audit-Script — Scannt alle echten Docs, kategorisiert Encoding-Fehler nach Typ
- **Task 2.2:** Permalink-Anker-Bereinigung — `Â¶` + `[¶](#...)` Muster aus Headings entfernen (FastAPI, Django, Sphinx-Docs)
- **Task 2.3:** Erweiterte UTF-8-Mojibake-Reparatur — Systematische Mapping-Tabelle für â€™→', â€œ→", Â→(remove), etc.
- **Task 2.4:** Encoding-Regression-Tests — Pro Referenz-Doc: Fixture mit kaputtem Encoding → Golden Output ohne
- **Task 2.5:** Content-Type + Charset-Detection — `fetch_page` prüft `charset` aus Response-Header, konvertiert bei Bedarf

### Epic 3: UI-Artefakt-Bereinigung v2 (Echte Patterns)

**Ziel:** Alle 161 "Show more", 153 "On this page", 65 Cookie-Reste eliminieren.

- **Task 3.1:** Pattern-Discovery-Script — Scannt echte Docs, extrahiert wiederkehrende Non-Content-Patterns automatisch
- **Task 3.2:** Site-spezifische Pattern-Profile — ContentCleaner akzeptiert `site_patterns: Dict[str, List[str]]` für Framework-spezifische Regeln
- **Task 3.3:** MkDocs-Profil — Permalink-Anker, "Edit on GitHub", "Last updated", Admonition-Syntax
- **Task 3.4:** React/Docusaurus-Profil — CodeSandbox, "Show more", Tab-Switcher-Reste
- **Task 3.5:** Sphinx-Profil — Note/Warning-Boxen, "Changed in version", "New in version"
- **Task 3.6:** Hugo-Profil — "On this page" TOC, Breadcrumbs, "Last modified"
- **Task 3.7:** Regressions-Tests mit echten Fixture-Snippets pro Profil

### Epic 4: Content-Sizing & Chunking

**Ziel:** Monster-Dateien (3 MB nodejs) und Stub-Seiten (220 Bytes) behandeln.

- **Task 4.1:** Maximale Dateigröße — Warnung + Split bei >500 KB, Konfigurierbar
- **Task 4.2:** Stub-Seiten-Erkennung — Seiten <500 Chars werden gemerged oder entfernt
- **Task 4.3:** Tabellen-Kompression — Referenz-Tabellen (Tailwind: 264 KB Farbtabelle) intelligenter zusammenfassen
- **Task 4.4:** Duplikat-Seiten-Erkennung — v1/v2/v3 gleicher Docs (tailwind hat 4 Versionen!) automatisch erkennen
- **Task 4.5:** Content-Quality-Score pro Seite — Metrik: `(heading_count * code_blocks * 10) / total_artifacts`

### Epic 5: Search-Relevanz mit echten Daten

**Ziel:** Suchqualität gegen reale Korpora statt synthetische Fixtures messen.

- **Task 5.1:** Realer Query-Suite-Generator — Aus den 10 Referenz-Docs jeweils 10 natürliche Queries + erwartetes Ergebnis manuell definieren (100 Queries total)
- **Task 5.2:** Multi-Corpus-Benchmark — MarkdownParser gegen jedes der 10 echten Doc-Sets laufen lassen, precision@1/3/MRR messen
- **Task 5.3:** Large-Corpus-Performance — Index-Build + Search-Latency für onoffice (645 Dateien) und tailwind (560 Dateien) messen
- **Task 5.4:** Cross-File-Search-Qualität — Queries die Ergebnisse aus mehreren Dateien erwarten
- **Task 5.5:** Code-Search-Spezifisch — Queries wie "React useState example", "FastAPI dependency injection" gegen echte Docs

### Epic 6: End-to-End Pipeline-Tests

**Ziel:** Volle Scrape→Clean→Index→Search Pipeline gegen MockServer testen.

- **Task 6.1:** Pipeline-Smoke-Test pro Referenz-Doc — MockServer → Scrape → Verify Markdown Output
- **Task 6.2:** Golden-Output-Snapshots — Pro Referenz-Doc: erwarteter Markdown-Output als Fixture
- **Task 6.3:** Diff-basierte Regression — Neue Scraper-Version vs. Golden Output, Änderungen müssen reviewed werden
- **Task 6.4:** MCP-Tool-Integration — search/get_overview/get_file_toc gegen echte Docs verifizieren
- **Task 6.5:** Quality-Dashboard — JSON-Report mit Metriken pro Doc-Set nach jedem Test-Run

---

## Priorisierung

```
Woche 1:  Epic 1 (Infrastruktur) + Epic 2 (Encoding — kritischstes Problem)
Woche 2:  Epic 3 (UI-Artefakte v2) + Epic 4 (Content-Sizing)
Woche 3:  Epic 5 (Search-Relevanz) + Epic 6 (E2E Pipeline)
```

## Fixture-Budget

Damit die Test-Suite handhabbar bleibt:

- **Pro Referenz-Doc:** Max. 5 gecapturte HTML-Seiten (= 50 HTML-Fixtures total)
- **Pro Referenz-Doc:** 1 Golden-Markdown-Output (= 10 Golden-Dateien)
- **Pro Referenz-Doc:** 10 Suchqueries (= 100 Query-Paare total)
- **Gesamtgröße Fixtures:** ~20 MB (HTML + Golden + Queries)
- **Fixture-Speicherort:** `tests/fixtures/real-world/` (git-tracked)

## MockServer-Architektur

```python
class FixtureHTTPServer:
    """Replays captured HTTP responses from fixtures directory."""
    
    def __init__(self, fixtures_dir: str):
        self.fixtures = self._load_fixtures(fixtures_dir)
        # Maps URL patterns to fixture files
    
    def start(self, port: int = 0) -> str:
        """Start server on random port, return base URL."""
        # Returns: http://localhost:12345
    
    def stop(self):
        """Stop server."""
    
    def get_base_url(self, doc_name: str) -> str:
        """Get rewritten base URL for a doc set."""
        # Original: https://react.dev/learn/...
        # Rewritten: http://localhost:12345/react/learn/...
```

**Pytest-Integration:**
```python
@pytest.fixture
def mock_server(tmp_path):
    server = FixtureHTTPServer("tests/fixtures/real-world")
    base_url = server.start()
    yield server
    server.stop()

def test_react_scrape_quality(mock_server):
    config = DocumentationConfig(
        start_url=mock_server.get_base_url("react"),
        ...
    )
    engine = ScraperEngine(config, storage)
    result = engine.scrape_all("v1")
    # Assert against golden output
```

## Erfolgskriterien

| Metrik | Aktuell | Ziel v2 |
|--------|---------|---------|
| Encoding-Fehler in echten Docs | 622 Dateien | 0 |
| UI-Artefakte ("Show more", etc.) | 161+ Dateien | <10 |
| Permalink-Anker in Headings | 622 Dateien | 0 |
| Search Precision@1 (synthetisch) | ≥80% | ≥80% |
| Search Precision@1 (echte Docs) | nicht gemessen | ≥70% |
| Test-Coverage (echte Datenquellen) | 0 | 10 Doc-Sets |
| Netzwerk-Abhängigkeit der Tests | 0 (aber auch 0 Realismus) | 0 (mit Realismus) |

---

## Zusammenfassung

Die aktuelle Test-Suite validiert Code-Korrektheit gegen synthetische Inputs.
Die nächste Iteration validiert **Ergebnis-Qualität** gegen echte Dokumentationen.

Der Schlüssel ist das **Capture-Replay-Muster**: Einmal echte Responses capturen,
dann offline und deterministisch testen — für immer. Damit haben wir das Beste
aus beiden Welten: echte Daten + schnelle, stabile Tests.
