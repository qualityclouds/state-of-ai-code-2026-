"""Shared paths and constants for the vibe-code-report pipeline."""

from pathlib import Path

import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# Local checkout of the Quality Clouds Hub "tools" engine repo (not public);
# the scan pipeline imports its rule-engine modules directly for prod fidelity.
TOOLS_REPO = Path(os.environ.get("QH_TOOLS_REPO", PROJECT_ROOT.parent / "tools"))

CATALOG_DIR = PROJECT_ROOT / "catalog"
CLONES_DIR = PROJECT_ROOT / "clones"
RESULTS_DIR = PROJECT_ROOT / "results"
DATA_DIR = PROJECT_ROOT / "data"
CHARTS_DIR = PROJECT_ROOT / "charts"
DOCS_DIR = PROJECT_ROOT / "docs"

RAW_EXPORT = CATALOG_DIR / "raw_export.json"
NORMALIZED_CATALOG = CATALOG_DIR / "normalized_catalog.json"
REPOS_STATE = PROJECT_ROOT / "repos.json"
ISSUES_DB = PROJECT_ROOT / "issues.sqlite"

BRAND_AUBERGINE = "#320537"
BRAND_RASPBERRY = "#C800D7"
