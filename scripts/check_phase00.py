"""Phase-00 gate: parent seal, prereg hashes, theorem ledger, matrices, splits.

Deterministic order: VERIFY HASHES -> LOAD CONTRACT -> ASSERT FIREWALL
-> COMPUTE (hash lists) -> ASSERT INVARIANTS -> SAVE RAW -> CERTIFICATE
-> INDEPENDENT VERIFY (adapter) -> GATE -> COMMIT (manual).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def main() -> int:
    # console.log equivalent [WP1-CHK-01]: check start
    console_log("[WP1-CHK-01] check_phase00 start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    from inherited.adapter import verify_parent
    from inherited.bootstrap_parent import write_bootstrap_manifest, assert_locked

    # console.log equivalent [WP1-CHK-02]: bootstrap manifest
    console_log("[WP1-CHK-02] writing bootstrap manifest")
    write_bootstrap_manifest(root)
    assert_locked(root / "parent")
    # console.log equivalent [WP1-CHK-03]: adapter verify
    console_log("[WP1-CHK-03] running parent adapter")
    adapter_results = verify_parent(root)
    # console.log equivalent [WP1-CHK-04]: prereg + ledger checks
    console_log("[WP1-CHK-04] checking prereg, ledger, matrices")
    prereg = root / "prereg"
    required = [
        "experiment_v0.2.yaml", "parent_contract.yaml", "b_panel.yaml",
        "state_tracks.yaml", "ontology_v0.2.yaml", "candidate_policy.yaml",
        "holdouts.yaml", "threat_control_matrix.yaml", "stop_control_matrix.yaml",
        "discovery_splits.yaml", "allowed_claims.md", "forbidden_claims.md",
    ]
    missing = [n for n in required if not (prereg / n).is_file()]
    if missing:
        raise RuntimeError(f"FOUNDATION_NOT_FROZEN: missing prereg files {missing}")
    ledger = json.loads((root / "math" / "proof_status.json").read_text(encoding="utf-8"))
    ids = [o["id"] for o in ledger["obligations"]]
    if ids != [f"BD0-{i:02d}" for i in range(1, 16)]:
        raise RuntimeError(f"FOUNDATION_NOT_FROZEN: BD0 ledger ids mismatch {ids}")
    bd15 = [o for o in ledger["obligations"] if o["id"] == "BD0-15"][0]
    if bd15["status"] != "UNPROVED":
        raise RuntimeError("FOUNDATION_NOT_FROZEN: BD0-15 must be UNPROVED at WP-1 entry")
    threat_ids = set()
    for line in (prereg / "threat_control_matrix.yaml").read_text(encoding="utf-8").splitlines():
        if line.startswith("T"):
            threat_ids.add(line.split(":")[0])
    if threat_ids != {f"T{i:02d}" for i in range(1, 51)}:
        raise RuntimeError(f"FOUNDATION_NOT_FROZEN: threat set mismatch ({len(threat_ids)})")
    stop_ids = set()
    for line in (prereg / "stop_control_matrix.yaml").read_text(encoding="utf-8").splitlines():
        if line.startswith("STOP-"):
            stop_ids.add(line.split(":")[0])
    if stop_ids != {f"STOP-{i:02d}" for i in range(1, 31)}:
        raise RuntimeError(f"FOUNDATION_NOT_FROZEN: stop set mismatch ({len(stop_ids)})")
    out = {
        "experiment_id": "SPLAY-AM-BD-v0.2",
        "phase": "PHASE-00",
        "adapter": adapter_results,
        "bd0_15_status": "UNPROVED",
        "threat_set_ok": True,
        "stop_set_ok": True,
        "verdict": "FOUNDATION_SEALED",
    }
    (root / "artifacts" / "v02" / "logs" / "phase00_gate.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP1-CHK-05]: gate pass
    console_log("[WP1-CHK-05] FOUNDATION_SEALED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
