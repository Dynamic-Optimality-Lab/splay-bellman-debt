# theorem_BD5_source_compatible_bisimulation_transports_U.md — BD0-05 (U transport)

**Obligation:** BD0-05 — compatible source treatment transports `U_b`.
**Status:** REVIEWED (lifecycle UNPROVED → PROVED → REVIEWED closed during WP-3 theorem closure; see `math/proof_status.json`).
**Scope:** frozen pair-state system, fixed `n`, fixed feasible `b`, full
diagonal source set `Δ_n` per the frozen multi-source contract.
No finite table is a premise.

## Definitions

- Edge slack `ℓ_b(e)=b·a(e)−y(e)=−w_b(e)` and
  `U_b(s)=inf_{P:Δ_n⇝s} Σℓ_b(e)` with `U_b(d)=0` on sources per BD0-03.
- A relation/quotient used for `U`-transport must be **source
  compatible**, meaning all of:
  1. diagonal/source membership is represented compatibly: related
     states agree on source membership, or the quotient carries an
     explicit quotient-source set with a well-defined membership rule;
  2. the source boundary value `U=0` is preserved across the relation;
  3. every source-rooted path to `s` maps to a source-rooted path to
     `t` with identical `ℓ_b` sequence and total slack;
  4. the reverse path correspondence also holds;
  5. source merging does not manufacture an artificial cheaper history
     (no new source-rooted path class with smaller total appears
     through the quotient map);
  6. source splitting does not destroy a legitimate history (every
     attaining or approximating history survives the map).
- If the quotient semantics require a quotient-source set rather than
  pairwise source equivalence, that set and its membership rule must be
  formalized exactly before any transport claim.

## Why future bisimulation alone is insufficient

A deterministic future bisimulation (BD0-04 hypotheses) constrains
outgoing transitions, costs, and successor classes. `U_b` is an
infimum over *incoming* diagonal-rooted histories. Two states can share
identical futures while having disjoint pasts (different cheapest
source-rooted slacks). Hence future bisimilarity preserves `V_b` but
does **not** automatically preserve `U_b`. Source treatment is an
additional hypothesis, which is why BD0-04 and BD0-05 are separate
obligations.

## Lemma (source-rooted path correspondence)

Under hypotheses 1–6, if `s` and `t` are related compatibly, then for
every source-rooted `P:Δ_n⇝s` there exists source-rooted
`Q:Δ_n⇝t` with identical `ℓ_b` totals, and vice versa.

*Proof.* By hypotheses 3–4 applied edge by edge along the path, with
hypotheses 1–2 anchoring the source endpoint at value `0`; hypotheses
5–6 guarantee the mapped families are exactly the source-rooted
families (no creation, no loss). ∎

## Theorem (U transport)

Under the compatible-source condition, for every fixed feasible `b`
(BD0-03 finiteness conditions):

```text
U_b(s) = U_b(t)
```

*Proof.* The Lemma gives slack-preserving correspondence between the
two source-rooted path families in both directions; hence the
attainable slack sets coincide and their infima coincide. ∎

## Cycle / infinity semantics

Since `ℓ_b=−w_b`, a diagonal-rooted reachable negative-slack cycle is
a positive-regret cycle. If one exists, both infima are `−∞` together
(the cycle maps with identical totals), understood in the extended
sense per BD0-03. No finite `U` table is assigned in that case.

## Review record

- PROVED: 2026-09-22, prover Muse Spark (implementation agent), WP-3 theorem closure.
- REVIEWED: 2026-09-22, independent check `tests/kernel/test_bd004_bd005_transport.py` + `python/audit/review_bd004_bd005.py` — green.
- Gate: quotient `U`-transport claims require this REVIEWED status **plus**
  a verified source-compatibility record for the quotient in use.
