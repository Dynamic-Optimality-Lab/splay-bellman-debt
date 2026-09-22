"""Read-only parent import: fact table from sealed summaries (never recomputed-as-parent)."""
from __future__ import annotations

import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


PARENT = Path(r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\parent_upstream_full")

EXPECTED_R = {2: 4, 3: 19, 4: 196, 5: 1764, 6: 17424, 7: 184041}
EXPECTED_B = {2: (1, 1), 3: (1, 1), 4: (3, 2), 5: (8, 5), 6: (8, 5), 7: (23, 14)}
EXPECTED_MAXU = {2: 4, 3: 10, 4: 22, 5: 38, 6: 44, 7: 58}
EXPECTED_MAXV = {2: 0, 3: 1, 4: 2, 5: 3, 6: 5, 7: 6}
EXPECTED_FORCED = {2: 2, 3: 5, 4: 14, 5: 42, 6: 132, 7: 429}


def load_parent_fact_row(n: int) -> dict:
    cert = json.loads((PARENT / f"artifacts/certificates/n{n}/bn_certificate.json").read_text())
    summ = json.loads((PARENT / f"artifacts/potentials/n{n}/hypothesis_bH/summary.json").read_text())
    return {
        "n": n,
        "R": cert["reachable_pair_count"],
        "b": (cert["b"]["p"], cert["b"]["q"]),
        "maxU": int(summ["max_U"]),
        "maxV": int(summ["max_V"]),
        "forced": int(summ["forced_count"]),
    }


def build_fact_table(ns: list[int]) -> list[dict]:
    # console.log equivalent [WP2-IMP-01]: fact table start
    console_log(f"[WP2-IMP-01] fact table start ns={ns}")
    rows = []
    for n in ns:
        r = load_parent_fact_row(n)
        r["R_match"] = (r["R"] == EXPECTED_R[n])
        r["b_match"] = ((str(r["b"][0]), str(r["b"][1])) == (str(EXPECTED_B[n][0]), str(EXPECTED_B[n][1])))
        r["maxU_match"] = (r["maxU"] == EXPECTED_MAXU[n])
        r["maxV_match"] = (r["maxV"] == EXPECTED_MAXV[n])
        r["forced_match"] = (r["forced"] == EXPECTED_FORCED[n])
        rows.append(r)
    # console.log equivalent [WP2-IMP-02]: fact table done
    console_log(f"[WP2-IMP-02] fact table done rows={len(rows)}")
    return rows
