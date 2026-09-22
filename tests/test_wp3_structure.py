"""ST-01..06: structural ontology gates (target-blind, symmetric, deterministic)."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def _strip(src: str) -> str:
    out, in_doc = [], False
    for line in src.splitlines():
        s = line.strip()
        if s.startswith('"""'):
            if s.count('"""') >= 2:
                continue
            in_doc = not in_doc
            continue
        if in_doc or s.startswith("#"):
            continue
        out.append(line)
    return "\n".join(out)


def test_st01_no_target_imports() -> None:
    # console.log equivalent [WP3-ST-01]: ST-01
    console_log("[WP3-ST-01] ST-01 no target imports")
    for mod in ["structure/trees.py", "structure/features.py", "structure/extract.py"]:
        src = _strip((root() / "python" / mod).read_text(encoding="utf-8"))
        for bad in ["U_scaled", "V_scaled", "G_scaled", "BELL-SIG", "bellman_debt.verify",
                    "bellman_debt.signatures", "v02/bellman", "holdout_firewall"]:
            assert bad not in src, (mod, bad)


def test_st02_identical_zero() -> None:
    # console.log equivalent [WP3-ST-02]: ST-02
    console_log("[WP3-ST-02] ST-02 identical-pair zeros")
    sys.path.insert(0, str(root() / "python"))
    from structure.trees import build_all
    from structure.features import pair_features
    built = build_all(4)
    for tid in range(14):
        f = pair_features(4, built["data"][tid], built["data"][tid])
        s = f["scalars"]
        assert s["depth_sum_abs"] == 0 and s["parent_diff"] == 0 and s["anc_Aonly"] == 0
        assert s["size_sum_abs"] == 0 and s["interval_symdiff_sum"] == 0 and s["root_same"] == 1


def test_st03_mirror_invariance() -> None:
    # console.log equivalent [WP3-ST-03]: ST-03
    console_log("[WP3-ST-03] ST-03 mirror invariance")
    sys.path.insert(0, str(root() / "python"))
    from structure.trees import build_all, parse_shape, serialize_shape
    from structure.features import pair_features
    built = build_all(4)
    serials = built["serials"]

    def mirror_shape(s):
        return None if s is None else (mirror_shape(s[1]), mirror_shape(s[0]))

    def mirror_tid(tid):
        ms = serialize_shape(mirror_shape(parse_shape(serials[tid])))
        return serials.index(ms)

    def mirror_data(d):
        # Full order-reversal: shape mirror + key relabel k -> n+1-k.
        m = lambda k: 4 + 1 - k if k else 0
        return {
            "root": m(d["root"]),
            "parent": {m(k): m(p) for k, p in d["parent"].items()},
            "depth": {m(k): v for k, v in d["depth"].items()},
            "children": {m(k): [(m(c) if c is not None else None) for c in reversed(v)] for k, v in d["children"].items()},
            "size": {m(k): v for k, v in d["size"].items()},
            "interval": {m(k): (4 + 1 - v[1], 4 + 1 - v[0]) for k, v in d["interval"].items()},
            "ancestors": {m(k): {m(u) for u in v} for k, v in d["ancestors"].items()},
            "paths": {m(k): [m(u) for u in v] for k, v in d["paths"].items()},
            "heavy": {m(k): (m(v) if v is not None else None) for k, v in d["heavy"].items()},
        }

    for a in (0, 3, 7):
        for b in (1, 5, 13):
            f = pair_features(4, built["data"][a], built["data"][b])
            g = pair_features(4, mirror_data(built["data"][a]), mirror_data(built["data"][b]))
            assert f["scalars"] == g["scalars"], (a, b)
    # shape-mirror alone is covariant, not invariant (documented): skip


def test_st04_raw_reconstruction() -> None:
    # console.log equivalent [WP3-ST-04]: ST-04
    console_log("[WP3-ST-04] ST-04 raw atom reconstruction")
    sys.path.insert(0, str(root() / "python"))
    from structure.trees import build_all
    from structure.features import pair_features
    built = build_all(4)
    f = pair_features(4, built["data"][2], built["data"][9])
    assert f["scalars"]["depth_sum_abs"] == sum(f["raw"]["depth_delta_by_key"])
    assert f["scalars"]["parent_common"] + f["scalars"]["parent_Aonly"] == len(f["raw"]["parent_edges_A"])
    assert f["scalars"]["interval_symdiff_sum"] == sum(abs(x - y) for ia, ib in zip(f["raw"]["intervals_A"], f["raw"]["intervals_B"]) for x, y in zip(ia, ib))


def test_st05_deterministic_serialization() -> None:
    # console.log equivalent [WP3-ST-05]: ST-05
    console_log("[WP3-ST-05] ST-05 deterministic serialization")
    gate = json.loads((root() / "artifacts" / "v02" / "logs" / "phase04_gate.json").read_text())
    tbl = json.loads((root() / "artifacts" / "v02" / "structure" / "n4.json").read_text())
    assert tbl["rows"][0]["state_id"] == "0"
    assert gate["results"]["4"]["rows"] == len(tbl["rows"])


def test_st06_full_state_control() -> None:
    # console.log equivalent [WP3-ST-06]: ST-06
    console_log("[WP3-ST-06] ST-06 full-state control")
    sys.path.insert(0, str(root() / "python"))
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    single = single_table(4)
    reach = build_reachability(4, len(single["trees"]), single)
    assert len(set(reach["ids"])) == 196
