"""Phase-13 gate (SPEC 13): correct validation-resource consumption (once, in order).

With zero development survivors, no fresh resource is consumed:
H1 stays EMPTY/unread, H2R stays BANK_COMMITTED/unlocks-0, n8 sees no
candidate contact. This non-consumption is the fail-closed outcome and
is recorded with firewall evidence. Any future survivor would follow:
Track-S: EV8-contaminated first, then H1 unlock-once; Track-R: H2R unlock-once.
"""
from __future__ import annotations

import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP5-P13-01]: phase13 start
    console_log("[WP5-P13-01] phase13 holdout gate start")
    root = Path(__file__).resolve().parents[1]
    gate12 = json.loads((root / "artifacts" / "v02" / "logs" / "phase12_gate.json").read_text())
    assert gate12["survivors"] == [], gate12["survivors"]
    # console.log equivalent [WP5-P13-02]: firewall evidence
    console_log("[WP5-P13-02] firewall evidence (no consumption)")
    h2r = json.loads((root / "artifacts" / "v02" / "holdouts" / "H2R" / "firewall.json").read_text())
    assert h2r["state"] == "BANK_COMMITTED" and h2r.get("unlocks", 0) == 0
    # H1: parent-sealed bank untouched (no v0.2 read); n8: no candidate contact.
    # console.log equivalent [WP5-P13-03]: empty set commitment
    console_log("[WP5-P13-03] empty candidate-set commitment")
    d = root / "artifacts" / "v02" / "holdouts"
    d.mkdir(parents=True, exist_ok=True)
    (d / "candidate_set.json").write_text(json.dumps(
        {"set": [], "reason": "zero development survivors; no fresh reveal occurred",
         "h1": "UNREAD", "h2r": "UNLOCKED_NEVER", "n8": "UNCONTACTED"}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (root / "artifacts" / "v02" / "logs" / "phase13_gate.json").write_text(
        json.dumps({"phase": "PHASE-13", "consumed": "NONE",
                    "verdict": "HOLDOUTS_PRISTINE"}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP5-P13-04]: phase13 done
    console_log("[WP5-P13-04] phase13 done (nothing consumed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
