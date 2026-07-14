"""Generate the publishable report: README.md, charts PNG, data exports, docs.

Reads issues.sqlite (collect.py output). Repos are anonymized in every
published artifact: sequential repo ids only, never slugs/names.
"""

import csv
import json
import sqlite3
from datetime import date

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import MaxNLocator  # noqa: E402

from config import (  # noqa: E402
    CHARTS_DIR,
    DATA_DIR,
    DOCS_DIR,
    ISSUES_DB,
    NORMALIZED_CATALOG,
    PROJECT_ROOT,
)

BAR = "#4a0a52"       # base bars (brand aubergine, lightened for marks)
HIGHLIGHT = "#C800D7"  # highlighted bar (brand raspberry)
INK = "#1a1420"
MUTED = "#6b6472"
GRID = "#ece8f0"

SECRET_RULES = {
    "py-sec-hardcoded-secret-1.0", "sa-sec-engine-url-secret-1.0",
    "ts-ai-provider-key-1.0", "ts-api-key-in-client-1.0", "ts-aws-credentials-1.0",
    "ts-db-connection-string-1.0", "ts-firebase-config-exposed-1.0",
    "ts-generic-secret-assignment-1.0", "ts-hardcoded-bearer-token-1.0",
    "ts-messaging-service-key-1.0", "ts-private-key-in-code-1.0",
    "node-env-file-committed-1.0", "node-no-api-keys-in-env-files-1.0",
    "php-sec-hardcoded-database-credentials-via-local-variable-assignment-1.0",
    "sb-exposed-service-role-key-1.0",
}

FRAMEWORK_LABELS = {
    "nextjs": "Next.js", "react-vite": "React + Vite", "react": "React (other)",
    "vue": "Vue", "svelte": "Svelte", "node-other": "Other JS/TS",
    "remix": "Remix", "other": "Python / PHP",
}

ORIGIN_LABELS = {"lovable": "Lovable", "v0": "v0", "bolt": "Bolt", "generic-ai": "AI-tagged GitHub"}


# --------------------------------------------------------------------------- stats

def _q(conn, sql, params=()):
    return conn.execute(sql, params).fetchall()


def gather_stats(conn):
    s = {}
    s["n_repos"], s["n_issues"], s["total_loc"] = _q(
        conn, "SELECT COUNT(*), SUM(n_issues), SUM(loc) FROM repos"
    )[0]
    s["avg_score"] = round(_q(conn, "SELECT AVG(score) FROM repos WHERE score IS NOT NULL")[0][0])
    s["median_score"] = _q(
        conn,
        "SELECT score FROM repos WHERE score IS NOT NULL ORDER BY score "
        "LIMIT 1 OFFSET (SELECT COUNT(*) FROM repos WHERE score IS NOT NULL)/2",
    )[0][0]
    s["tiers"] = dict(_q(conn, "SELECT tier, COUNT(*) FROM repos GROUP BY tier"))

    marks = ",".join("?" * len(SECRET_RULES))
    s["repos_with_secret"] = _q(
        conn, f"SELECT COUNT(DISTINCT repo_ix) FROM issues WHERE rule_id IN ({marks})",
        tuple(SECRET_RULES),
    )[0][0]
    s["pct_secret"] = round(100 * s["repos_with_secret"] / s["n_repos"])

    s["n_supabase"] = _q(conn, "SELECT COUNT(*) FROM repos WHERE uses_supabase=1")[0][0]
    s["supabase_insecure"] = _q(
        conn,
        "SELECT COUNT(DISTINCT r.repo_ix) FROM repos r JOIN issues i ON i.repo_ix=r.repo_ix "
        "WHERE r.uses_supabase=1 AND i.rule_id LIKE 'sb-%' AND i.impact_area='security'",
    )[0][0]
    s["pct_supabase_insecure"] = (
        round(100 * s["supabase_insecure"] / s["n_supabase"]) if s["n_supabase"] else 0
    )

    s["by_framework"] = _q(
        conn,
        "SELECT framework, COUNT(*), ROUND(AVG(score)), "
        "ROUND(1000.0*SUM(n_issues)/SUM(loc),1) FROM repos "
        "WHERE score IS NOT NULL GROUP BY framework HAVING COUNT(*) >= 5 ORDER BY AVG(score) DESC",
    )
    origins = _q(
        conn,
        "SELECT origin, COUNT(*), ROUND(AVG(score)), ROUND(1000.0*SUM(n_issues)/SUM(loc),1) "
        "FROM repos GROUP BY origin ORDER BY AVG(score) DESC",
    )
    s["by_origin"] = []
    for origin, n, score, per_kloc in origins:
        counts = [r[0] for r in _q(conn, "SELECT n_issues FROM repos WHERE origin=? ORDER BY n_issues", (origin,))]
        s["by_origin"].append((origin, n, score, counts[len(counts) // 2], per_kloc))
    s["by_area"] = _q(
        conn,
        "SELECT impact_area, COUNT(*), COUNT(DISTINCT repo_ix) FROM issues "
        "WHERE impact_area IS NOT NULL GROUP BY impact_area ORDER BY COUNT(*) DESC",
    )
    s["by_severity"] = dict(_q(conn, "SELECT severity, COUNT(*) FROM issues GROUP BY severity"))
    s["top_rules"] = _q(
        conn,
        "SELECT rule_id, MAX(rule_name), MAX(impact_area), MAX(severity), COUNT(*), "
        "COUNT(DISTINCT repo_ix) FROM issues GROUP BY rule_id ORDER BY COUNT(DISTINCT repo_ix) DESC, COUNT(*) DESC LIMIT 10",
    )
    s["distribution"] = _q(
        conn,
        "SELECT MIN(score/10, 9)*10, COUNT(*) FROM repos WHERE score IS NOT NULL "
        "GROUP BY MIN(score/10, 9) ORDER BY 1",
    )
    s["issues_per_kloc"] = round(1000.0 * s["n_issues"] / s["total_loc"], 1)
    return s


# --------------------------------------------------------------------------- charts

def _style_axes(ax):
    ax.spines[:].set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=10, length=0)
    ax.set_axisbelow(True)


def chart_score_by_framework(stats):
    rows = stats["by_framework"]
    labels = [FRAMEWORK_LABELS.get(r[0], r[0]) for r in rows]
    values = [r[2] for r in rows]
    colors = [HIGHLIGHT if v == max(values) else BAR for v in values]
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=150)
    bars = ax.bar(labels, values, color=colors, width=0.62, zorder=3)
    ax.bar_label(bars, fmt="%.0f", padding=4, fontsize=11, fontweight="bold", color=INK)
    ax.grid(axis="y", color=GRID, zorder=0)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Avg Production-Ready Score", color=MUTED, fontsize=10)
    _style_axes(ax)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "score-by-framework.png", facecolor="white")
    plt.close(fig)


def chart_top_issues(stats):
    rows = stats["top_rules"][:5][::-1]
    labels = [f"{r[1][:48]}" for r in rows]
    values = [round(100 * r[5] / stats["n_repos"]) for r in rows]
    colors = [HIGHLIGHT if v == max(values) else BAR for v in values]
    fig, ax = plt.subplots(figsize=(8, 3.6), dpi=150)
    bars = ax.barh(labels, values, color=colors, height=0.58, zorder=3)
    ax.bar_label(bars, fmt="%.0f%%", padding=5, fontsize=10.5, fontweight="bold", color=INK)
    ax.grid(axis="x", color=GRID, zorder=0)
    ax.set_xlim(0, 100)
    ax.set_xlabel("% of repos affected", color=MUTED, fontsize=10)
    _style_axes(ax)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "top-issues.png", facecolor="white")
    plt.close(fig)


def chart_score_distribution(stats):
    buckets = {b: 0 for b in range(0, 100, 10)}
    buckets.update(dict(stats["distribution"]))
    labels = [f"{b}–{b + 10}" for b in buckets]
    values = list(buckets.values())
    colors = [HIGHLIGHT if v == max(values) else BAR for v in values]
    fig, ax = plt.subplots(figsize=(8, 4.0), dpi=150)
    bars = ax.bar(labels, values, color=colors, width=0.68, zorder=3)
    ax.bar_label(bars, fontsize=10, fontweight="bold", color=INK, padding=3)
    ax.grid(axis="y", color=GRID, zorder=0)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylabel("Repos", color=MUTED, fontsize=10)
    ax.set_xlabel("Production-Ready Score bucket", color=MUTED, fontsize=10)
    _style_axes(ax)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "score-distribution.png", facecolor="white")
    plt.close(fig)


# --------------------------------------------------------------------------- data exports

def export_data(conn, stats):
    area_ids = [r[0] for r in stats["by_area"]]
    rows = []
    for repo in _q(
        conn,
        "SELECT repo_ix, origin, framework, uses_supabase, language, loc, n_issues, score, tier "
        "FROM repos ORDER BY repo_ix",
    ):
        per_area = dict(_q(
            conn,
            "SELECT impact_area, COUNT(*) FROM issues WHERE repo_ix=? GROUP BY impact_area",
            (repo[0],),
        ))
        rows.append(list(repo) + [per_area.get(a, 0) for a in area_ids])

    header = [
        "repo_id", "origin", "framework", "uses_supabase", "language",
        "loc", "total_issues", "score", "tier",
    ] + [f"issues_{a}" for a in area_ids]

    with open(DATA_DIR / "vibe-code-2026.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    (DATA_DIR / "vibe-code-2026.json").write_text(
        json.dumps([dict(zip(header, r)) for r in rows], indent=1), encoding="utf-8"
    )

    agg = [("metric", "value")]
    agg += [
        ("repos_scanned", stats["n_repos"]),
        ("total_issues", stats["n_issues"]),
        ("total_loc", stats["total_loc"]),
        ("issues_per_kloc", stats["issues_per_kloc"]),
        ("avg_score", stats["avg_score"]),
        ("median_score", stats["median_score"]),
        ("pct_repos_with_leaked_secret", stats["pct_secret"]),
        ("supabase_repos", stats["n_supabase"]),
        ("pct_supabase_with_security_issue", stats["pct_supabase_insecure"]),
    ]
    agg += [(f"tier_{t.lower()}", n) for t, n in sorted(stats["tiers"].items())]
    agg += [(f"issues_{a}", n) for a, n, _ in stats["by_area"]]
    agg += [(f"issues_severity_{sev.lower()}", n) for sev, n in sorted(stats["by_severity"].items())]
    with open(DATA_DIR / "aggregate-stats.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(agg)


# --------------------------------------------------------------------------- readme

def _count_rules():
    catalog = json.loads(NORMALIZED_CATALOG.read_text(encoding="utf-8"))
    return len({r["rule_version_id"] for t in catalog["tools"].values() for r in t["rules"]})


def render_readme(stats):
    n_rules = _count_rules()
    top = stats["top_rules"]
    fw = stats["by_framework"]
    real_fw = [r for r in fw if r[0] in ("nextjs", "react-vite", "react", "vue", "svelte", "remix")]
    best_fw = FRAMEWORK_LABELS.get(real_fw[0][0], "-") if real_fw else "-"
    worst_fw = FRAMEWORK_LABELS.get(real_fw[-1][0], "-") if real_fw else "-"
    today = date.today().strftime("%B %Y")

    area_rows = "\n".join(
        f"| {a.capitalize()} | {n:,} | {nr} |" for a, n, nr in stats["by_area"]
    )
    top_rows = "\n".join(
        f"| {name} | {area} | {sev} | {n_issues:,} | {round(100 * n_repos / stats['n_repos'])}% |"
        for _, name, area, sev, n_issues, n_repos in top
    )
    fw_rows = "\n".join(
        f"| {FRAMEWORK_LABELS.get(f, f)} | {n} | **{int(score)}** | {per_kloc} |"
        for f, n, score, per_kloc in fw
    )
    origin_rows = "\n".join(
        f"| {ORIGIN_LABELS.get(o, o)} | {n} | {int(score) if score is not None else '-'} | {median} | {per_kloc} |"
        for o, n, score, median, per_kloc in stats["by_origin"]
    )

    readme = f"""# The State of AI-Generated Code, 2026

![dataset](https://img.shields.io/badge/dataset-CC--BY--4.0-007ec6)
![scans](https://img.shields.io/badge/scans-{stats['n_repos']}_repos-320537)
![updated](https://img.shields.io/badge/updated-{today.replace(' ', '_')}-8250df)
![engine](https://img.shields.io/badge/engine-Quality_Clouds_Hub-C800D7)

Published {today} by [Quality Clouds Hub](https://qualityclouds.com) · Data available under CC-BY-4.0

> **{stats['pct_secret']}% of AI-generated projects ship with a leaked secret or hardcoded credential.
> {stats['pct_supabase_insecure']}% of Supabase-backed apps have at least one client-side security
> misconfiguration. The average Production-Ready Score is {stats['avg_score']} out of 100.**

## Key findings

- We scanned **{stats['n_repos']} public projects** built with Lovable, Bolt, v0, and AI-copilot-tagged
  GitHub repos — **{stats['total_loc']:,} lines of code** in total.
- The scans produced **{stats['n_issues']:,} issues** ({stats['issues_per_kloc']} per 1,000 lines of code).
- The average **Production-Ready Score is {stats['avg_score']} / 100** (median {stats['median_score']}).
- **{stats['pct_secret']}%** of projects shipped at least one leaked secret or hardcoded credential.
- **{stats['pct_supabase_insecure']}%** of the {stats['n_supabase']} Supabase-backed projects had at least
  one client-side security misconfiguration (exposed service-role keys, client-side auth logic,
  public buckets…).
- **{best_fw}** projects scored highest on average; **{worst_fw}** lowest.
- **{round(100 * stats['tiers'].get('NOT_READY', 0) / stats['n_repos'])}%** of projects are
  **NOT production-ready** under the Hub's certification bar — not for a low overall score, but
  because at least one impact area collapses below the hard-fail threshold.
  {round(100 * stats['tiers'].get('GOLD', 0) / stats['n_repos'])}% reach GOLD.

## Issues by impact area

| Impact area | Issues | Repos affected |
|---|---|---|
{area_rows}

## Top 10 most frequent findings

| Rule | Area | Severity | Issues | % repos |
|---|---|---|---|---|
{top_rows}

## Score by frontend framework

| Framework | Repos | Avg score | Issues / KLOC |
|---|---|---|---|
{fw_rows}

## By generation platform

| Origin | Repos | Avg score | Median issues | Issues / KLOC |
|---|---|---|---|---|
{origin_rows}

## Charts

![Score by framework](charts/score-by-framework.png)
![Top issues](charts/top-issues.png)
![Score distribution](charts/score-distribution.png)

## Methodology

Projects were sampled from public GitHub repositories carrying unambiguous markers of the
generation platform (Lovable/v0/Bolt README templates, AI topics), filtered by size and recency,
capped at 2 repos per owner. Each was scanned with the **same deterministic rule engine and the
same {n_rules} production rules** (Semgrep + regex) that power the Quality Clouds Hub scanner,
and scored with the Hub's
production-readiness formula. **Individual repositories are never named — only aggregate
statistics are published.** Full details in [docs/methodology.md](docs/methodology.md) and
[docs/ruleset.md](docs/ruleset.md).

## Downloads

| File | Contents |
|---|---|
| [data/vibe-code-2026.csv](data/vibe-code-2026.csv) | Per-repo metrics (anonymized), one row per project |
| [data/vibe-code-2026.json](data/vibe-code-2026.json) | Same as above, JSON |
| [data/aggregate-stats.csv](data/aggregate-stats.csv) | Headline aggregate statistics |

## Reproduce

Scan your own repository with the same ruleset at [qualityclouds.com](https://qualityclouds.com) —
import your repo and get a Production-Ready Score in minutes.

## License

**Data:** CC-BY-4.0 — reuse with attribution · **Pipeline code:** MIT
"""
    (PROJECT_ROOT / "README.md").write_text(readme, encoding="utf-8")


def render_docs(stats):
    catalog = json.loads(NORMALIZED_CATALOG.read_text(encoding="utf-8"))
    seen, lines = set(), []
    for tid, tool in sorted(catalog["tools"].items()):
        for r in tool["rules"]:
            if r["rule_version_id"] in seen:
                continue
            seen.add(r["rule_version_id"])
            kind = "semgrep" if "semgrep" in r else "regex"
            lines.append(
                f"| {r['base_rule_id']} | {r['rule_name']} | {r['impact_area']} | "
                f"{r['severity']} | {kind} | {tid.replace('-quality-hub-agent', '')} |"
            )
    ruleset = (
        "# Ruleset\n\nAll rules are the production catalog of Quality Clouds Hub "
        f"(global, active, deterministic — Semgrep or regex). Total: {len(seen)} rules.\n\n"
        "| Rule | Name | Impact area | Severity | Engine | Tool |\n|---|---|---|---|---|---|\n"
        + "\n".join(lines) + "\n"
    )
    (DOCS_DIR / "ruleset.md").write_text(ruleset, encoding="utf-8")

    repairs = json.loads(NORMALIZED_CATALOG.read_text(encoding="utf-8")).get("payload_repairs", {})
    repairs_list = ", ".join(sorted(r.replace("-1.0", "") for r in repairs))
    methodology = f"""# Methodology

## Sample selection

- **Sources:** GitHub repository search for unambiguous platform markers:
  Lovable ("Welcome to your Lovable project" README), v0 (auto-sync README), Bolt
  (bolt.new README references), and repos tagged `ai-generated` / `vibe-coding`.
- **Filters:** no forks, 150 KB – 100 MB, pushed after 2026-01-01, primary language in
  TypeScript / JavaScript / Python / PHP (the technologies the scanner generates issues for),
  max 2 repos per owner, >=100 lines of scannable code.
- **Sample:** {stats['n_repos']} repositories scanned successfully.

## Scanning

- Shallow clone of the default branch; scanned with the **production rule engine of Quality
  Clouds Hub** (Semgrep 1.136.0 + regex runner) and its production rule catalog (deterministic
  rules only — LLM-agent rules, prompt-quality analysis and linter passthrough are out of scope).
- Tool applicability per repo mirrors the Hub's stack autodiscovery (language/framework detection).
- Lockfiles and generated artifacts (package-lock.json, *.min.js, source maps…) are excluded.
- 12 rules whose stored pattern was syntactically corrupted at source were repaired before
  scanning (YAML indentation/quoting fixes; one pattern reconstructed to its evident intent):
  {repairs_list}. Two taint-mode Semgrep rules (rct-open-redirect, rct-unvalidated-url-params)
  were additionally enabled.

## Scoring

Scores replicate the Hub's production-readiness formula (rule-health policy):
per impact area, every evaluated rule scores 100 if it produced no findings, 50 if it is a
MEDIUM-severity rule with findings, 0 if HIGH (LOW-severity rules never subtract). The area
score is the average over evaluated rules; the overall score is the weighted average across
areas (security 30, performance 20, scalability 20, manageability 15, maintainability 10).
Tiers: GOLD >= 90, CERTIFIED >= 75, CONDITIONAL >= 60, NOT_READY otherwise; any area below 60
is a hard fail (NOT_READY).

## Privacy

Individual repositories are never named. Published data contains only sequential ids,
platform of origin, framework, size, and aggregate counts. See [privacy.md](privacy.md).
"""
    (DOCS_DIR / "methodology.md").write_text(methodology, encoding="utf-8")

    privacy = """# Privacy

- The study only scans **public** repositories.
- No repository names, URLs, owner identities, file paths, or code snippets are published.
- The published datasets contain sequential anonymous ids and aggregate metrics only.
- Findings that could identify a specific repository (e.g. unique secrets) are never included
  in the published data; leaked credentials found during the study were not collected, stored,
  or verified.
"""
    (DOCS_DIR / "privacy.md").write_text(privacy, encoding="utf-8")


def main():
    for d in (CHARTS_DIR, DATA_DIR, DOCS_DIR):
        d.mkdir(exist_ok=True)
    conn = sqlite3.connect(ISSUES_DB)
    stats = gather_stats(conn)
    chart_score_by_framework(stats)
    chart_top_issues(stats)
    chart_score_distribution(stats)
    export_data(conn, stats)
    render_readme(stats)
    render_docs(stats)
    conn.close()
    print(f"[report] README.md + 3 charts + data exports written for {stats['n_repos']} repos")


if __name__ == "__main__":
    main()
