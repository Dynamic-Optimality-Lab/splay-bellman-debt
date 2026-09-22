# theorem_BD4_bisimulation_transports_V.md — BD0-04 (V transport)

**Obligation:** BD0-04 — deterministic cost-preserving bisimulation transports `V_b`.
**Status:** REVIEWED (lifecycle UNPROVED → PROVED → REVIEWED closed during WP-3 theorem closure; see `math/proof_status.json`).
**Scope:** frozen deterministic pair-state transition system, fixed `n`, fixed feasible `b`.
No finite table, quotient class, or empirical observation is a premise.

## Definitions

- Legal states, actions `(KEEP,x)` / `(DELETE,x)`, costs `a=c(A,x)`,
  `y=c(B,x)` (KEEP) / `y=0` (DELETE), regret `w_b(e)=y−b·a`,
  and `V_b(s)=sup_{P:s⇝*} Σw_b(e)` (empty continuation allowed) per BD0-02.
- An equivalence relation `~` on states is a **cost-preserving
  deterministic bisimulation** when, for all `s~t` and every action
  `α=(mode,x)`:
  1. `α` is enabled at `s` iff enabled at `t` (here: always);
  2. action correspondence is the identity on `(mode,x)`;
  3. immediate costs agree: `a_s(α)=a_t(α)`, `y_s(α)=y_t(α)`;
  4. hence immediate regret agrees: `w_b(e_s)=w_b(e_t)`;
  5. successor equivalence: if `α` sends `s→s'` and `t→t'`,
     then `s'~t'`;
  6. the correspondence is symmetric (`~` is an equivalence).

## Lemma (continuation correspondence)

If `s~t`, then for every finite legal continuation
`P=(α_1...α_k)` from `s` with successors `s=s_0→s_1→...→s_k`,
the same action sequence from `t` is legal with successors
`t=t_0→t_1→...→t_k`, satisfies `s_i~t_i` for all `i`, and carries
identical immediate values `w_b(e_i^s)=w_b(e_i^t)` and hence identical
cumulative regret `Σw_b`.

*Proof.* By induction on `k`. Base `k=0` is the empty continuation
(value `0` both sides). Step: hypotheses 1–4 give the same first edge
weight; hypothesis 5 gives `s_1~t_1`; the induction hypothesis applied
from there gives the suffix correspondence. ∎

## Theorem (V transport)

If `s~t` under a cost-preserving deterministic bisimulation, then for
every fixed feasible `b` (BD0-02 finiteness conditions):

```text
V_b(s) = V_b(t)
```

*Proof.* The Lemma gives a regret-preserving bijection between finite
continuations from `s` and from `t` (apply in both directions using
symmetry, hypothesis 6). Hence the attainable future-regret sets
coincide, and their suprema coincide. Under feasibility both values
are finite and the equality is exact. ∎

## Cycle / infinity semantics

If a reachable positive-regret cycle exists, both `V_b(s)` and
`V_b(t)` are `+∞` together: the cycle maps across the bisimulation
with identical totals, so unboundedness transfers. The equality is
then understood in the extended value sense. No finite table is
assigned in the infeasible case; no silent finite value is used.

## Required non-converse

Only `bisimilar ⇒ equal V_b` is claimed. The converse
(`equal V_b ⇒ bisimilar`) is NOT claimed and is false in general:
states with equal future regret need not share action/cost/successor
structure. Likewise, behavioral equivalence must not be conflated with
feature-kernel equality unless the kernel has been proven to induce a
relation satisfying hypotheses 1–6 above.

## Review record

- PROVED: 2026-09-22, prover Muse Spark (implementation agent), WP-3 theorem closure.
- REVIEWED: 2026-09-22, independent check `tests/kernel/test_bd004_bd005_transport.py` + `python/audit/review_bd004_bd005.py` — green.
- Gate: quotient V-transport claims require this REVIEWED status.
