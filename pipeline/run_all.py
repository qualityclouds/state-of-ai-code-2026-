"""Clone + scan every candidate in repos.json. Resumable; state saved per repo.

Usage: python run_all.py [--limit N]
Clones are deleted after a successful scan (results JSON keeps everything).
"""

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
import time
import traceback

from config import CLONES_DIR, REPOS_STATE, RESULTS_DIR
from scan import scan_repo

CLONE_TIMEOUT = 180


def _load_state():
    return json.loads(REPOS_STATE.read_text(encoding="utf-8"))


def _save_state(repos):
    REPOS_STATE.write_text(json.dumps(repos, indent=1), encoding="utf-8")


def _rmtree(path):
    def _on_error(func, p, _exc):
        try:
            import os

            os.chmod(p, stat.S_IWRITE)
            func(p)
        except OSError:
            pass

    shutil.rmtree(path, onerror=_on_error)


def _clone(repo):
    dest = CLONES_DIR / repo["slug"]
    if dest.exists():
        _rmtree(dest)  # leftover partial clone from a killed run
    cmd = [
        "git", "clone", "--depth", "1", "--quiet",
        "-c", "core.longpaths=true",
        "-c", "credential.helper=",  # never invoke a credential manager
        repo["clone_url"], str(dest),
    ]
    env = {
        **os.environ,
        "GIT_TERMINAL_PROMPT": "0",  # fail fast on deleted/private repos
        "GCM_INTERACTIVE": "never",
    }
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=CLONE_TIMEOUT,
        stdin=subprocess.DEVNULL, env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git clone failed: {result.stderr[:200]}")
    return dest


def _process(repo):
    dest = _clone(repo)
    try:
        result = scan_repo(dest, repo["slug"])
    finally:
        _rmtree(dest)
    repo["status"] = "scanned"
    repo["issues"] = len(result["issues"])
    repo["tools_run"] = result["tools_run"]
    repo["loc"] = sum(result["loc_by_extension"].values())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--shard", type=int, default=0, help="shard index (0-based)")
    parser.add_argument("--shards", type=int, default=1, help="total parallel shards")
    args = parser.parse_args()

    CLONES_DIR.mkdir(exist_ok=True)
    RESULTS_DIR.mkdir(exist_ok=True)
    fails_dir = RESULTS_DIR.parent / "failures"
    fails_dir.mkdir(exist_ok=True)

    repos = _load_state()
    pending = [
        r for i, r in enumerate(repos)
        if r["status"] == "candidate"
        and i % args.shards == args.shard
        and not (RESULTS_DIR / f"{r['slug']}.json").exists()
        and not (fails_dir / f"{r['slug']}.txt").exists()
    ]
    if args.limit:
        pending = pending[: args.limit]
    print(f"[run_all:{args.shard}] {len(pending)} repos to process")

    started = time.time()
    done = failed = 0
    for i, repo in enumerate(pending, 1):
        try:
            _process(repo)
            done += 1
            print(f"[{args.shard}:{i}/{len(pending)}] OK   {repo['full_name']} issues={repo['issues']}")
        except Exception as e:  # noqa: BLE001 - keep the batch alive
            failed += 1
            (fails_dir / f"{repo['slug']}.txt").write_text(str(e)[:500], encoding="utf-8")
            print(f"[{args.shard}:{i}/{len(pending)}] FAIL {repo['full_name']}: {str(e)[:120]}")
            if "--verbose" in sys.argv:
                traceback.print_exc()

    mins = (time.time() - started) / 60
    print(f"\n[run_all:{args.shard}] done={done} failed={failed} in {mins:.0f} min")


if __name__ == "__main__":
    main()
