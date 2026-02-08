# Batch Scrape Analysis — 50 Sites (Stand: 08.02.2026)

## Übersicht: 30/50 Sites fertig, 1 deaktiviert (redis), ~19 laufen noch

## Ergebnistabelle

| Site | Pages | Total KB | Avg KB/Page | AGENTS.md KB | Overhead % | Bewertung |
|------|------:|--------:|-----------:|------------:|-----------:|-----------|
| **angular** | 1495 | 4495 | 3.0 | 29.6 | 0.66% | ⚠️ Zu viele (ext. GitHub-Links) |
| **django** | 324 | 7560 | 23.3 | 5.7 | 0.08% | ✅ Gut (en-only nach Fix) |
| **dotnet** | 235 | 4519 | 19.2 | 8.4 | 0.19% | ✅ Gut (nach Fix) |
| **elasticsearch** | 5 | 31 | 6.2 | 0.4 | 1.29% | ❌ Zu wenig — Scope zu eng |
| **eslint** | 422 | 2819 | 6.7 | 8.6 | 0.31% | ✅ Excellent |
| **fastapi** | 1301 | 22726 | 17.5 | 24.1 | 0.11% | ⚠️ Zu viele (Multi-Locale?) |
| **flask** | 25 | 570 | 22.8 | 0.5 | 0.09% | ⚠️ Zu wenig |
| **git** | 90 | 2200 | 24.4 | 1.5 | 0.07% | ✅ Gut |
| **golang** | 79 | 2039 | 25.8 | 1.3 | 0.06% | ✅ Gut |
| **grpc** | 87 | 911 | 10.5 | 1.7 | 0.19% | ✅ Gut |
| **hyperapp** | 59 | 25 | 0.4 | 1.6 | 6.40% | ⚠️ Overhead hoch (GitHub-Repo) |
| **java-se** | 24 | 90 | 3.8 | 0.7 | 0.78% | ❌ Nur Index-Seiten, keine Doku |
| **kafka** | 80 | 2242 | 28.0 | 1.8 | 0.08% | ✅ Gut |
| **kotlin** | 91 | 4331 | 47.6 | 2.4 | 0.06% | ✅ Gut (nach Fix: 9902→91) |
| **laravel** | 127 | 5474 | 43.1 | 1.7 | 0.03% | ✅ Gut |
| **linux-man** | 642 | 6746 | 10.5 | 11.1 | 0.16% | ✅ OK (500 Cap, nach Fix) |
| **mongodb** | 149 | 1205 | 8.1 | 4.6 | 0.38% | ✅ Gut |
| **mysql** | 1871 | 17725 | 9.5 | 53.0 | 0.30% | ⚠️ Zu viele + "Skip to" Artefakt |
| **nextjs** | 421 | 3006 | 7.1 | 8.5 | 0.28% | ⚠️ "Was this helpful" in 100% |
| **nuxt** | 268 | 1333 | 5.0 | 4.7 | 0.35% | ⚠️ Mojibake + Footer-Artefakte |
| **postgresql** | 1182 | 10966 | 9.3 | 23.9 | 0.22% | ⚠️ Zu viele? |
| **python3** | 25 | — | — | 0.6 | — | ❌ Zu wenig (nur 25 von ~500) |
| **nodejs** | 258 | — | — | 3.8 | — | ✅ Gut |
| **typescript** | 302 | — | — | 6.6 | — | ✅ Gut |
| **rabbitmq** | 156 | 2684 | 17.2 | 0.0 | 0% | ⚠️ Kein AGENTS.md! |
| **rails** | 74 | 2771 | 37.4 | 1.9 | 0.07% | ✅ Gut |
| **react** | 187 | 1203 | 6.4 | 4.0 | 0.33% | ✅ Gut |
| **rust-book** | 104 | 3880 | 37.3 | 3.0 | 0.08% | ✅ Excellent |
| **spring-boot** | 366 | 3342 | 9.1 | 8.8 | 0.26% | ✅ Gut |
| **sqlite** | 130 | 3232 | 24.9 | 1.7 | 0.05% | ✅ Gut |
| **svelte** | 187 | 1446 | 7.7 | 3.0 | 0.21% | ⚠️ Identisch mit sveltekit |
| **sveltekit** | 187 | 1446 | 7.7 | 3.0 | 0.21% | ⚠️ Identisch mit svelte |
| **swagger** | 33 | 92 | 2.8 | 0.9 | 0.98% | ✅ OK (kleine Doku) |
| **tailwind** | 192 | 1432 | 7.5 | 3.4 | 0.24% | ✅ Gut |
| **vite** | 41 | 383 | 9.3 | 0.9 | 0.23% | ✅ Gut |
| **vuejs** | 52 | 626 | 12.0 | 1.8 | 0.29% | ✅ Gut |
| **webpack** | 153 | 2848 | 18.6 | 2.9 | 0.10% | ✅ Gut |

## AGENTS.md Overhead-Analyse

- **Median Overhead:** ~0.2% — vernachlässigbar
- **Worst Case:** hyperapp 6.4% (GitHub-Repo, winzige MD-Dateien)
- **Best Case:** laravel 0.03%
- **Fazit:** AGENTS.md Index-Overhead ist minimal (<1% bei normalen Sites)

## Artefakt-Analyse (Top-Probleme)

| Artefakt | Betroffene Dateien | Schwere |
|---|---:|---|
| `Skip to Main Content` | 1845 | 🔴 Kritisch (MySQL allein 1845) |
| Mojibake (kaputte UTF-8 Emojis) | 1507 | 🔴 Kritisch |
| `Was this helpful` + Feedback | 670 | 🟡 Mittel |
| `Copyright` Footer | 602 | 🟡 Mittel |
| `Cookie` Hinweise | 404 | 🟡 Mittel |
| `MIT License` Footer | 277 | 🟠 Niedrig |
| `Report an issue` | 251 | 🟠 Niedrig |

## Problematische Sites (Handlungsbedarf)

### ❌ Zu wenig Seiten
- **elasticsearch** (5) — Scope zu eng, findet fast nichts
- **python3** (25) — Nur Bruchteil der Python-Doku
- **flask** (25) — Nur Bruchteil
- **java-se** (24) — Nur Index-Seiten pro Version

### ⚠️ Zu viele / Duplikate
- **fastapi** (1301) — Vermutlich Multi-Locale (Cookie in 279 Dateien!)
- **mysql** (1871) — "Skip to Main Content" in fast jeder Datei
- **angular** (1495) — Enthält externe GitHub-Links
- **postgresql** (1182) — Möglicherweise zu breit

### ⚠️ Qualitätsprobleme
- **svelte = sveltekit** — Identischer Inhalt (187 Seiten, gleiche Größe)
- **rabbitmq** — Kein AGENTS.md generiert
- **nuxt** — Mojibake-Emojis + Footer-Artefakte in 249/268 Dateien
- **nextjs** — "Was this helpful" in 100% der Dateien
