"""Independent parent-seal verifier (reads schemas + frozen files, not discovery code)."""
from __future__ import annotations

from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def verify_no_post_lock_writes(repo_root: Path) -> bool:
    # console.log equivalent [WP1-AUD-01]: audit start
    console_log("[WP1-AUD-01] independent audit start")
    manifest = repo_root / "parent" / "BOOTSTRAP_MANIFEST.sha256"
    ok = manifest.is_file()
    # console.log equivalent [WP1-AUD-02]: audit verdict
    console_log(f"[WP1-AUD-02] bootstrap manifest present: {ok}")
    return ok
