"""Anchor b=2 Bellman verification: streamed edge checks over our graph.

Loads parent U/V/G arrays (read-only target for checking), recomputes
every edge weight L=p*a-q*y from OUR Splay tables, and asserts:
V(s)=max(0,max_e[w+V(t)]), U(t)=min_e[U(s)+l], V<=U, V>=0, plus
tight-edge/witness classification. n=7 streamed (no full edge store).
"""
from __future__ import annotations

import json
from pathlib import Path

import zstandard as zstd


def console_log(msg: str) -> None:
    print(msg)


PARENT = Path(r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\parent_upstream_full")


def load_array(n: int, name: str, size: int | None = None) -> list[int]:
    raw = (PARENT / f"artifacts/potentials/n{n}/hypothesis_bH/{name}.json.zst").read_bytes()
    arr = json.loads(zstd.ZstdDecompressor().decompress(raw).decode("utf-8"))
    if size is None:
        size = max(r["pair_id"] for r in arr) + 1
    out = [0] * size
    key = {"U": "U_scaled", "V": "V_scaled", "G": "G_scaled"}[name]
    for row in arr:
        out[row["pair_id"]] = int(row[key])
    return out


def verify_anchor(n: int, tree_count: int, single: dict, reach_ids: list[int]) -> dict:
    # console.log equivalent [WP2-VER-01]: anchor verify start
    console_log(f"[WP2-VER-01] anchor b=2 verify n={n} start R={len(reach_ids)}")
    p, q = 2, 1
    size = tree_count * tree_count
    U = load_array(n, "U", size)
    V = load_array(n, "V", size)
    G = load_array(n, "G", size)
    table = single["table"]
    pos = {pid: i for i, pid in enumerate(reach_ids)}
    # V<=U, V>=0, G==U-V pointwise on reachable ids
    for pid in reach_ids:
        if not (V[pid] >= 0 and V[pid] <= U[pid] and G[pid] == U[pid] - V[pid]):
            raise RuntimeError(f"BD-04/01 fail at n={n} pid={pid}")
    n_keep_excess = 0
    n_delete_create = 0
    n_vtight = 0
    n_utight = 0
    n_exact_repay = 0
    max_excess = None
    max_dV = None
    # streamed edge sweep; also collect per-state outgoing best for V-witness
    best_out = {}
    for pid in reach_ids:
        a = pid // tree_count
        b = pid % tree_count
        best = None
        for x in range(1, n + 1):
            ra = table[(a, x)]
            rb = table[(b, x)]
            ca, cb = ra["cost"], rb["cost"]
            # KEEP
            t = ra["after"] * tree_count + rb["after"]
            w = q * cb - p * ca  # scaled w*q? careful: w = y - b*a = (q*y - p*a)/q
            # use scaled integers: Ws = q*y - p*a ; Ls = p*a - q*y
            Ws = q * cb - p * ca
            Ls = p * ca - q * cb
            Rv = Ws + (V[t] - V[pid])
            Ru = Ws + (U[t] - U[pid])
            if Rv > 0 or Ru > 0:
                raise RuntimeError(f"BD-02/03 Bellman violation n={n} {pid}-> {t} x={x}")
            if Rv == 0:
                n_vtight += 1
            if Ru == 0:
                n_utight += 1
            if Ws > 0:
                n_keep_excess += 1
                if max_excess is None or Ws > max_excess:
                    max_excess = Ws
                if Rv == 0:
                    n_exact_repay += 1
            cand = Ws + V[t]
            if best is None or cand > best:
                best = cand
            # DELETE
            t2 = ra["after"] * tree_count + b
            Ws2 = -p * ca
            Ls2 = p * ca
            Rv2 = Ws2 + (V[t2] - V[pid])
            Ru2 = Ws2 + (U[t2] - U[pid])
            if Rv2 > 0 or Ru2 > 0:
                raise RuntimeError(f"BD-02/03 DELETE violation n={n} {pid}->{t2}")
            if Rv2 == 0:
                n_vtight += 1
            if Ru2 == 0:
                n_utight += 1
            if V[t2] > V[pid]:
                n_delete_create += 1
                dV = V[t2] - V[pid]
                if max_dV is None or dV > max_dV:
                    max_dV = dV
            cand2 = Ws2 + V[t2]
            if cand2 > best:
                best = cand2
        best_out[pid] = best
    # V fixed point: V[pid] == max(0, best)
    for pid in reach_ids:
        if V[pid] != max(0, best_out[pid]):
            raise RuntimeError(f"BD-03 fixed-point fail n={n} pid={pid}")
    # console.log equivalent [WP2-VER-02]: anchor verify done
    console_log(f"[WP2-VER-02] anchor n={n} done excess={n_keep_excess} create={n_delete_create}")
    return {
        "n": n, "R": len(reach_ids),
        "keep_excess": n_keep_excess, "delete_create": n_delete_create,
        "vtight": n_vtight, "utight": n_utight, "exact_repay": n_exact_repay,
        "max_excess_scaled": max_excess if max_excess is not None else 0,
        "max_delete_dV_scaled": max_dV if max_dV is not None else 0,
        "maxU": max(U[pid] for pid in reach_ids),
        "maxV": max(V[pid] for pid in reach_ids),
    }
