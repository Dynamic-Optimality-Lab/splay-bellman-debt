"""Adversarial families + exact-residual harness (campaign gated on survivors).

Families (state-only): spines, opposite spines, zig-zag, balanced-vs-spine,
root splits, nested disagreements, rank-gap extremes, mirrors, random Catalan,
DELETE-diverged histories, inflated extremal motifs.
Recency adds: max divergence, X-only bursts, same-tree/different-recency,
deep nonadjacent violations, alternating histories, deletion bursts + one KEEP.
Engines (uniform/structured/hill-climb/annealing/genetic/motif-inflation/
rotation-neighborhood/generalizer) propose; the exact evaluator disposes.
A campaign runs only for development survivors; with zero survivors the
campaign status is NOT_ACTIVATED (recorded, never skipped silently).
"""
from __future__ import annotations


def console_log(msg: str) -> None:
    print(msg)


STATE_FAMILIES = ["spine", "opp_spine", "zigzag", "balanced_vs_spine", "root_split",
                  "nested_disagree", "rank_gap", "mirror", "random_catalan",
                  "delete_diverged", "motif_inflation"]
RECENCY_FAMILIES = STATE_FAMILIES + ["max_divergence", "x_only_burst", "same_tree_diff_recency",
                                     "deep_violation", "alternating_histories", "burst_then_keep"]


def campaign_status(survivors: list) -> dict:
    # console.log equivalent [WP5-ADV-01]: campaign gate
    console_log(f"[WP5-ADV-01] adversary campaign gate survivors={len(survivors)}")
    if not survivors:
        return {"status": "NOT_ACTIVATED", "reason": "zero development survivors; nothing to attack"}
    return {"status": "REQUIRED", "targets": survivors}
