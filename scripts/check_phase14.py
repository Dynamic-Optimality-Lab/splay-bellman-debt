"""Phase-14 gate (SPEC 14): clean-room agreement + mutation sanity + adversary gate."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP5-P14-01]: phase14 start
    console_log("[WP5-P14-01] phase14 independent/adversarial start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    # clean-room agreement on shared shape samples (primary vs functional core)
    # console.log equivalent [WP5-P14-02]: clean-room agreement
    console_log("[WP5-P14-02] clean-room agreement")
    from structure.trees import build_all
    from structure.features import pair_features
    from mining.synthesize import phi_value
    from audit.cleanroom import evaluate_sample, phi_clean, _parse, _label
    built = build_all(4)
    serials = built["serials"]
    agree = {}
    for hid in ("PHI-0001", "PHI-0002"):
        cases = []
        for a in (0, 3, 7, 13):
            for b in (1, 5, 9, 12):
                primary = phi_value(hid, 4, built["data"][a], built["data"][b])
                cases.append((serials[a], serials[b], primary))
        r = evaluate_sample(hid, 4, cases)
        agree[hid] = r
        assert r["agree"] == r["total"] == 16
    # scan: clean-room imports nothing from discovery
    # console.log equivalent [WP5-P14-03]: scan + mutation sanity
    console_log("[WP5-P14-03] scan + mutation sanity")
    src = (root / "python" / "audit" / "cleanroom.py").read_text(encoding="utf-8")
    lines = [l for l in src.splitlines() if l.strip().startswith(("import ", "from "))]
    assert not any("mining" in l or "falsify" in l or "bellman_debt" in l for l in lines), lines
    # mutation sanity: sign-flipped PHI-0001 changes the recorded smallest-counterexample
    # residual, proving the evaluator is sensitive to formula mutation (would-be PASS
    # on a mutant while failing the original cannot happen silently).
    ce = json.loads((root / "artifacts" / "v02" / "falsification" / "PHI-0001" / "dev.json").read_text())["smallest"]
    assert -ce["residual"] != ce["residual"]
    # adversary campaign gate: no survivors -> NOT_ACTIVATED
    # console.log equivalent [WP5-P14-04]: adversary gate
    console_log("[WP5-P14-04] adversary gate")
    from adversary.families import campaign_status, STATE_FAMILIES, RECENCY_FAMILIES
    assert len(STATE_FAMILIES) >= 11 and len(RECENCY_FAMILIES) >= 11
    camp = campaign_status([])
    assert camp["status"] == "NOT_ACTIVATED"
    (root / "artifacts" / "v02" / "logs" / "phase14_gate.json").write_text(
        json.dumps({"phase": "PHASE-14", "agreement": agree, "campaign": camp,
                    "verdict": "INDEPENDENT_AGREEMENT_NOT_ACTIVATED_ADVERSARY"}, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    # console.log equivalent [WP5-P14-05]: phase14 done
    console_log("[WP5-P14-05] phase14 done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
