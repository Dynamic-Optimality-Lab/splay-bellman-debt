"""ERA-BD-A candidate synthesis: frozen versioned universal debt laws.

Each PHI-* freezes: definition, track, b_H (one, n-independent),
tie rules, normalization, ontology version, range claim, proof outline.
Any change creates a new ID. May use all development evidence; may not
use detailed n8/H1/H2R/future counterexamples (none touched here).
"""
from __future__ import annotations

import json
from pathlib import Path

from structure.recency_features import recency_features


def console_log(msg: str) -> None:
    print(msg)


CANDIDATES = [
    {
        "hypothesis_id": "PHI-0001",
        "parent_hypothesis": None,
        "track": "STATE_ONLY",
        "definition": "Phi(A,B) = sum_k |depth_A(k) - depth_B(k)| (depth_sum_abs, F-depth atom)",
        "b_hypothesis": {"p": "2", "q": "1"},
        "ontology_version": "ONTOLOGY-v0.2",
        "tie_rules": "none required (symmetric sums)",
        "normalization": "Phi(T,T)=0 by zero differences",
        "range_claim": "RANGE_UNKNOWN (finite maxima recorded, no asymptotic claim)",
        "proof_outline": "none (falsification stage)",
        "uses_recency": False,
        "uses_history_beyond_recency": False,
        "uses_UV_lookup": False,
        "n_specific_parameters": False,
        "status": "FALSIFICATION_PENDING",
    },
    {
        "hypothesis_id": "PHI-0002",
        "parent_hypothesis": None,
        "track": "STATE_ONLY",
        "definition": "Phi(A,B) = sum_k |size_A(k) - size_B(k)| (size_sum_abs, F-subtree atom)",
        "b_hypothesis": {"p": "2", "q": "1"},
        "ontology_version": "ONTOLOGY-v0.2",
        "tie_rules": "none required (symmetric sums)",
        "normalization": "Phi(T,T)=0 by zero differences",
        "range_claim": "RANGE_UNKNOWN (finite maxima recorded, no asymptotic claim)",
        "proof_outline": "none (falsification stage)",
        "uses_recency": False,
        "uses_history_beyond_recency": False,
        "uses_UV_lookup": False,
        "n_specific_parameters": False,
        "status": "FALSIFICATION_PENDING",
    },
    {
        "hypothesis_id": "PHI-0003",
        "parent_hypothesis": None,
        "track": "RECENCY_AUGMENTED",
        "definition": "Phi(z) = heap_viol_AX + heap_viol_BY + anc_viol_AX + anc_viol_BY (directed recency-violation charges D1/D2)",
        "b_hypothesis": {"p": "2", "q": "1"},
        "ontology_version": "ONTOLOGY-v0.2",
        "tie_rules": "TIE_EXPLICIT (unseen pairs unresolved, counted 0)",
        "normalization": "Phi(T,T,[],[])=0 (all pairs unresolved at empty recency)",
        "range_claim": "RANGE_UNKNOWN (finite maxima recorded, no asymptotic claim)",
        "proof_outline": "none (falsification stage)",
        "uses_recency": True,
        "uses_history_beyond_recency": False,
        "uses_UV_lookup": False,
        "n_specific_parameters": False,
        "status": "FALSIFICATION_PENDING",
    },
]


def phi_value(hid: str, n: int, A: dict, B: dict, rx: tuple = (), ry: tuple = ()) -> int:
    # Exact integer evaluation from frozen math text (shared by primary evaluator).
    if hid == "PHI-0001":
        return sum(abs(A["depth"][k] - B["depth"][k]) for k in range(1, n + 1))
    if hid == "PHI-0002":
        return sum(abs(A["size"][k] - B["size"][k]) for k in range(1, n + 1))
    if hid == "PHI-0003":
        f = recency_features(n, A, B, rx, ry)
        return f["heap_viol_AX"] + f["heap_viol_BY"] + f["anc_viol_AX"] + f["anc_viol_BY"]
    raise ValueError(hid)


def freeze(repo_root: Path) -> list[dict]:
    # console.log equivalent [WP5-SYN-01]: synthesis freeze
    console_log("[WP5-SYN-01] ERA-BD-A freeze (3 candidates, dev evidence only)")
    d = repo_root / "artifacts" / "v02" / "hypotheses"
    d.mkdir(parents=True, exist_ok=True)
    for c in CANDIDATES:
        (d / f"{c['hypothesis_id']}.json").write_text(
            json.dumps(c, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (d / f"{c['hypothesis_id']}.eval_contract.json").write_text(
            json.dumps({"hypothesis_id": c["hypothesis_id"],
                        "b_hypothesis": c["b_hypothesis"],
                        "b_is_universal_candidate": True,
                        "branch": "RATIONAL"}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP5-SYN-02]: freeze done
    console_log("[WP5-SYN-02] freeze done")
    return CANDIDATES
