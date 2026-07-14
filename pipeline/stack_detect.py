"""Lightweight autodiscovery: decide which catalog tools apply to a repo clone.

Mirrors the spirit of prod autodiscovery (stack targets) with cheap local
heuristics: file extensions present + dependency manifests.
"""

import json
from pathlib import Path

IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "dist", "build", ".pytest_cache", ".mypy_cache", "vendor", ".qh_deps",
}


def _walk_files(repo_dir: Path):
    for path in repo_dir.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def _collect_signals(repo_dir: Path):
    extensions = set()
    package_json_text = ""
    python_manifest_text = ""
    composer_text = ""
    for path in _walk_files(repo_dir):
        extensions.add(path.suffix.lower().lstrip("."))
        name = path.name.lower()
        try:
            if name == "package.json":
                package_json_text += path.read_text(encoding="utf-8", errors="ignore")
            elif name in ("requirements.txt", "pyproject.toml", "pipfile", "setup.py"):
                python_manifest_text += path.read_text(encoding="utf-8", errors="ignore")
            elif name == "composer.json":
                composer_text += path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            pass
    return extensions, package_json_text.lower(), python_manifest_text.lower(), composer_text.lower()


def _grep_any(repo_dir: Path, suffixes, needles, max_files=400):
    checked = 0
    for path in _walk_files(repo_dir):
        if path.suffix.lower() not in suffixes:
            continue
        checked += 1
        if checked > max_files:
            return False
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if any(n in text for n in needles):
            return True
    return False


def detect_tools(repo_dir: Path) -> list:
    """Return the catalog tool_ids that apply to this repo clone."""
    exts, pkg, pymanifest, composer = _collect_signals(repo_dir)
    has_py = "py" in exts
    tools = []

    if has_py:
        tools.append("python-quality-hub-agent")
        if "fastapi" in pymanifest or _grep_any(repo_dir, {".py"}, ("from fastapi", "import fastapi")):
            tools.append("fastapi-quality-hub-agent")
        if "sqlalchemy" in pymanifest or _grep_any(repo_dir, {".py"}, ("import sqlalchemy", "from sqlalchemy")):
            tools.append("sqlalchemy-quality-hub-agent")

    if exts & {"js", "jsx", "mjs", "cjs"}:
        tools.append("javascript-quality-hub-agent")
    if exts & {"ts", "tsx"}:
        tools.append("typescript-quality-hub-agent")
    if '"react"' in pkg or exts & {"jsx", "tsx"}:
        tools.append("react-quality-hub-agent")
    if '"vite"' in pkg or any((repo_dir / f"vite.config.{e}").exists() for e in ("js", "ts", "mjs", "mts")):
        tools.append("vite-quality-hub-agent")
    if pkg:
        tools.append("nodejs-quality-hub-agent")
    if "@supabase/" in pkg or (repo_dir / "supabase").is_dir():
        tools.append("supabase-quality-hub-agent")

    if "php" in exts:
        tools.append("php-quality-hub-agent")
        if "magento" in composer:
            tools.append("regex-tool-adobe-magento")

    return tools


def count_loc(repo_dir: Path, extensions) -> dict:
    """Count non-empty lines per extension for the given extension set."""
    loc = {}
    for path in _walk_files(repo_dir):
        ext = path.suffix.lower().lstrip(".")
        if ext not in extensions:
            continue
        try:
            lines = sum(
                1 for ln in path.read_text(encoding="utf-8", errors="ignore").splitlines() if ln.strip()
            )
        except OSError:
            continue
        loc[ext] = loc.get(ext, 0) + lines
    return loc


def detect_origin_stack(repo_dir: Path) -> dict:
    """Extra report metadata: frontend framework flavor for segmentation."""
    _, pkg, _, _ = _collect_signals(repo_dir)
    framework = "other"
    if '"next"' in pkg:
        framework = "nextjs"
    elif '"@remix-run/' in pkg:
        framework = "remix"
    elif '"vite"' in pkg and '"react"' in pkg:
        framework = "react-vite"
    elif '"react"' in pkg:
        framework = "react"
    elif '"vue"' in pkg:
        framework = "vue"
    elif '"svelte"' in pkg:
        framework = "svelte"
    elif pkg:
        framework = "node-other"
    return {"framework": framework, "uses_supabase": "@supabase/" in pkg}


if __name__ == "__main__":
    import sys

    repo = Path(sys.argv[1])
    print(json.dumps({"tools": detect_tools(repo), **detect_origin_stack(repo)}, indent=2))
