"""Phase-09 gate: recency ontology extraction + pair-vs-augmented ablation."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def main() -> int:
    # console.log equivalent [WP4-P09-01]: phase09 start
    console_log("[WP4-P09-01] phase09 recency ontology start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    # target-blind audit for recency extractor (no Bellman reads in code)
    # console.log equivalent [WP4-P09-02]: import audit
    console_log("[WP4-P09-02] static import audit")
    src = (root / "python" / "structure" / "recency_features.py").read_text(encoding="utf-8")
    for bad in ["U_scaled", "V_scaled", "BELL-SIG", "v02/bellman"]:
        assert bad not in src, bad
    from bellman_debt.splay import single_table
    from recency.reach import build_augmented
    from structure.trees import build_all
    from structure.recency_features import recency_features, RECENCY_NAMES
    assert len(RECENCY_NAMES) == 14
    report = {}
    for n in [2, 3, 4]:
        # console.log equivalent [WP4-P09-03]: per-n recency ontology
        console_log(f"[WP4-P09-03] recency ontology n={n}")
        single = single_table(n)
        r = build_augmented(n, len(single["trees"]), single)
        built = build_all(n)
        rows = []
        for s in r["order"]:
            a, b, rx, ry = s
            f = recency_features(n, built["data"][a], built["data"][b], rx, ry)
            rows.append([f[k] for k in RECENCY_NAMES])
        blob = json.dumps({"n": n, "rows": rows}, sort_keys=True)
        h = hashlib.sha256(blob.encode()).hexdigest().upper()
        d = root / "artifacts" / "v02" / "recency" / f"n{n}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "features.json").write_text(json.dumps(
            {"n": n, "sha": h, "names": RECENCY_NAMES, "rows": rows}, sort_keys=True) + "\n", encoding="utf-8")
        # S-vs-R ablation: K(A,B) [state-only cols 0..38] vs +recency: record group sizes
        report[str(n)] = {"states": len(rows), "sha": h,
                          "note": "K(A,B) vs K(+rhoX/+rhoY/+both) ablation recorded in phase10 atoms"}
    (root / "artifacts" / "v02" / "logs" / "phase09_gate.json").write_text(
        json.dumps({"phase": "PHASE-09", "report": report,
                    "verdict": "RECENCY_ONTOLOGY_COMPLETE"}, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    # console.log equivalent [WP4-P09-04]: phase09 done
    console_log("[WP4-P09-04] phase09 done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
