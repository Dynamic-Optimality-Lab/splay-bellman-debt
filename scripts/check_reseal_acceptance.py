"""WP-1 reseal acceptance A1-A20 (fail-closed; any failure => FOUNDATION_NOT_FROZEN)."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest().upper()


def main() -> int:
    # console.log equivalent [WP1-ACC-01]: acceptance start
    console_log("[WP1-ACC-01] reseal acceptance A1-A20 start")
    root = Path(__file__).resolve().parents[1]
    seal = json.loads((root / "parent" / "PARENT_SEAL.json").read_text(encoding="utf-8"))
    # console.log equivalent [WP1-ACC-02]: A1-A5 foundation
    console_log("[WP1-ACC-02] checking A1-A5")
    assert seal["sealed_commit"] == "6de1ca2a595e8895f54794f3a211fe6ee1a95a80", "A1"
    assert (root / "parent" / "BOOTSTRAP_MANIFEST.sha256").is_file(), "A2"
    fw = json.loads((root / "parent" / "H1_FIREWALL_SEAL.json").read_text(encoding="utf-8"))
    assert fw["state"] == "EMPTY" and fw["unlock"] is None, "A3"
    assert seal["n8_status"] == "PARTIALLY_REVEALED_CANARY_CONTAMINATED", "A4"
    expected_sha = (root / "prereg" / "prereg_sha256.txt").read_text(encoding="utf-8").strip()
    import hashlib as hl
    files = ["prereg/experiment_v0.2.yaml", "prereg/parent_contract.yaml", "prereg/b_panel.yaml",
             "prereg/state_tracks.yaml", "prereg/ontology_v0.2.yaml", "prereg/candidate_policy.yaml",
             "prereg/holdouts.yaml", "prereg/threat_control_matrix.yaml", "prereg/stop_control_matrix.yaml",
             "prereg/discovery_splits.yaml", "prereg/allowed_claims.md", "prereg/forbidden_claims.md"]
    h = hl.sha256()
    for f in sorted(files):
        h.update((root / f).read_bytes())
    assert h.hexdigest().upper() == expected_sha, "A5"
    # console.log equivalent [WP1-ACC-03]: A6-A9 theorem
    console_log("[WP1-ACC-03] checking A6-A9")
    ledger = json.loads((root / "math" / "proof_status.json").read_text(encoding="utf-8"))
    bd15 = [o for o in ledger["obligations"] if o["id"] == "BD0-15"][0]
    assert (root / bd15["proof"]).is_file(), "A6"
    assert sha256_file(root / bd15["proof"]) == bd15["proof_sha256"], "A7"
    assert bd15["status"] == "REVIEWED", "A8"
    assert [x["status"] for x in bd15["history"]] == ["UNPROVED", "PROVED", "REVIEWED"], "A8-history"
    r = subprocess.run([sys.executable, "-m", "pytest", "tests/parent/test_bd015_recency_v_blindness.py", "-q"],
                       cwd=root, capture_output=True, text=True)
    assert r.returncode == 0, f"A9: {r.stdout[-500:]}"
    # console.log equivalent [WP1-ACC-04]: A10-A13 literature
    console_log("[WP1-ACC-04] checking A10-A13")
    man = json.loads((root / "external" / "MANIFEST.json").read_text(encoding="utf-8"))
    by_id = {s["source_id"]: s for s in man["sources"]}
    assert by_id["L1"]["freeze_method"] == "BIBLIOGRAPHIC_IDENTITY" and by_id["L1"]["status"] == "FROZEN", "A10"
    assert by_id["L4"]["freeze_method"] == "LOCAL_BYTES" and by_id["L4"]["status"] == "FROZEN", "A11"
    assert sha256_file(root / "external" / "papers" / "L2_levy_tarjan.pdf") == by_id["L2"]["sha256"], "A12"
    assert sha256_file(root / "external" / "papers" / "L3_chmel_et_al_2026.pdf") == by_id["L3"]["sha256"], "A12"
    assert sha256_file(root / "external" / "papers" / "L4_geometric_inversions_2020.pdf") == by_id["L4"]["sha256"], "A11-sha"
    assert set(by_id) == {"L0", "L1", "L2", "L3", "L4"}, "A13"
    # console.log equivalent [WP1-ACC-05]: A14-A18 structure
    console_log("[WP1-ACC-05] checking A14-A18")
    import glob
    schemas = glob.glob(str(root / "schemas" / "*.schema.json"))
    assert len(schemas) == 12, "A14-count"
    for s in schemas:
        raw = open(s, "rb").read()
        assert not raw.startswith(b"\xef\xbb\xbf"), f"A14-BOM {s}"
        json.loads(raw.decode("utf-8"))
    tids = set()
    for line in (root / "prereg" / "threat_control_matrix.yaml").read_text(encoding="utf-8").splitlines():
        if line.startswith("T"):
            tids.add(line.split(":")[0])
    assert tids == {f"T{i:02d}" for i in range(1, 51)}, "A15"
    sids = set()
    for line in (root / "prereg" / "stop_control_matrix.yaml").read_text(encoding="utf-8").splitlines():
        if line.startswith("STOP-"):
            sids.add(line.split(":")[0])
    assert sids == {f"STOP-{i:02d}" for i in range(1, 31)}, "A16"
    splits = (root / "prereg" / "discovery_splits.yaml").read_text(encoding="utf-8")
    assert "frozen: true" in splits and "TRACK_S:" in splits and "TRACK_R:" in splits, "A17"
    for d in ["artifacts/v02/bellman", "artifacts/v02/structure", "artifacts/v02/kernels",
              "artifacts/v02/hypotheses", "artifacts/v02/holdouts", "artifacts/v02/recency",
              "artifacts/v02/debt_atoms", "artifacts/v02/falsification", "artifacts/v02/adversarial"]:
        assert not (root / d).exists(), f"A18 {d}"
    # console.log equivalent [WP1-ACC-06]: A19-A20 tests+stress
    console_log("[WP1-ACC-06] checking A19-A20")
    r1 = subprocess.run([sys.executable, "-m", "pytest", "tests/parent", "-q"],
                        cwd=root, capture_output=True, text=True)
    assert r1.returncode == 0, f"A19: {r1.stdout[-500:]}"
    r2 = subprocess.run([sys.executable, "scripts/stress_phase00.py"],
                        cwd=root, capture_output=True, text=True)
    assert r2.returncode == 0, f"A20: {r2.stdout[-500:]}"
    out = {"verdict": "RESEAL_PASS", "checks": 20}
    (root / "artifacts" / "v02" / "logs" / "phase00_reseal.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP1-ACC-07]: reseal pass
    console_log("[WP1-ACC-07] RESEAL_PASS A1-A20")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
