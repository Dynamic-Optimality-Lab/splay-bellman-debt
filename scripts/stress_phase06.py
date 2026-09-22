"""WP-6 stress: seal determinism, manifest coverage, no-proof discipline, ledger stability."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest().upper()


def main() -> int:
    # console.log equivalent [WP6-STR-01]: stress start
    console_log("[WP6-STR-01] stress phase06 start")
    root = Path(__file__).resolve().parents[1]
    # console.log equivalent [WP6-STR-02]: manifest coverage
    console_log("[WP6-STR-02] manifest coverage (all tracked scientific files)")
    man = (root / "artifacts" / "v02" / "seal" / "MANIFEST.sha256").read_text().splitlines()
    r = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True)
    tracked = sorted(f for f in r.stdout.splitlines() if not f.startswith(".git/"))
    covered = {l.split("  ", 1)[1] for l in man}
    missing = [f for f in tracked if f not in covered and "MANIFEST.sha256" not in f and "tar.zst" not in f]
    assert not missing, missing[:5]
    # console.log equivalent [WP6-STR-03]: archive determinism
    console_log("[WP6-STR-03] archive determinism (rebuild + compare)")
    before = (root / "SPLAY-AM-BD-v0.2.tar.zst.sha256").read_text().split()[0]
    sys.path.insert(0, str(root / "scripts"))
    subprocess.run([sys.executable, "scripts/check_seal.py"], cwd=root, check=True)
    after = (root / "SPLAY-AM-BD-v0.2.tar.zst.sha256").read_text().split()[0]
    assert before == after, (before, after)
    # console.log equivalent [WP6-STR-04]: no-proof discipline
    console_log("[WP6-STR-04] no universal proof artifacts exist")
    ledger = json.loads((root / "math" / "proof_status.json").read_text())
    by_id = {o["id"]: o for o in ledger["obligations"]}
    for bid in ("BD0-08", "BD0-09", "BD0-11", "BD0-12", "BD0-14"):
        assert by_id[bid]["status"] == "UNPROVED", bid
    # console.log equivalent [WP6-STR-05]: ledger stability
    console_log("[WP6-STR-05] BD0-01..07/13/15 still REVIEWED")
    for bid in ("BD0-01", "BD0-02", "BD0-03", "BD0-04", "BD0-05", "BD0-06", "BD0-07", "BD0-13", "BD0-15"):
        assert by_id[bid]["status"] in ("PROVED", "REVIEWED"), bid
    out = {"verdict": "STRESS_PASS", "checks": 5}
    (root / "artifacts" / "v02" / "logs" / "phase06_stress.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP6-STR-06]: stress pass
    console_log("[WP6-STR-06] STRESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
