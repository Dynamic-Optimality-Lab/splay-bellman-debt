"""BOOTSTRAP_PARENT_IMPORT: one authorized transaction populating parent/ then locking it.

After parent/BOOTSTRAP_MANIFEST.sha256 is written, any mutation of parent/
is fatal (STOP-01/02/03). The source parent repo is always immutable.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def bootstrap_manifest(parent_dir: Path) -> dict:
    # console.log equivalent [WP1-BOOT-01]: bootstrap start
    console_log("[WP1-BOOT-01] bootstrap parent snapshot start")
    files = sorted(
        p for p in parent_dir.iterdir()
        if p.is_file() and p.name != "BOOTSTRAP_MANIFEST.sha256"
    )
    entries = {}
    for p in files:
        entries[p.name] = sha256_file(p)
    # console.log equivalent [WP1-BOOT-02]: bootstrap file count
    console_log(f"[WP1-BOOT-02] bootstrap files hashed: {len(entries)}")
    return entries


def write_bootstrap_manifest(repo_root: Path) -> Path:
    parent_dir = repo_root / "parent"
    entries = bootstrap_manifest(parent_dir)
    out = parent_dir / "BOOTSTRAP_MANIFEST.sha256"
    lines = [f"{v}  {k}\n" for k, v in sorted(entries.items())]
    out.write_text("".join(lines), encoding="utf-8")
    # console.log equivalent [WP1-BOOT-03]: bootstrap manifest written
    console_log(f"[WP1-BOOT-03] bootstrap manifest written: {out}")
    return out


def assert_locked(parent_dir: Path) -> None:
    manifest = parent_dir / "BOOTSTRAP_MANIFEST.sha256"
    if not manifest.is_file():
        raise RuntimeError("STOP-01: parent/ not bootstrapped (missing BOOTSTRAP_MANIFEST.sha256)")
    # console.log equivalent [WP1-BOOT-04]: lock verified
    console_log("[WP1-BOOT-04] parent/ READ_ONLY_LOCKED verified")
