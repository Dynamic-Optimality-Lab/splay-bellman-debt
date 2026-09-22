"""Phase-11 gate (SPEC 11): ERA-BD-A synthesis freeze + correct-b precheck."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP5-P11-01]: phase11 start
    console_log("[WP5-P11-01] phase11 synthesis start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    from mining.synthesize import freeze, CANDIDATES
    frozen = freeze(root)
    assert len(frozen) == 3
    ids = [c["hypothesis_id"] for c in frozen]
    assert ids == ["PHI-0001", "PHI-0002", "PHI-0003"]
    for c in frozen:
        assert c["b_hypothesis"] == {"p": "2", "q": "1"}, c
    # correct-b precheck: 2/1 >= b_n* on 2..7 (cross-multiplied, exact)
    # console.log equivalent [WP5-P11-02]: b_H feasibility
    console_log("[WP5-P11-02] b_H=2 feasibility vs b_n*")
    for n, (pn, qn) in {2: (1, 1), 3: (1, 1), 4: (3, 2), 5: (8, 5), 6: (8, 5), 7: (23, 14)}.items():
        assert 2 * qn >= pn * 1, n
    (root / "artifacts" / "v02" / "logs" / "phase11_gate.json").write_text(
        json.dumps({"phase": "PHASE-11", "era": "ERA-BD-A", "candidates": ids,
                    "b_feasible_all_n": True, "verdict": "SYNTHESIS_FROZEN"}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP5-P11-03]: phase11 done
    console_log("[WP5-P11-03] phase11 done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
