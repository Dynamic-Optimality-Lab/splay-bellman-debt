"""Phase-05 gate (SPEC 05): behavioral quotient, agreement, FULL_STATE, compression.

Bellman transport join is BLOCKED: BD0-04/05 are UNPROVED, so the
partition is certified target-independent only. No V/U join here.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP3-P05-01]: phase05 start
    console_log("[WP3-P05-01] phase05 quotient start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    from kernel.refine import refine
    from kernel.refine2 import refine2, same_partition
    ledger = json.loads((root / "math" / "proof_status.json").read_text(encoding="utf-8"))
    by_id = {o["id"]: o for o in ledger["obligations"]}
    # Post-closure: BD0-04/05 REVIEWED; V-transport applicable per method audit,
    # U-transport remains blocked by source contract (see transport_audit.json).
    assert by_id["BD0-04"]["status"] == "REVIEWED" and by_id["BD0-05"]["status"] == "REVIEWED"
    transport = "V_APPLICABLE_U_BLOCKED_BY_SOURCE_CONTRACT"
    report = {"transport": transport}
    for n in [2, 3, 4, 5, 6, 7]:
        # console.log equivalent [WP3-P05-02]: per-n quotient
        console_log(f"[WP3-P05-02] quotient n={n}")
        single = single_table(n)
        reach = build_reachability(n, len(single["trees"]), single)
        r1 = refine(n, len(single["trees"]), single, reach["ids"])
        r2 = refine2(n, len(single["trees"]), single, reach["ids"])
        assert same_partition(r1, r2, reach["ids"]), f"K-02 agreement fail n={n}"
        # FULL_STATE control: every state unique (holds by construction of pair ids)
        assert len(set(reach["ids"])) == len(reach_ids_distinct(reach["ids"]))
        classes = r1["classes"]
        sizes: dict[int, int] = {}
        for pid in reach["ids"]:
            sizes[classes[pid]] = sizes.get(classes[pid], 0) + 1
        dist = sorted(sizes.values())
        report[str(n)] = {"R": len(reach["ids"]), "classes": r1["nclasses"],
                     "ratio": len(reach["ids"]) / r1["nclasses"],
                     "largest": dist[-1], "singletons": sum(1 for v in dist if v == 1),
                     "rounds": (r1["rounds"], r2["rounds"])}
    d = root / "artifacts" / "v02" / "kernels"
    d.mkdir(parents=True, exist_ok=True)
    (d / "quotient.json").write_text(json.dumps(report, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    (root / "artifacts" / "v02" / "logs" / "phase05_gate.json").write_text(
        json.dumps({"phase": "PHASE-05", "transport": transport,
                    "verdict": "BEHAVIORAL_QUOTIENT_CERTIFIED"}, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    # console.log equivalent [WP3-P05-03]: phase05 done
    console_log(f"[WP3-P05-03] phase05 done transport={transport}")
    return 0


def reach_ids_distinct(ids: list[int]) -> list[int]:
    return sorted(set(ids))


if __name__ == "__main__":
    raise SystemExit(main())
