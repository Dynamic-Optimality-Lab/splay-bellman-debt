"""WP-2 stress: determinism, out-discipline, wrong-b canary, import-scan gates."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP2-ST-01]: stress start
    console_log("[WP2-ST-01] stress phase02 start")
    root = Path(__file__).resolve().parents[1]
    # console.log equivalent [WP2-ST-02]: rerun determinism
    console_log("[WP2-ST-02] rerun determinism")
    g1 = (root / "artifacts" / "v02" / "logs" / "phase01_gate.json").read_bytes()
    subprocess.run([sys.executable, "scripts/check_phase01.py"], cwd=root, check=True)
    assert (root / "artifacts" / "v02" / "logs" / "phase01_gate.json").read_bytes() == g1
    # console.log equivalent [WP2-ST-03]: out-discipline
    console_log("[WP2-ST-03] out-discipline (no WP-3+ artifacts)")
    for d in ["artifacts/v02/structure", "artifacts/v02/kernels", "artifacts/v02/debt_atoms",
              "artifacts/v02/hypotheses", "artifacts/v02/holdouts", "artifacts/v02/recency"]:
        assert not (root / d).exists(), d
    # console.log equivalent [WP2-ST-04]: wrong-b canary
    console_log("[WP2-ST-04] wrong-b canary (b=2 V must violate b=1 inequalities at n=4)")
    sys.path.insert(0, str(root / "python"))
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    from bellman_debt.verify import load_array
    single = single_table(4)
    reach = build_reachability(4, len(single["trees"]), single)
    V2 = load_array(4, "V")
    table = single["table"]
    violations = 0
    for pid in reach["ids"]:
        a = pid // 14
        b = pid % 14
        for x in range(1, 5):
            ra = table[(a, x)]
            rb = table[(b, x)]
            t = ra["after"] * 14 + rb["after"]
            if (rb["cost"] - 1 * ra["cost"]) + (V2[t] - V2[pid]) > 0:
                violations += 1
    assert violations > 0, "BD-10 canary failed: wrong-b geometry unexpectedly satisfied"
    # console.log equivalent [WP2-ST-05]: import-scan gates
    console_log("[WP2-ST-05] import-scan gates")
    audit_src = (root / "python" / "audit" / "verify_bellman.py").read_text(encoding="utf-8")
    import_lines = [l for l in audit_src.splitlines() if l.strip().startswith(("import ", "from "))]
    assert not any("bellman_debt" in l for l in import_lines), "audit imports discovery"
    struct_src = (root / "python" / "bellman_debt" / "verify.py").read_text(encoding="utf-8")
    assert "zstandard" in struct_src  # exact dependency declared
    out = {"verdict": "STRESS_PASS", "checks": 5}
    (root / "artifacts" / "v02" / "logs" / "phase02_stress.json").write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP2-ST-06]: stress pass
    console_log("[WP2-ST-06] STRESS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
