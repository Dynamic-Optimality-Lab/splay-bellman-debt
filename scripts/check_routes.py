"""Phase-15/16/17 record (SPEC 15,16,17): route activation audit.

Positive route needs a development survivor with independent agreement;
with zero survivors there is no primary theorem object, so no Pair Access
proof, no telescoping, and no Levy-Tarjan invocation are attempted.
Negative branch needs C1-C4 (all four); dev H-residual failures are not
actual-cost motifs (T29), so it is not activated. Both non-activations
are recorded as results, never as silent omissions.
"""
from __future__ import annotations

import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP6-RTE-01]: route audit start
    console_log("[WP6-RTE-01] route audit start")
    root = Path(__file__).resolve().parents[1]
    gate12 = json.loads((root / "artifacts" / "v02" / "logs" / "phase12_gate.json").read_text())
    gate14 = json.loads((root / "artifacts" / "v02" / "logs" / "phase14_gate.json").read_text())
    survivors = gate12["survivors"]
    assert survivors == []
    positive = {"activated": False,
                "reason": "zero development survivors; no primary theorem candidate to promote",
                "p15_proof": "NOT_ATTEMPTED", "p16_telescope_bridge": "NOT_ATTEMPTED"}
    # negative C1-C4: no reachable legal actual-cost motif with growing ratio was observed;
    # dev counterexamples are H-residual violations, not Splay-cost ratio growth (T29).
    negative = {"activated": False,
                "C1_reachable_legal_motif": False,
                "C2_parameterized_construction": False,
                "C3_growing_ratio": False,
                "C4_independent_replay": False,
                "reason": "no systematic actual-cost motif; H-residual failures are not Splay-ratio motifs"}
    assert gate14["campaign"]["status"] == "NOT_ACTIVATED"
    d = root / "artifacts" / "v02" / "seal"
    d.mkdir(parents=True, exist_ok=True)
    (d / "route_audit.json").write_text(json.dumps(
        {"positive": positive, "negative": negative}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP6-RTE-02]: route audit done
    console_log("[WP6-RTE-02] route audit done (neither route activated)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
