"""WP-5 stress: determinism, out-discipline, set immutability, no-universal-claim."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP5-STR-01]: stress start
    console_log("[WP5-STR-01] stress phase05 start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    # console.log equivalent [WP5-STR-02]: ledger determinism
    console_log("[WP5-STR-02] ledger verdicts deterministic")
    led = json.loads((root / "artifacts" / "v02" / "hypotheses" / "ledger.json").read_text())
    assert [(l["hypothesis_id"], l["status"]) for l in led] == [
        ("PHI-0001", "REJECTED"), ("PHI-0002", "REJECTED"), ("PHI-0003", "REJECTED")]
    # console.log equivalent [WP5-STR-03]: out-discipline
    console_log("[WP5-STR-03] out-discipline (no WP-6 seal artifacts)")
    assert not (root / "artifacts" / "v02" / "seal").exists()
    assert not (root / "SPLAY-AM-BD-v0.2.tar.zst").exists()
    # console.log equivalent [WP5-STR-04]: set immutability
    console_log("[WP5-STR-04] candidate-set empty and immutable")
    cs = json.loads((root / "artifacts" / "v02" / "holdouts" / "candidate_set.json").read_text())
    assert cs["set"] == []
    # console.log equivalent [WP5-STR-05]: no universal claim
    console_log("[WP5-STR-05] ceiling is finite survival (none) — no theorem")
    g12 = json.loads((root / "artifacts" / "v02" / "logs" / "phase12_gate.json").read_text())
    assert g12["survivors"] == []
    out = {"verdict": "STRESS_PASS", "checks": 5}
    (root / "artifacts" / "v02" / "logs" / "phase05_stress.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP5-STR-06]: stress pass
    console_log("[WP5-STR-06] STRESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
