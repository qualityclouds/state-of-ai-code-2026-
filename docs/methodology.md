# Methodology

## Sample selection

- **Sources:** GitHub repository search for unambiguous platform markers:
  Lovable ("Welcome to your Lovable project" README), v0 (auto-sync README), Bolt
  (bolt.new README references), and repos tagged `ai-generated` / `vibe-coding`.
- **Filters:** no forks, 150 KB – 100 MB, pushed after 2026-01-01, primary language in
  TypeScript / JavaScript / Python / PHP (the technologies the scanner generates issues for),
  max 2 repos per owner, >=100 lines of scannable code.
- **Sample:** 429 repositories scanned successfully.

## Scanning

- Shallow clone of the default branch; scanned with the **production rule engine of Quality
  Clouds Hub** (Semgrep 1.136.0 + regex runner) and its production rule catalog (deterministic
  rules only — LLM-agent rules, prompt-quality analysis and linter passthrough are out of scope).
- Tool applicability per repo mirrors the Hub's stack autodiscovery (language/framework detection).
- Lockfiles and generated artifacts (package-lock.json, *.min.js, source maps…) are excluded.
- 12 rules whose stored pattern was syntactically corrupted at source were repaired before
  scanning (YAML indentation/quoting fixes; one pattern reconstructed to its evident intent):
  js-nested-ternary, php-sec-insecure-cookie-attributes-missing-httponly-or-secure-flags, rct-mixed-concerns, sb-auth-reversed-logic, sb-storage-public-bucket, sb-supabase-admin-client, ts-api-key-in-client, ts-hardcoded-bearer-token, ts-private-key-in-code, vite-missing-referrer-policy, vite-missing-sri, vite-production-url-in-code. Two taint-mode Semgrep rules (rct-open-redirect, rct-unvalidated-url-params)
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
