"""Theorem-gate matrix verifier: BD0-01..15 covered exactly once, consumers fail-closed."""
from __future__ import annotations

import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP2-GATE-01]: gate matrix start
    console_log("[WP2-GATE-01] theorem gate matrix verify start")
    root = Path(__file__).resolve().parents[1]
    ledger = json.loads((root / "math" / "proof_status.json").read_text(encoding="utf-8"))
    by_id = {o["id"]: o for o in ledger["obligations"]}
    assert set(by_id) == {f"BD0-{i:02d}" for i in range(1, 16)}, "ledger ID set"
    rows: dict = {}
    for line in (root / "prereg" / "theorem_gate_matrix.yaml").read_text(encoding="utf-8").splitlines():
        if line.startswith("BD0-"):
            rows[line.split(":")[0]] = line
    assert set(rows) == set(by_id), "matrix covers ledger exactly once"
    for bid, o in by_id.items():
        assert o["status"] in ("UNPROVED", "PROVED", "REVIEWED", "BLOCKED"), bid
    # consumers fail-closed: WP-3 needs BD0-02/03 REVIEWED
    assert by_id["BD0-02"]["status"] == "REVIEWED", "WP-3 gate BD0-02"
    assert by_id["BD0-03"]["status"] == "REVIEWED", "WP-3 gate BD0-03"
    # BD0-04/05 REVIEWED by WP-3 theorem closure; BD0-06..14 not promoted
    assert by_id["BD0-04"]["status"] == "REVIEWED", "BD0-04"
    assert by_id["BD0-05"]["status"] == "REVIEWED", "BD0-05"
    for bid in [f"BD0-{i:02d}" for i in range(6, 15)]:
        assert by_id[bid]["status"] == "UNPROVED", f"{bid} must remain UNPROVED (owning phase)"
    assert by_id["BD0-15"]["status"] == "REVIEWED"
    out = {"verdict": "GATE_MATRIX_PASS", "n": len(rows)}
    (root / "artifacts" / "v02" / "logs" / "theorem_gate_check.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP2-GATE-02]: gate matrix pass
    console_log("[WP2-GATE-02] GATE_MATRIX_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
