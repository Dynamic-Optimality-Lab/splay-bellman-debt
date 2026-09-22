"""WP-1 stress: determinism, manifest stability, out-discipline, schema validity."""
from __future__ import annotations

import hashlib
import json
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
    # console.log equivalent [WP1-S-01]: stress start
    console_log("[WP1-S-01] stress_phase00 start")
    root = Path(__file__).resolve().parents[1]
    # console.log equivalent [WP1-S-02]: rerun determinism
    console_log("[WP1-S-02] rerun determinism check")
    g1 = (root / "artifacts" / "v02" / "logs" / "phase00_gate.json").read_text(encoding="utf-8")
    import subprocess
    subprocess.run(["python", "scripts/check_phase00.py"], cwd=root, check=True)
    g2 = (root / "artifacts" / "v02" / "logs" / "phase00_gate.json").read_text(encoding="utf-8")
    assert g1 == g2, "gate JSON non-deterministic"
    # console.log equivalent [WP1-S-03]: bootstrap stability
    console_log("[WP1-S-03] bootstrap manifest stability")
    lines = (root / "parent" / "BOOTSTRAP_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 9, f"expected 9 parent files, got {len(lines)}"
    # console.log equivalent [WP1-S-04]: out-discipline
    console_log("[WP1-S-04] out-discipline: no WP-2+ artifacts")
    forbidden = [
        root / "artifacts" / "v02" / "bellman",
        root / "artifacts" / "v02" / "structure",
        root / "artifacts" / "v02" / "kernels",
        root / "artifacts" / "v02" / "hypotheses",
        root / "artifacts" / "v02" / "holdouts",
    ]
    for p in forbidden:
        assert not p.exists(), f"out-discipline violation: {p} exists"
    # console.log equivalent [WP1-S-05]: schema validity
    console_log("[WP1-S-05] schema JSON validity")
    import glob
    schemas = glob.glob(str(root / "schemas" / "*.schema.json"))
    assert len(schemas) == 12, f"expected 12 schemas, got {len(schemas)}"
    for s in schemas:
        json.loads(Path(s).read_text(encoding="utf-8"))
    # console.log equivalent [WP1-S-06]: external hash agreement
    console_log("[WP1-S-06] external hash agreement")
    man = json.loads((root / "external" / "MANIFEST.json").read_text(encoding="utf-8"))
    l2 = [s for s in man["sources"] if s["source_id"] == "L2"][0]
    assert sha256_file(root / "external" / "papers" / "L2_levy_tarjan.pdf") == l2["sha256"]
    out = {"verdict": "STRESS_PASS", "checks": 6}
    (root / "artifacts" / "v02" / "logs" / "phase00_stress.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP1-S-07]: stress pass
    console_log("[WP1-S-07] STRESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
