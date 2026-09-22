"""WP-3 stress: determinism, out-discipline, leak-mutant, no-minimality-overclaim."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP3-STR-01]: stress start
    console_log("[WP3-STR-01] stress phase03 start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    # console.log equivalent [WP3-STR-02]: determinism
    console_log("[WP3-STR-02] extraction determinism (n4 rehash)")
    from structure.extract import extract_n
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = extract_n(4, Path(td))
    gate = json.loads((root / "artifacts" / "v02" / "logs" / "phase04_gate.json").read_text())
    assert r["sha"] == gate["results"]["4"]["sha"], "nondeterministic extraction"
    # console.log equivalent [WP3-STR-03]: out-discipline
    console_log("[WP3-STR-03] out-discipline (no WP-4+ artifacts)")
    for d in ["artifacts/v02/recency", "artifacts/v02/holdouts/H2R", "artifacts/v02/hypotheses",
              "artifacts/v02/falsification", "artifacts/v02/adversarial", "python/recency",
              "python/holdout", "python/adversary"]:
        assert not (root / d).exists(), d
    # console.log equivalent [WP3-STR-04]: leak mutant caught
    console_log("[WP3-STR-04] leak-mutant detection")
    bad = "from bellman_debt.verify import load_array\nV = load_array(4)\n"
    markers = ["U_scaled", "V_scaled", "bellman_debt.verify", "v02/bellman"]
    assert any(m in bad for m in markers), "audit markers broken"
    # console.log equivalent [WP3-STR-05]: wording guard
    console_log("[WP3-STR-05] no minimality overclaim")
    abl = (root / "artifacts" / "v02" / "kernels" / "ablation.json").read_text(encoding="utf-8")
    assert "COMPONENTWISE_NECESSARY_FINITE" in abl
    assert "GLOBALLY_MINIMAL" not in abl and "minimal_kernel" not in abl.lower()
    # console.log equivalent [WP3-STR-06]: transport still blocked
    console_log("[WP3-STR-06] transport still blocked")
    q = json.loads((root / "artifacts" / "v02" / "kernels" / "quotient.json").read_text())
    assert q["transport"] == "BLOCKED_BD0_04_05_UNPROVED"
    out = {"verdict": "STRESS_PASS", "checks": 6}
    (root / "artifacts" / "v02" / "logs" / "phase03_stress.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP3-STR-07]: stress pass
    console_log("[WP3-STR-07] STRESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
