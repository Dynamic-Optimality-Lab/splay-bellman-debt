"""Phase-07 gate (SPEC 07): delta-first mining, exact search, validation, motifs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import zstandard as zstd


def console_log(msg: str) -> None:
    print(msg)


def load_V(n: int) -> dict:
    from pathlib import Path as P
    par = P(r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\parent_upstream_full")
    raw = (par / f"artifacts/potentials/n{n}/hypothesis_bH/V.json.zst").read_bytes()
    arr = json.loads(zstd.ZstdDecompressor().decompress(raw).decode())
    return {str(r["pair_id"]): int(r["V_scaled"]) for r in arr}


def main() -> int:
    # console.log equivalent [WP3-P07-01]: phase07 start
    console_log("[WP3-P07-01] phase07 mining start")
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "python"))
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    from mining.deltas import build_deltas
    from mining.search import exact_search, minimal_inconsistent, motifs
    from structure.features import FEATURE_NAMES
    train = []
    for n in [2, 3, 4, 5]:
        # console.log equivalent [WP3-P07-02]: training deltas
        console_log(f"[WP3-P07-02] training deltas n={n}")
        single = single_table(n)
        reach = build_reachability(n, len(single["trees"]), single)
        feats = json.loads((root / "artifacts" / "v02" / "structure" / f"n{n}.json").read_text())
        fb = {r["state_id"]: r["scalars"] for r in feats["rows"]}
        train += build_deltas(n, fb, load_V(n), len(single["trees"]), single, reach["ids"])
    # console.log equivalent [WP3-P07-03]: exact search (declared domain)
    console_log("[WP3-P07-03] exact search (singles exhaustive + pairs among top-12)")
    from mining.search import exact_search as _es
    res = search_declared(train, len(FEATURE_NAMES))
    # validation on held-out sizes n=6,7 (different graphs, unseen states;
    # streamed scoring — no full delta materialization at n=7 scale)
    valid = {}
    for n in [6, 7]:
        # console.log equivalent [WP3-P07-04]: validation deltas
        console_log(f"[WP3-P07-04] validation n={n}")
        valid[str(n)] = score_streamed(n, root, res["combo"])
    res["validation"] = valid
    res["motifs"] = motifs(train)
    res["inconsistent_repay"] = minimal_inconsistent(train, res["combo"], "repay")
    res["inconsistent_create"] = minimal_inconsistent(train, res["combo"], "create")
    d = root / "artifacts" / "v02" / "debt_atoms"
    d.mkdir(parents=True, exist_ok=True)
    (d / "state_only_search.json").write_text(json.dumps(res, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    (root / "artifacts" / "v02" / "logs" / "phase07_gate.json").write_text(
        json.dumps({"phase": "PHASE-07", "verdict": "DEBT_MINING_COMPLETE",
                    "combo": res["combo"], "validation": valid}, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    # console.log equivalent [WP3-P07-05]: phase07 done
    console_log("[WP3-P07-05] phase07 done")
    return 0


def search_declared(deltas: list[dict], nfeats: int) -> dict:
    import itertools
    # singles exhaustive
    single_cov = []
    for i in range(nfeats):
        for c in (-2, -1, 1, 2):
            combo = ((i, c),)
            cr = sum(1 for r in deltas if r["mode"] == "KEEP" and r["excess"] and sum(cc * r["dF"][ii] for ii, cc in combo) == r["neg_w"])
            cc = sum(1 for r in deltas if r["mode"] == "DELETE" and sum(cc * r["dF"][ii] for ii, cc in combo) == r["dV"])
            single_cov.append((cr + cc, i, c))
    single_cov.sort(reverse=True)
    top = [s[1] for s in single_cov[:12]]
    # console.log equivalent [WP3-P07-06]: declared domain pairs
    console_log(f"[WP3-P07-06] pairs among top-12 features {top}")
    best = None
    tested = 0
    cands = [((i, c),) for i in range(nfeats) for c in (-2, -1, 1, 2)]
    cands += [((i, c1), (j, c2)) for a, i in enumerate(top) for j in top[a + 1:] for c1 in (-2, -1, 1, 2) for c2 in (-2, -1, 1, 2)]
    for combo in cands:
        tested += 1
        cr = sum(1 for r in deltas if r["mode"] == "KEEP" and r["excess"] and sum(cc * r["dF"][ii] for ii, cc in combo) == r["neg_w"])
        cc = sum(1 for r in deltas if r["mode"] == "DELETE" and sum(cc * r["dF"][ii] for ii, cc in combo) == r["dV"])
        score = (cr + cc, cr, cc, -len(combo))
        if best is None or score > best[0]:
            best = (score, combo)
    return {"combo": best[1], "score": best[0], "tested": tested, "domain": "singles-exhaustive + pairs-among-top12"}


def score_streamed(n: int, root, combo: tuple) -> dict:
    import sys
    sys.path.insert(0, str(root / "python"))
    from bellman_debt.splay import single_table
    from bellman_debt.reach import build_reachability
    single = single_table(n)
    reach = build_reachability(n, len(single["trees"]), single)
    feats = json.loads((root / "artifacts" / "v02" / "structure" / f"n{n}.json").read_text())
    fb = {r["state_id"]: r["scalars"] for r in feats["rows"]}
    V = load_V(n)
    C = len(single["trees"])
    table = single["table"]
    cr = tr = cc = tc = 0
    for pid in reach["ids"]:
        a = pid // C
        b = pid % C
        fa = fb[str(pid)]
        for x in range(1, n + 1):
            ra = table[(a, x)]
            rb = table[(b, x)]
            t = ra["after"] * C + rb["after"]
            fb_t = fb[str(t)]
            Ws = rb["cost"] - 2 * ra["cost"]
            if Ws > 0:
                tr += 1
                if sum(c * (fb_t[i] - fa[i]) for i, c in combo) == -Ws:
                    cr += 1
            t2 = ra["after"] * C + b
            tc += 1
            fb2 = fb[str(t2)]
            if sum(c * (fb2[i] - fa[i]) for i, c in combo) == V[str(t2)] - V[str(pid)]:
                cc += 1
    return {"repay": [cr, tr], "create": [cc, tc]}


def score_on(combo: tuple, deltas: list[dict]) -> dict:
    cr = tr = cc = tc = 0
    for r in deltas:
        if r["mode"] == "KEEP" and r["excess"]:
            tr += 1
            if sum(c * r["dF"][i] for i, c in combo) == r["neg_w"]:
                cr += 1
        if r["mode"] == "DELETE":
            tc += 1
            if sum(c * r["dF"][i] for i, c in combo) == r["dV"]:
                cc += 1
    return {"repay": [cr, tr], "create": [cc, tc]}


if __name__ == "__main__":
    raise SystemExit(main())
