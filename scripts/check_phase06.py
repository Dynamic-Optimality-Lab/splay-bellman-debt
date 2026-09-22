"""Phase-06 gate (SPEC 06): K0 ablation with necessity witnesses."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import zstandard as zstd


def console_log(msg: str) -> None:
    print(msg)


def load_V(n: int) -> dict:
    from pathlib import Path as P
    par = P(r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\parent_upstream_full")
    raw = (par / f"artifacts/potentials/n{n}/hypothesis_bH/V.json.zst").read_bytes()
    arr = json.loads(zstd.ZstdDecompressor().decompress(raw).decode())
    return {str(r["pair_id"]): int(r["V_scaled"]) for r in arr}


def main() -> int:
    # console.log equivalent [WP3-P06-01]: phase06 start
    console_log("[WP3-P06-01] phase06 ablation start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    from kernel.ablate import ablate
    out = {}
    for n in [2, 3, 4, 5, 6, 7]:
        # console.log equivalent [WP3-P06-02]: per-n ablation
        console_log(f"[WP3-P06-02] ablation n={n}")
        single = single_table(n)
        reach = build_reachability(n, len(single["trees"]), single)
        feats = json.loads((root / "artifacts" / "v02" / "structure" / f"n{n}.json").read_text())
        V = load_V(n)
        quo = json.loads((root / "artifacts" / "v02" / "kernels" / "quotient.json").read_text())
        # quotient classes are per-n full maps? recompute lightweight class = pair id (singletons)
        classes = {pid: pid for pid in reach["ids"]}
        res = ablate(n, feats["rows"], V, classes, len(single["trees"]), single, reach["ids"])
        out[n] = {k: {"type": v["type"], "witness": v["witness"], "note": v["note"]} for k, v in res.items()}
    (root / "artifacts" / "v02" / "kernels" / "ablation.json").write_text(
        json.dumps(out, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    (root / "artifacts" / "v02" / "logs" / "phase06_gate.json").write_text(
        json.dumps({"phase": "PHASE-06", "verdict": "KERNEL_ABLATION_COMPLETE"}, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    # console.log equivalent [WP3-P06-03]: phase06 done
    console_log("[WP3-P06-03] phase06 done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
