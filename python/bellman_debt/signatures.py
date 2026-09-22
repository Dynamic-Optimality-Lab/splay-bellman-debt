"""BELL-SIG-v0.2 per-state signatures + per-edge classification (analysis reads Bellman)."""
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


def build_signatures(n: int, tree_count: int, single: dict, reach_ids: list[int]) -> dict:
    # console.log equivalent [WP2-SIG-01]: signatures start
    console_log(f"[WP2-SIG-01] signatures n={n} start")
    p, q = 2, 1
    size = tree_count * tree_count
    U = load_array(n, "U", size)
    V = load_array(n, "V", size)
    table = single["table"]
    sigs = []
    for pid in reach_ids:
        a = pid // tree_count
        b = pid % tree_count
        v_tight = []
        u_tight = []
        pos_keep = 0
        del_create = 0
        max_excess = 0
        max_dV_del = 0
        min_dV_keep = 0
        first = True
        for x in range(1, n + 1):
            ra = table[(a, x)]
            rb = table[(b, x)]
            ca, cb = ra["cost"], rb["cost"]
            t = ra["after"] * tree_count + rb["after"]
            Ws = q * cb - p * ca
            if Ws + (V[t] - V[pid]) == 0:
                v_tight.append(["KEEP", x])
            if Ws + (U[t] - U[pid]) == 0:
                u_tight.append(["KEEP", x])
            if Ws > 0:
                pos_keep += 1
                max_excess = max(max_excess, Ws)
            dV = V[t] - V[pid]
            if first or dV < min_dV_keep:
                min_dV_keep = dV
            first = False
            t2 = ra["after"] * tree_count + b
            Ws2 = -p * ca
            if Ws2 + (V[t2] - V[pid]) == 0:
                v_tight.append(["DELETE", x])
            if Ws2 + (U[t2] - U[pid]) == 0:
                u_tight.append(["DELETE", x])
            if V[t2] > V[pid]:
                del_create += 1
                max_dV_del = max(max_dV_del, V[t2] - V[pid])
        sigs.append({
            "schema_version": "BELL-SIG-v0.2",
            "n": n, "b": {"p": "2", "q": "1"},
            "state_id": str(pid),
            "U_scaled": str(U[pid]), "V_scaled": str(V[pid]), "G_scaled": str(U[pid] - V[pid]),
            "v_tight_actions": v_tight, "u_tight_actions": u_tight,
            "positive_excess_keep_count": pos_keep,
            "delete_creation_count": del_create,
            "max_keep_excess_scaled": str(max_excess),
            "max_delete_deltaV_scaled": str(max_dV_del),
        })
    # console.log equivalent [WP2-SIG-02]: signatures done
    console_log(f"[WP2-SIG-02] signatures n={n} done rows={len(sigs)}")
    return {"n": n, "signatures": sigs}
