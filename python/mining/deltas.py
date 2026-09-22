"""Delta-first datasets: ΔF per edge vs DELETE ΔV_2 / KEEP −w_2 / V-tight equality.

Training selection per prereg/discovery_splits.yaml: n=2..5 discovery rows;
validation n=6..7 held within development (never n8/H1). Joined to Bellman
targets only here (post-freeze); extraction never saw targets.
"""
from __future__ import annotations


def console_log(msg: str) -> None:
    print(msg)


def build_deltas(n: int, feat_by_state: dict, V: dict, tree_count: int, single: dict, reach_ids: list[int]) -> list[dict]:
    # console.log equivalent [WP3-DELTA-01]: deltas start
    console_log(f"[WP3-DELTA-01] deltas n={n} start")
    table = single["table"]
    rows = []
    for pid in reach_ids:
        a = pid // tree_count
        b = pid % tree_count
        fa = feat_by_state[str(pid)]
        for x in range(1, n + 1):
            ra = table[(a, x)]
            rb = table[(b, x)]
            ca, cb = ra["cost"], rb["cost"]
            # KEEP edge
            t = ra["after"] * tree_count + rb["after"]
            fb = feat_by_state[str(t)]
            dF = [y - z for y, z in zip(fb, fa)]
            Ws = cb - 2 * ca
            rows.append({"n": n, "mode": "KEEP", "key": x, "source": pid, "target": t,
                         "dF": dF, "neg_w": -Ws, "dV": V[str(t)] - V[str(pid)],
                         "vtight": (Ws + (V[str(t)] - V[str(pid)]) == 0), "excess": Ws > 0})
            # DELETE edge
            t2 = ra["after"] * tree_count + b
            fb2 = feat_by_state[str(t2)]
            dF2 = [y - z for y, z in zip(fb2, fa)]
            rows.append({"n": n, "mode": "DELETE", "key": x, "source": pid, "target": t2,
                         "dF": dF2, "neg_w": 2 * ca, "dV": V[str(t2)] - V[str(pid)],
                         "vtight": (-2 * ca + (V[str(t2)] - V[str(pid)]) == 0), "excess": False})
    # console.log equivalent [WP3-DELTA-02]: deltas done
    console_log(f"[WP3-DELTA-02] deltas n={n} done rows={len(rows)}")
    return rows
