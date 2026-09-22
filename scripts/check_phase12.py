"""Phase-12 gate (SPEC 12): exact development falsification of all frozen candidates."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP5-P12-01]: phase12 start
    console_log("[WP5-P12-01] phase12 falsification start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    from falsify.residuals import falsify_state_only, falsify_recency
    results = {}
    # console.log equivalent [WP5-P12-02]: falsify PHI-0001
    console_log("[WP5-P12-02] falsify PHI-0001")
    results["PHI-0001"] = falsify_state_only("PHI-0001", [2, 3, 4, 5, 6, 7], root)
    # console.log equivalent [WP5-P12-03]: falsify PHI-0002
    console_log("[WP5-P12-03] falsify PHI-0002")
    results["PHI-0002"] = falsify_state_only("PHI-0002", [2, 3, 4, 5, 6, 7], root)
    # console.log equivalent [WP5-P12-04]: falsify PHI-0003
    console_log("[WP5-P12-04] falsify PHI-0003")
    results["PHI-0003"] = falsify_recency("PHI-0003", [2, 3, 4], root)
    for hid, r in results.items():
        (root / "artifacts" / "v02" / "falsification" / hid).mkdir(parents=True, exist_ok=True)
        (root / "artifacts" / "v02" / "falsification" / hid / "dev.json").write_text(
            json.dumps(r, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    survivors = [h for h, r in results.items() if r["verdict"] == "SURVIVES_DEV"]
    (root / "artifacts" / "v02" / "logs" / "phase12_gate.json").write_text(
        json.dumps({"phase": "PHASE-12", "verdicts": {h: r["verdict"] for h, r in results.items()},
                    "survivors": survivors, "verdict": "DEV_FALSIFICATION_COMPLETE"},
                   indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    # console.log equivalent [WP5-P12-05]: phase12 done
    console_log(f"[WP5-P12-05] phase12 done survivors={survivors}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
