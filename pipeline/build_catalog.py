"""Normalize the production catalog export into per-tool rule lists.

Input: catalog/raw_export.json (the JSON produced by the read-only prod query).
Output: catalog/normalized_catalog.json with shape:

    {
      "tools": {tool_id: {...tool row, "target": {...}, "rules": [normalized_rule]}},
      "severities": [...], "impact_areas": [...]
    }

Each normalized rule uses the exact keys the tools-repo engine consumes
(SemgrepRuleBuilder / regex runner): rule_version_id, rule_name, severity,
semgrep | regex, file_extensions, files_whitelist_patterns, ce_types.
Report-only metadata (impact_area, description, base rule_id) rides along.
"""

import json
import re
from collections import defaultdict

import yaml

from config import CATALOG_DIR, NORMALIZED_CATALOG, RAW_EXPORT

PAYLOAD_OVERRIDES = CATALOG_DIR / "payload_overrides.json"

# Same heuristic as tools' SemgrepRuleBuilder._is_complete_yaml
_COMPLETE_YAML_KEYS = ("pattern:", "patterns:", "pattern-either:")


def _is_complete_yaml(body):
    stripped = body.strip()
    return stripped.startswith("rules:") or any(k in stripped for k in _COMPLETE_YAML_KEYS)


def _try_parse(body):
    try:
        parsed = yaml.safe_load(body)
        return parsed if isinstance(parsed, dict) else None
    except yaml.YAMLError:
        return None


def _fix_first_line_indent(body):
    """Re-indent the first line: prod payloads often lost its leading spaces."""
    lines = body.split("\n")
    first = next((i for i, ln in enumerate(lines) if ln.strip()), None)
    if first is None:
        return None
    for k in (4, 2, 6, 8):
        cand = lines[:]
        cand[first] = " " * k + cand[first].lstrip()
        fixed = "\n".join(cand)
        if _try_parse(fixed):
            return fixed
    return None


def _fix_unquoted_scalars(body):
    """Single-quote pattern values containing ': ' or ' ? ' that break YAML."""
    out = []
    for ln in body.split("\n"):
        m = re.match(r"^(\s*-?\s*)(pattern-not|pattern|pattern-inside|pattern-not-inside):\s+(.*\S)\s*$", ln)
        if m and (": " in m.group(3) or " ? " in m.group(3)) and not m.group(3).startswith(("|", ">", "'", '"')):
            ln = f"{m.group(1)}{m.group(2)}: '" + m.group(3).replace("'", "''") + "'"
        out.append(ln)
    return "\n".join(out)


def _repair_semgrep_payload(rule_version_id, body, overrides):
    """Return (payload, repair_method). Repairs YAML broken at source in prod."""
    if rule_version_id in overrides:
        return overrides[rule_version_id], "manual_override"
    normalized = body.replace("\r\n", "\n").replace("\r", "\n")
    if not _is_complete_yaml(normalized) or _try_parse(normalized):
        return body, None
    for method, candidate in (
        ("reindent", _fix_first_line_indent(normalized)),
        ("quote_scalars", _fix_unquoted_scalars(normalized)),
        ("reindent+quote", _fix_first_line_indent(_fix_unquoted_scalars(normalized))),
    ):
        if candidate and _try_parse(candidate):
            return candidate, method
    return body, "UNREPAIRED"


def _payload_rule_id(body):
    """Embedded semgrep rule id, used by scan.py to map check_id back to the rule."""
    parsed = _try_parse(body.replace("\r\n", "\n")) if _is_complete_yaml(body) else None
    if not parsed:
        return None
    entry = (parsed.get("rules") or [parsed])[0]
    return entry.get("id") if isinstance(entry, dict) else None


def _index_rule_satellites(cat):
    semgrep = {r["rule_version_id"]: r["semgrep"] for r in cat["semgrep_rules"]}
    regex = {r["rule_version_id"]: r["regex"] for r in cat["regex_rules"]}
    extensions = defaultdict(list)
    for row in cat["rules_file_extensions"]:
        extensions[row["rule_id"]].append(row["extension"])
    whitelist = defaultdict(list)
    for row in cat.get("rules_file_whitelist") or []:
        whitelist[row["rule_id"]].append(row["path_pattern"])
    return semgrep, regex, extensions, whitelist


def _normalize_rule(rule, semgrep, regex, extensions, whitelist):
    rid = rule["id"]
    normalized = {
        "rule_version_id": rid,
        "rule_name": rule["name"],
        "severity": rule["severity"],
        "file_extensions": sorted(extensions.get(rid, [])),
        "files_whitelist_patterns": whitelist.get(rid, []),
        "ce_types": [],
        # report-only metadata
        "impact_area": rule["impact_area"],
        "base_rule_id": rule["rule_id"],
        "description": rule["description"],
    }
    if rid in semgrep:
        normalized["semgrep"] = semgrep[rid]
        alias = _payload_rule_id(semgrep[rid])
        if alias and alias != rid:
            normalized["payload_rule_id"] = alias
    if rid in regex:
        normalized["regex"] = regex[rid]
    return normalized


def _rules_by_tool(cat, normalized_rules):
    ruleset_to_tool = {r["ruleset_version_id"]: r["tool_id"] for r in cat["ruleset_tools"]}
    by_tool = defaultdict(dict)  # tool_id -> {rule_version_id: rule} (dedup)
    for link in cat["rules_ruleset_versions"]:
        tool_id = ruleset_to_tool.get(link["ruleset_version_id"])
        rule = normalized_rules.get(link["rule_version_id"])
        if tool_id and rule:
            by_tool[tool_id][rule["rule_version_id"]] = rule
    return {t: sorted(rules.values(), key=lambda r: r["rule_version_id"]) for t, rules in by_tool.items()}


def build():
    cat = json.loads(RAW_EXPORT.read_text(encoding="utf-8"))
    overrides = json.loads(PAYLOAD_OVERRIDES.read_text(encoding="utf-8"))
    overrides.pop("_comment", None)
    semgrep, regex, extensions, whitelist = _index_rule_satellites(cat)

    repairs = {}
    for rid in list(semgrep):
        semgrep[rid], method = _repair_semgrep_payload(rid, semgrep[rid], overrides)
        if method:
            repairs[rid] = method
    normalized_rules = {
        r["id"]: _normalize_rule(r, semgrep, regex, extensions, whitelist)
        for r in cat["rules"]
    }
    by_tool = _rules_by_tool(cat, normalized_rules)
    targets = {t["tool_id"]: t for t in cat["tool_targets"]}

    tools = {}
    for tool in cat["tools"]:
        tid = tool["id"]
        tools[tid] = {**tool, "target": targets.get(tid), "rules": by_tool.get(tid, [])}

    out = {
        "tools": tools,
        "severities": cat["severities"],
        "impact_areas": cat["impact_areas"],
        "payload_repairs": repairs,
    }
    NORMALIZED_CATALOG.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")

    print(f"payload repairs ({len(repairs)}):")
    for rid, method in sorted(repairs.items()):
        print(f"  {rid}: {method}")
    print(f"\n{'tool':<32} {'rules':>5} {'semgrep':>8} {'regex':>6}  target")
    for tid, t in sorted(tools.items()):
        rules = t["rules"]
        n_sg = sum(1 for r in rules if "semgrep" in r)
        n_rx = sum(1 for r in rules if "regex" in r)
        target = (t["target"] or {}).get("target_key", "-")
        print(f"{tid:<32} {len(rules):>5} {n_sg:>8} {n_rx:>6}  {target}")


if __name__ == "__main__":
    build()
