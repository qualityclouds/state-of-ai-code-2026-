# The State of AI-Generated Code, 2026

![dataset](https://img.shields.io/badge/dataset-CC--BY--4.0-007ec6)
![scans](https://img.shields.io/badge/scans-429_repos-320537)
![updated](https://img.shields.io/badge/updated-July_2026-8250df)
![engine](https://img.shields.io/badge/engine-Quality_Clouds_Hub-C800D7)

Published July 2026 by [Quality Clouds Hub](https://qualityclouds.com) · Data available under CC-BY-4.0

> **14% of AI-generated projects ship with a leaked secret or hardcoded credential.
> 52% of Supabase-backed apps have at least one client-side security
> misconfiguration. Across 23 million lines of AI-generated code, we found one issue
> every 64 lines.**

## Key findings

- We scanned **429 public projects** built with Lovable, Bolt, v0, and AI-copilot-tagged
  GitHub repos — **23,095,920 lines of code** in total.
- The scans produced **362,115 issues** — **15.7 per 1,000 lines of code**.
- **57%** of all findings are HIGH severity (205,197 of 362,115).
- **14%** of projects shipped at least one leaked secret or hardcoded credential.
- **52%** of the 206 Supabase-backed projects had at least
  one client-side security misconfiguration (exposed service-role keys, client-side auth logic,
  public buckets…).
- **87%** of projects have at least one security finding. Only **57 of 429** are clean on security.
- The single most common HIGH finding — *Async Operation Without Error Handling* — appears in
  **79%** of projects, 138,601 times.

## AI code generators, ranked by quality

Ranked by **issue density** (issues per 1,000 lines of code — lower is better). The ordering is
stable across every independent metric we measured: a platform that is worse on overall density
is also worse on security density and on the share of projects carrying a security finding.

| # | Generator | Repos | Issues / KLOC | Security issues / KLOC | Projects with a security finding | Median issues per project |
|---|---|---|---|---|---|---|
| 1 | **AI-tagged GitHub** (Copilot-assisted) | 92 | **9.5** | **0.32** | 66% | 90 |
| 2 | **Bolt** | 43 | **11.4** | **0.54** | 65% | 134 |
| 3 | **v0** | 111 | 16.5 | 1.10 | 92% | 95 |
| 4 | **Lovable** | 183 | **18.1** | **1.18** | **99%** | **644** |

**What separates them.** Bolt and Copilot-assisted repos produce roughly **half** the issue
density of v0 and Lovable, and **a third to a half** of their security-issue density. The gap is
starkest on security exposure: two thirds of Bolt and Copilot projects carry at least one
security finding, versus **92% for v0 and 99% for Lovable** — of 183 Lovable projects, exactly
one is clean on security.

Lovable's median project also ships **644 issues**, roughly 5× the median of any other platform.
Some of that is Supabase: **84%** of Lovable projects are Supabase-backed (against 3% of
Copilot-assisted repos), and Supabase-backed apps carry a distinct class of client-side security
misconfiguration that the other platforms largely avoid by never reaching for a BaaS.

Issue density by impact area (issues per KLOC, lower is better):

| Generator | Security | Performance | Scalability | Manageability | Maintainability |
|---|---|---|---|---|---|
| AI-tagged GitHub | **0.3** | **0.7** | 5.6 | **1.1** | **1.7** |
| Bolt | 0.5 | 1.2 | **5.4** | 2.6 | **1.7** |
| v0 | 1.1 | **3.5** | 5.8 | **3.9** | 2.2 |
| Lovable | **1.2** | 3.2 | **7.8** | 2.4 | **3.6** |

**Caveat on the leader.** "AI-tagged GitHub" repos are Copilot-*assisted*, not fully
AI-*generated* — a human drove the architecture and reviewed the output. It is a control group
rather than a like-for-like competitor, and the fact that it wins is itself the finding: the more
of the codebase the model authors unsupervised, the worse the density gets.

## By frontend framework

| Framework | Repos | Issues / KLOC |
|---|---|---|
| Python / PHP | 38 | **10.0** |
| Other JS/TS | 44 | 10.5 |
| Next.js | 127 | 13.9 |
| React + Vite | 215 | **17.1** |

React + Vite — the default output of most prompt-to-app tools — is the dirtiest stack in the
corpus, at 71% higher issue density than Python/PHP.

## Issues by impact area

| Impact area | Issues | Repos affected |
|---|---|---|
| Scalability | 160,248 | 390 |
| Maintainability | 67,483 | 387 |
| Performance | 59,006 | 384 |
| Manageability | 53,390 | 394 |
| Security | 21,826 | 372 |
| Architecture | 162 | 29 |

## Top 10 most frequent findings

| Rule | Area | Severity | Issues | % repos |
|---|---|---|---|---|
| Array.forEach() With Async Callback | scalability | MEDIUM | 17,998 | 80% |
| Async Operation Without Error Handling | scalability | HIGH | 138,601 | 79% |
| Nested ternary expression | maintainability | MEDIUM | 34,535 | 78% |
| Synchronous setState Inside useEffect | performance | HIGH | 40,220 | 74% |
| console.log Used Instead of Structured Logging | manageability | MEDIUM | 31,441 | 74% |
| Implicit Boolean Coercion via Double Negation | maintainability | LOW | 23,881 | 73% |
| Network Request Without Timeout | performance | MEDIUM | 12,576 | 71% |
| Empty Catch Block Swallows Errors | manageability | HIGH | 9,761 | 67% |
| Dynamic Value Bound to href Without URL Validation | security | HIGH | 3,511 | 63% |
| Wildcard Dependency Version | security | HIGH | 6,038 | 52% |

## Charts

![Top issues](charts/top-issues.png)

## Methodology

Projects were sampled from public GitHub repositories carrying unambiguous markers of the
generation platform (Lovable/v0/Bolt README templates, AI topics), filtered by size and recency,
capped at 2 repos per owner. Each was scanned with the **same deterministic rule engine and the
same 295 production rules** (Semgrep + regex) that power the Quality Clouds Hub scanner.
**Individual repositories are never named — only aggregate statistics are published.** Full
details in [docs/methodology.md](docs/methodology.md) and [docs/ruleset.md](docs/ruleset.md).

All comparisons in this report are made on **issue density** (issues per 1,000 lines of code)
rather than raw counts, so that larger projects are not penalised for their size.

## Downloads

| File | Contents |
|---|---|
| [data/vibe-code-2026.csv](data/vibe-code-2026.csv) | Per-repo metrics (anonymized), one row per project |
| [data/vibe-code-2026.json](data/vibe-code-2026.json) | Same as above, JSON |
| [data/aggregate-stats.csv](data/aggregate-stats.csv) | Headline aggregate statistics |

## Reproduce

Scan your own repository with the same ruleset at [qualityclouds.com](https://qualityclouds.com) —
import your repo and see every finding in minutes.

## License

**Data:** CC-BY-4.0 — reuse with attribution · **Pipeline code:** MIT
