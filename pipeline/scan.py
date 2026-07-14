"""Scan one repo clone with the production ruleset using the tools-repo engine.

Usage: python scan.py <repo_dir> <repo_slug>

Writes results/<repo_slug>.json with issues + stats. Imports the real engine
modules from the local tools repo for full fidelity with production:
SemgrepRuleBuilder/SemgrepLauncher/SemgrepResultMapper + regex runner.
"""

import json
import os
import sys
import time
from pathlib import Path

from config import NORMALIZED_CATALOG, RESULTS_DIR, TOOLS_REPO

sys.path.insert(0, str(TOOLS_REPO))
os.environ.setdefault("SEMGREP_DEBUG_MAX_LIST_FILES", "0")

from regex_tools_api.src.domain.services.semgrep_result_mapper import SemgrepResultMapper  # noqa: E402
from regex_tools_api.src.infrastructure.external_tools.regex_tool_launcher import (  # noqa: E402
    run_regex_with_rules,
)
from regex_tools_api.src.infrastructure.external_tools.semgrep_launcher import SemgrepLauncher  # noqa: E402
from regex_tools_api.src.infrastructure.external_tools.semgrep_rule_builder import (  # noqa: E402
    SemgrepRuleBuilder,
)

from stack_detect import count_loc, detect_origin_stack, detect_tools  # noqa: E402


class StudyRuleBuilder(SemgrepRuleBuilder):
    """Extends the prod builder to also accept taint-mode rules.

    Prod's _has_pattern_field drops `mode: taint` rules (they carry
    pattern-sources/pattern-sinks instead of pattern/patterns); documented
    deviation so those two React security rules run in this study.
    """

    @staticmethod
    def _has_pattern_field(entry):
        if entry.get("mode") == "taint" and entry.get("pattern-sources") and entry.get("pattern-sinks"):
            return True
        return SemgrepRuleBuilder._has_pattern_field(entry)


def _load_catalog():
    return json.loads(NORMALIZED_CATALOG.read_text(encoding="utf-8"))


def _gather_rules(catalog, tool_ids):
    """Dedup rules across the applicable tools; remember rule -> tools mapping.

    rule_meta is keyed by rule_version_id AND by the semgrep payload's embedded
    id (semgrep reports check_id from the YAML, which may lack the version suffix).
    """
    semgrep_rules, regex_rules, rule_meta = {}, {}, {}
    for tid in tool_ids:
        for rule in catalog["tools"][tid]["rules"]:
            rid = rule["rule_version_id"]
            meta = rule_meta.setdefault(
                rid,
                {
                    "rule_version_id": rid,
                    "impact_area": rule["impact_area"],
                    "severity": rule["severity"],
                    "base_rule_id": rule["base_rule_id"],
                    "rule_name": rule["rule_name"],
                    "tools": [],
                },
            )
            if tid not in meta["tools"]:
                meta["tools"].append(tid)
            if rule.get("payload_rule_id"):
                rule_meta.setdefault(rule["payload_rule_id"], meta)
            if "semgrep" in rule:
                semgrep_rules[rid] = rule
            elif "regex" in rule:
                regex_rules[rid] = rule
    return list(semgrep_rules.values()), list(regex_rules.values()), rule_meta


def _run_engine(repo_dir, semgrep_rules, regex_rules):
    issues = []
    if semgrep_rules:
        launcher = SemgrepLauncher(StudyRuleBuilder(), SemgrepResultMapper())
        sg_issues, _ = launcher.run_semgrep_with_rules(str(repo_dir), semgrep_rules)
        issues.extend(sg_issues)
    if regex_rules:
        rx_issues, _ = run_regex_with_rules(str(repo_dir), regex_rules)
        issues.extend(rx_issues)
    return issues


# Lockfiles / generated artifacts: the raw engine has no notion of them and
# some prod rules ship without file scoping (e.g. node-wildcard-dependency),
# flooding results with lockfile matches. Study-level exclusion, documented
# in methodology.
GENERATED_BASENAMES = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb", "bun.lock",
    "deno.lock", "composer.lock", "poetry.lock", "pipfile.lock", "uv.lock",
}
GENERATED_SUFFIXES = (".min.js", ".min.css", ".map", ".snap", ".bundle.js")


def _is_generated_file(file_path):
    name = Path(file_path or "").name.lower()
    return name in GENERATED_BASENAMES or name.endswith(GENERATED_SUFFIXES)


def _resolve_meta(check_id, rule_meta):
    """Match a semgrep check_id to catalog meta.

    Semgrep prefixes check_id with the temp-config path (dot-joined), and
    versioned ids contain dots ("-1.0"), so exact + dotted-suffix match.
    """
    if not check_id:
        return {}
    meta = rule_meta.get(check_id)
    if meta:
        return meta
    for key, m in rule_meta.items():
        if check_id.endswith("." + key):
            return m
    return {}


def _enrich_and_dedup(issues, rule_meta):
    seen, out, unmatched = set(), [], set()
    for issue in issues:
        if _is_generated_file(issue.get("file")):
            continue
        meta = _resolve_meta(issue.get("rule_id"), rule_meta)
        if not meta:
            unmatched.add(issue.get("rule_id"))
        issue["rule_id"] = meta.get("rule_version_id") or issue.get("rule_id")
        key = (issue["rule_id"], issue.get("file"), issue.get("line"))
        if key in seen:
            continue
        seen.add(key)
        issue["impact_area"] = meta.get("impact_area")
        issue["severity"] = (meta.get("severity") or issue.get("severity", "")).upper()
        issue["base_rule_id"] = meta.get("base_rule_id")
        issue["rule_name"] = meta.get("rule_name")
        issue["tools"] = meta.get("tools", [])
        out.append(issue)
    if unmatched:
        print(f"[scan] WARNING: {len(unmatched)} check_ids without catalog match: {sorted(unmatched)[:10]}")
    return out


def scan_repo(repo_dir: Path, repo_slug: str) -> dict:
    catalog = _load_catalog()
    started = time.time()
    tool_ids = detect_tools(repo_dir)
    semgrep_rules, regex_rules, rule_meta = _gather_rules(catalog, tool_ids)

    issues = _run_engine(repo_dir, semgrep_rules, regex_rules)
    issues = _enrich_and_dedup(issues, rule_meta)

    all_exts = {
        e.lstrip(".").lower()
        for r in [*semgrep_rules, *regex_rules]
        for e in r["file_extensions"]
    }
    result = {
        "repo": repo_slug,
        "tools_run": tool_ids,
        "rules_evaluated": len(semgrep_rules) + len(regex_rules),
        "stack": detect_origin_stack(repo_dir),
        "loc_by_extension": count_loc(repo_dir, all_exts),
        "duration_seconds": round(time.time() - started, 1),
        "issues": issues,
    }
    RESULTS_DIR.mkdir(exist_ok=True)
    out_path = RESULTS_DIR / f"{repo_slug}.json"
    out_path.write_text(json.dumps(result, indent=1, ensure_ascii=False), encoding="utf-8")
    return result


def main():
    repo_dir, repo_slug = Path(sys.argv[1]), sys.argv[2]
    result = scan_repo(repo_dir, repo_slug)
    print(
        f"\n[scan] {repo_slug}: tools={result['tools_run']} "
        f"rules={result['rules_evaluated']} issues={len(result['issues'])} "
        f"in {result['duration_seconds']}s"
    )


if __name__ == "__main__":
    main()
