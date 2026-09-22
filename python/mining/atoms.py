"""Recency-augmented debt atoms D1-D9 + creation/repayment screens + scale audit.

Atoms: per-node/per-edge sums, recency-violation charges, nested/crossing
charges, rank-derived charges, heavy/gap/inversion-mapped charges (new IDs),
bounded multiscale charges (O(1) per object), and finite combinations.
Eligibility: tree/recency-theoretic def, exact eval, relabel semantics,
local support, per-object charge bound. Black-box nets, lookup tables and
unrestricted regression are excluded by construction.
"""
from __future__ import annotations


def console_log(msg: str) -> None:
    print(msg)


def atom_vector(kind: str, n: int, A: dict, B: dict, rx: tuple, ry: tuple) -> dict:
    # Returns per-state atom values for one family (exact integers).
    from structure.recency_features import recency_features
    rf = recency_features(n, A, B, rx, ry)
    if kind == "D1_node":
        return {"v": rf["heap_viol_AX"] + rf["heap_viol_BY"], "bound": 2 * (n - 1)}
    if kind == "D2_edge":
        return {"v": rf["anc_viol_AX"] + rf["anc_viol_BY"], "bound": 2 * n * n}
    if kind == "D3_recency":
        return {"v": rf["rho_disagree"] + rf["x_only_seen"], "bound": n * n}
    if kind == "D4_nested":
        return {"v": rf["rec_cross"] + rf["common_prefix"], "bound": 2 * n}
    if kind == "D5_rank":
        return {"v": rf["age_diff_sum"], "bound": 2 * n * n}
    if kind == "D6_mapped":
        return {"v": rf["RECENCY_INV_dis"], "bound": n * n}
    if kind == "D7_multiscale":
        return {"v": (rf["heap_unres_AX"] + rf["heap_unres_BY"]) // 1, "bound": 2 * n}
    raise ValueError(kind)


ATOM_KINDS = ["D1_node", "D2_edge", "D3_recency", "D4_nested", "D5_rank", "D6_mapped", "D7_multiscale"]


def screen_creation(delats: list[dict], bound_multiple: int = 1) -> list[dict]:
    # Flag CHEAP_DELETE_LARGE_ATOM_JUMP: |Δatom| >> c_A without cancellation.
    flags = []
    for r in delats:
        if r["mode"] == "DELETE" and abs(r["dAtom"]) > bound_multiple * r["a"] and r["a"] <= 2:
            flags.append({**r, "flag": "CHEAP_DELETE_LARGE_ATOM_JUMP"})
    return flags


def scale_audit(values_by_n: dict) -> dict:
    return {n: {"max": max(v), "min": min(v), "note": "finite observation only; no asymptotic inference"} for n, v in values_by_n.items()}
