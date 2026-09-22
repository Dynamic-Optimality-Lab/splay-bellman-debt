# theorem_BD13_pair_corridor_scope.md — BD0-13 (pair corridor does not bind augmented potentials)

**Obligation:** BD0-13 — pair-state corridor `V_b ≤ H ≤ U_b` does not constrain arbitrary augmented-state potentials.
**Status:** REVIEWED (lifecycle UNPROVED → PROVED → REVIEWED closed during WP-4 theorem seal; see `math/proof_status.json`).
**Scope:** scope / non-implication theorem about the BD0-02/BD0-03 corridor corollary.
Proves only that the pair-state theorem cannot legally reject arbitrary augmented candidates.
No construction of any out-of-corridor feasible potential is claimed.

## Definitions

- Pair-state potential `H:R_n → ℝ` in the corridor hypothesis class:
  domain is the pair-state graph; normalized diagonal treatment
  (`H(d)=0` on sources); nonnegativity (`H ≥ 0`); pair-state edge
  inequalities (`H(t)−H(s) ≤ ℓ_b(e)` on every legal pair edge);
  one value `H(A,B)` per pair state.
- Augmented potential `Φ` on `(A,B,ρ_X,ρ_Y)`: a function of the
  augmented state; not, merely by existing, a function on `R_n`.
- Projection `π(A,B,ρ_X,ρ_Y)=(A,B)`.

## Theorem (scope)

The pair-state corridor theorem:

```text
V_b(A,B) ≤ H(A,B) ≤ U_b(A,B)
```

applies only to functions in its hypothesis class above. An arbitrary
augmented potential `Φ(A,B,ρ_X,ρ_Y)` is not in that class merely by
existing. Therefore the pair-state theorem alone does NOT imply:

```text
V_b(A,B) ≤ Φ(A,B,ρ_X,ρ_Y) ≤ U_b(A,B)
```

for arbitrary augmented `Φ` and arbitrary recency.

*Proof.* The corridor proof (BD0-02 upper half, BD0-03 past half) sums
edge inequalities along pair-state paths and uses the normalization
`H(d)=0`, `H ≥ 0` at every step. Each step requires the function under
test to assign one value per pair state satisfying the pair-edge
inequalities. An augmented `Φ` assigns values per augmented state; its
restriction to a projection fiber need not be constant, and no
hypothesis equates fiber values. Without an additional
lifting/projection theorem placing `Φ` in the hypothesis class, the
corridor derivation does not go through. Hence no rejection of `Φ(z)`
for violating `V_b(A,B)`/`U_b(A,B)` follows from the pair theorem. ∎

## What is NOT claimed

- No claim that a valid augmented Splay potential outside the
  pair-state corridor necessarily exists (no such example is
  constructed or proved here).
- No claim that recency is necessary for any universal proof.
- No claim that an augmented `Φ` may violate the corridor while
  remaining feasible (that would require a separate construction).

## Required distinction

`H(A,B)` (pair-state potential) and `Φ(A,B,ρ_X,ρ_Y)` (augmented
potential) are different mathematical objects with different domains.
Further, `V_b^R` being constant on projection fibers (BD0-15) does NOT
imply every valid augmented `Φ` is constant on fibers: BD0-15 is
recency blindness of canonical future value `V`, not recency blindness
of every possible accounting potential. Misusing BD0-15 as
"`Φ` is recency-blind" is explicitly forbidden.

## Consequence for WP-5

The WP-5 candidate evaluator is barred from applying pair `U_b`/`V_b`
envelopes as a rejection gate to Track-R candidates unless an explicit
lifting theorem allows it. Track-S candidates (pair-state domain) may
still use their own-`b_H` corridor precheck per the candidate contract.

## Review record

- PROVED: 2026-09-22, prover Muse Spark (implementation agent), WP-4 theorem seal.
- REVIEWED: 2026-09-22, independent check `tests/test_bd013_corridor_scope.py` + `python/audit/review_bd013.py` — green.
- Gate: WP-5 Track-R evaluation requires this REVIEWED status.
