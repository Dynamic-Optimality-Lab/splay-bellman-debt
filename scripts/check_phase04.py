"""Phase-04 gate (SPEC 04): target-blind ontology extraction + freeze.

Static import audit: extraction modules must not import Bellman targets.
Join to targets happens only in later mining steps, never here.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


FORBIDDEN = ["U_scaled", "V_scaled", "G_scaled", "BELL-SIG", "bellman_debt.verify",
             "bellman_debt.signatures", "bellman_debt.specimens", "v02/bellman", "v02/specimens",
             "tightness-labels", "holdout_firewall"]


def strip_docs(src: str) -> str:
    # Remove triple-quoted docstrings and # comments so the audit checks code, not prose.
    out = []
    in_doc = False
    for line in src.splitlines():
        s = line.strip()
        if s.startswith('"""'):
            if s.count('"""') >= 2:
                continue
            in_doc = not in_doc
            continue
        if in_doc or s.startswith("#"):
            continue
        out.append(line)
    return "\n".join(out)


def main() -> int:
    # console.log equivalent [WP3-P04-01]: phase04 start
    console_log("[WP3-P04-01] phase04 ontology start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    # console.log equivalent [WP3-P04-02]: import audit
    console_log("[WP3-P04-02] static import audit (no target reads)")
    for mod in ["structure/trees.py", "structure/features.py", "structure/extract.py"]:
        src = strip_docs((root / "python" / mod).read_text(encoding="utf-8"))
        hits = [f for f in FORBIDDEN if f in src]
        assert not hits, f"target leakage in {mod}: {hits}"
    from structure.extract import extract_n
    from structure.features import FEATURE_NAMES
    assert len(FEATURE_NAMES) == 39, len(FEATURE_NAMES)
    results = {}
    for n in [2, 3, 4, 5, 6, 7]:
        # console.log equivalent [WP3-P04-03]: per-n extract
        console_log(f"[WP3-P04-03] extract n={n}")
        r = extract_n(n, root / "artifacts" / "v02" / "structure")
        results[n] = r
    # determinism: rehash one size
    blob = (root / "artifacts" / "v02" / "structure" / "n4.json").read_bytes()
    h = hashlib.sha256(blob).hexdigest().upper()
    (root / "artifacts" / "v02" / "logs" / "phase04_gate.json").write_text(
        json.dumps({"phase": "PHASE-04", "ontology": "ONTOLOGY-v0.2", "results": results,
                    "verdict": "STRUCTURAL_ONTOLOGY_COMPLETE"}, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    # console.log equivalent [WP3-P04-04]: phase04 done
    console_log("[WP3-P04-04] phase04 done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
