"""Target-blind extraction driver: state serialization + tree tables + frozen ontology.

Writes per-n feature tables with hashes; Bellman join happens only in a
separate post-freeze step (mining), never inside extraction.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def extract_n(n: int, out_dir: Path) -> dict:
    # console.log equivalent [WP3-EXT-01]: extract start
    console_log(f"[WP3-EXT-01] extract n={n} start")
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "python"))
    from structure.trees import build_all
    from structure.features import pair_features, FEATURE_NAMES
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    built = build_all(n)
    single = single_table(n)
    reach = build_reachability(n, len(single["trees"]), single)
    C = len(built["serials"])
    rows = []
    for pid in reach["ids"]:
        a = pid // C
        b = pid % C
        f = pair_features(n, built["data"][a], built["data"][b])
        rows.append({"state_id": str(pid), "scalars": [f["scalars"][k] for k in FEATURE_NAMES]})
    blob = json.dumps({"n": n, "features": FEATURE_NAMES, "rows": rows}, sort_keys=True)
    h = hashlib.sha256(blob.encode()).hexdigest().upper()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"n{n}.json").write_text(json.dumps({"n": n, "sha": h, "rows": rows, "features": FEATURE_NAMES}, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP3-EXT-02]: extract done
    console_log(f"[WP3-EXT-02] extract n={n} done rows={len(rows)} sha={h[:12]}")
    return {"n": n, "rows": len(rows), "sha": h}
