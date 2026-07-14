"""Aggregate scan results into SQLite and compute per-repo Production-Ready Scores.

Replicates the Hub's scoring exactly (ADR-019, rule-health policy):
- per impact area: clean rules = 100 pts, MEDIUM failing = 50, HIGH failing = 0,
  LOW failing counts as clean; area_score = avg over rules_in_area.
- overall = weight-averaged area scores (areas with no rules are unscored).
- tiers: GOLD>=90, CERTIFIED>=75, CONDITIONAL>=60, else NOT_READY;
  any area < 60 => hard fail => NOT_READY.
"""

import json
import sqlite3
from collections import defaultdict

from config import ISSUES_DB, NORMALIZED_CATALOG, REPOS_STATE, RESULTS_DIR
from scan import _is_generated_file

AREA_WEIGHTS = {
    "security": 30,
    "performance": 20,
    "scalability": 20,
    "manageability": 15,
    "maintainability": 10,
    "architecture": 5,
}

TIER_GOLD, TIER_CERTIFIED, TIER_CONDITIONAL, HARD_FAIL = 90, 75, 60, 60

# The Hub only generates issues for these technologies; repos whose primary
# language is anything else are out of scope for the study.
STUDY_LANGUAGES = {"Python", "PHP", "JavaScript", "TypeScript"}


def _rules_by_area(catalog, tool_ids):
    """Distinct evaluated rules per impact area with severity (mirrors _gather_rules)."""
    rules = {}
    for tid in tool_ids:
        for rule in catalog["tools"].get(tid, {}).get("rules", []):
            rules[rule["rule_version_id"]] = (rule["impact_area"], rule["severity"])
    by_area = defaultdict(dict)
    for rid, (area, severity) in rules.items():
        by_area[area][rid] = severity
    return by_area


def compute_score(catalog, tools_run, issues):
    """Return (overall, tier, {area: area_score})."""
    by_area = _rules_by_area(catalog, tools_run)
    failing = defaultdict(set)
    for issue in issues:
        failing[issue.get("impact_area")].add(issue.get("rule_id"))

    area_scores = {}
    for area, rules in by_area.items():
        if not rules:
            continue
        num_high = sum(1 for rid, sev in rules.items() if rid in failing[area] and sev == "HIGH")
        num_medium = sum(1 for rid, sev in rules.items() if rid in failing[area] and sev == "MEDIUM")
        clean = len(rules) - num_high - num_medium
        area_scores[area] = max(0, min(100, round((clean * 100 + num_medium * 50) / len(rules))))

    measured = {a: s for a, s in area_scores.items() if a in AREA_WEIGHTS}
    if not measured:
        return None, "UNSCORED", area_scores
    total_w = sum(AREA_WEIGHTS[a] for a in measured)
    overall = round(sum(s * AREA_WEIGHTS[a] for a, s in measured.items()) / total_w)

    if any(s < HARD_FAIL for s in measured.values()):
        tier = "NOT_READY"
    elif overall >= TIER_GOLD:
        tier = "GOLD"
    elif overall >= TIER_CERTIFIED:
        tier = "CERTIFIED"
    elif overall >= TIER_CONDITIONAL:
        tier = "CONDITIONAL"
    else:
        tier = "NOT_READY"
    return overall, tier, area_scores


def _create_schema(conn):
    conn.executescript(
        """
        DROP TABLE IF EXISTS repos;
        DROP TABLE IF EXISTS issues;
        CREATE TABLE repos (
            repo_ix INTEGER PRIMARY KEY,
            slug TEXT UNIQUE,
            origin TEXT,
            framework TEXT,
            uses_supabase INTEGER,
            language TEXT,
            stars INTEGER,
            loc INTEGER,
            n_issues INTEGER,
            score INTEGER,
            tier TEXT,
            tools_run TEXT,
            area_scores TEXT
        );
        CREATE TABLE issues (
            repo_ix INTEGER,
            rule_id TEXT,
            base_rule_id TEXT,
            rule_name TEXT,
            impact_area TEXT,
            severity TEXT,
            file TEXT,
            line INTEGER
        );
        CREATE INDEX ix_issues_repo ON issues(repo_ix);
        CREATE INDEX ix_issues_rule ON issues(rule_id);
        """
    )


def collect():
    catalog = json.loads(NORMALIZED_CATALOG.read_text(encoding="utf-8"))
    state = {r["slug"]: r for r in json.loads(REPOS_STATE.read_text(encoding="utf-8"))}
    conn = sqlite3.connect(ISSUES_DB)
    _create_schema(conn)

    repo_ix = 0
    for path in sorted(RESULTS_DIR.glob("*.json")):
        result = json.loads(path.read_text(encoding="utf-8"))
        meta = state.get(result["repo"], {})
        if meta.get("language") not in STUDY_LANGUAGES:
            continue
        loc = sum(result["loc_by_extension"].values())
        if loc < 100:  # skip near-empty repos (template-only / broken)
            continue
        repo_ix += 1
        # re-apply generated-file exclusion (older scans predate bun.lock/deno.lock)
        result["issues"] = [i for i in result["issues"] if not _is_generated_file(i.get("file"))]
        overall, tier, area_scores = compute_score(catalog, result["tools_run"], result["issues"])
        conn.execute(
            "INSERT INTO repos VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                repo_ix, result["repo"], meta.get("origin"),
                result["stack"]["framework"], int(result["stack"]["uses_supabase"]),
                meta.get("language"), meta.get("stars", 0), loc,
                len(result["issues"]), overall, tier,
                json.dumps(result["tools_run"]), json.dumps(area_scores),
            ),
        )
        conn.executemany(
            "INSERT INTO issues VALUES (?,?,?,?,?,?,?,?)",
            [
                (
                    repo_ix, i.get("rule_id"), i.get("base_rule_id"), i.get("rule_name"),
                    i.get("impact_area"), i.get("severity"), i.get("file"), i.get("line"),
                )
                for i in result["issues"]
            ],
        )

    conn.commit()
    n_issues = conn.execute("SELECT COUNT(*) FROM issues").fetchone()[0]
    print(f"[collect] repos={repo_ix} issues={n_issues} -> {ISSUES_DB.name}")
    for row in conn.execute(
        "SELECT origin, COUNT(*), ROUND(AVG(score),1), ROUND(AVG(n_issues),1) FROM repos GROUP BY origin"
    ):
        print(f"  {row[0]:<12} repos={row[1]:>4} avg_score={row[2]} avg_issues={row[3]}")
    conn.close()


if __name__ == "__main__":
    collect()
