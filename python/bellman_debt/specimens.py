"""Extremal specimen tables + canonical witnesses + human-readable trajectories."""
from __future__ import annotations

import json
from pathlib import Path

import zstandard as zstd


def console_log(msg: str) -> None:
    print(msg)


PARENT = Path(r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\parent_upstream_full")


def load_array(n: int, name: str, size: int) -> list[int]:
    raw = (PARENT / f"artifacts/potentials/n{n}/hypothesis_bH/{name}.json.zst").read_bytes()
    arr = json.loads(zstd.ZstdDecompressor().decompress(raw).decode("utf-8"))
    out = [0] * size
    key = {"U": "U_scaled", "V": "V_scaled", "G": "G_scaled"}[name]
    for row in arr:
        out[row["pair_id"]] = int(row[key])
    return out


def canonical_key(edge: tuple) -> tuple:
    return edge


def build_specimens(n: int, tree_count: int, single: dict, reach_ids: list[int]) -> dict:
    # console.log equivalent [WP2-SPEC-01]: specimens start
    console_log(f"[WP2-SPEC-01] specimens n={n} start")
    p, q = 2, 1
    size = tree_count * tree_count
    U = load_array(n, "U", size)
    V = load_array(n, "V", size)
    table = single["table"]
    keep_excess = []
    delete_create = []
    exact_repay = []
    vtight = []
    utight = []
    both = []
    for pid in reach_ids:
        a = pid // tree_count
        b = pid % tree_count
        for x in range(1, n + 1):
            ra = table[(a, x)]
            ca = ra["cost"]
            cb = single["table"][(b, x)]["cost"]
            t = ra["after"] * tree_count + single["table"][(b, x)]["after"]
            Ws = q * cb - p * ca
            Rv = Ws + (V[t] - V[pid])
            Ru = Ws + (U[t] - U[pid])
            base = {"n": n, "mode": "KEEP", "key": x, "source": str(pid), "target": str(t),
                    "a": ca, "y": cb, "w_scaled": Ws, "dV": V[t] - V[pid], "dU": U[t] - U[pid]}
            if Rv == 0:
                vtight.append({**base, "class": "V_TIGHT"})
            if Ru == 0:
                utight.append({**base, "class": "U_TIGHT"})
            if Rv == 0 and Ru == 0:
                both.append({**base, "class": "BOTH_TIGHT"})
            if Ws > 0:
                keep_excess.append({**base, "class": "KEEP_EXCESS"})
                if Rv == 0:
                    exact_repay.append({**base, "class": "EXACT_V_REPAYMENT"})
            t2 = ra["after"] * tree_count + b
            Ws2 = -p * ca
            Rv2 = Ws2 + (V[t2] - V[pid])
            Ru2 = Ws2 + (U[t2] - U[pid])
            b2 = {"n": n, "mode": "DELETE", "key": x, "source": str(pid), "target": str(t2),
                  "a": ca, "y": 0, "w_scaled": Ws2, "dV": V[t2] - V[pid], "dU": U[t2] - U[pid]}
            if Rv2 == 0:
                vtight.append({**b2, "class": "V_TIGHT"})
            if Ru2 == 0:
                utight.append({**b2, "class": "U_TIGHT"})
            if Rv2 == 0 and Ru2 == 0:
                both.append({**b2, "class": "BOTH_TIGHT"})
            if V[t2] > V[pid]:
                delete_create.append({**b2, "class": "CANONICAL_CREATION"})
    def wit(rows):
        if not rows:
            return None
        rows = sorted(rows, key=lambda r: (int(r["source"]), r["mode"], r["key"], int(r["target"])))
        return rows[0]
    out = {
        "n": n,
        "counts": {
            "keep_excess": len(keep_excess), "delete_create": len(delete_create),
            "exact_repay": len(exact_repay), "vtight": len(vtight),
            "utight": len(utight), "both": len(both),
        },
        "witnesses": {
            "keep_excess": wit(keep_excess), "delete_create": wit(delete_create),
            "exact_repay": wit(exact_repay),
        },
        "tables": {
            "keep_excess": keep_excess, "delete_create": delete_create,
            "exact_repay": exact_repay, "vtight": vtight,
            "utight": utight, "both": both,
        },
    }
    # console.log equivalent [WP2-SPEC-02]: specimens done
    console_log(f"[WP2-SPEC-02] specimens n={n} done")
    return out


def trajectory_md(n: int, witness: dict | None, single: dict, tree_count: int) -> str:
    if witness is None:
        return f"# n={n} no witness in class\n"
    lines = [f"# n={n} {witness['class']} witness",
             f"mode={witness['mode']} key={witness['key']} source={witness['source']} target={witness['target']}",
             f"a={witness['a']} y={witness['y']} w_scaled={witness['w_scaled']} dV={witness['dV']} dU={witness['dU']}"]
    # console.log equivalent [WP2-SPEC-03]: trajectory rendered
    console_log(f"[WP2-SPEC-03] trajectory n={n} class={witness['class']}")
    return "\n".join(lines) + "\n"
