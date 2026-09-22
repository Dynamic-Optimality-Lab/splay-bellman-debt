# theorem_BD2_bellman_debt.md — BD0-02 (V future-regret / Bellman recursion)

**Obligation:** BD0-02 — `V_b` equals maximum future regret and satisfies Bellman recursion.
**Status:** REVIEWED (lifecycle UNPROVED → PROVED → REVIEWED closed during WP-2 theorem closure; see `math/proof_status.json`).
**Scope:** frozen pair-state transition system, fixed `n`, fixed rational `b`.
No finite computation is used as a premise. No claim about universal closed-form potentials.

## Definitions

- Legal pair states: reachable domain `R_n` (diagonal-reachable pairs).
- Legal edges `e:s→t`: all `(KEEP,x)` / `(DELETE,x)` for `x ∈ [n]`,
  with `K_x(A,B)=(S_xA,S_xB)` and `D_x(A,B)=(S_xA,B)`.
- Edge regret `w_b(e) = y(e) − b·a(e)`, where `a=c(A,x)`, `y=c(B,x)` on
  KEEP and `y=0` on DELETE. Integer scaling `L_{p,q}(e)=p·a−q·y`.
- A future continuation from `s`, written `P:s⇝*`, is a finite directed
  path of legal edges starting at `s`, **including the empty path**
  (zero edges, value `0` by definition).
- `V_b(s) = sup_{P:s⇝*} Σ_{e∈P} w_b(e)`, where the supremum is over all
  finite legal continuations. The value may be `+∞` if suprema are
  unbounded (see finiteness section).

## Lemma (path decomposition)

Every legal future continuation from `s` is exactly one of:

1. the empty continuation, with value `0`;
2. a first legal edge `e:s→t` followed by a legal continuation
   `P':t⇝*` (possibly empty), with value `w_b(e) + Σ_{e'∈P'} w_b(e')`.

*Proof.* By definition of a finite path: either it has length zero
(case 1) or length ≥1, in which case removing the first edge leaves a
finite legal path from its target (case 2). The decomposition is unique
given the first edge. ∎

## Theorem (Bellman recursion)

Assume `V_b(t)` is finite for every successor `t` of `s` and the
per-state suprema are attained or approached within finite paths
(the feasible case characterized below). Then:

```text
V_b(s) = max(0, max_{e:s→t} [w_b(e) + V_b(t)])
```

*Proof.* Apply the Lemma inside the supremum. The family of path values
splits into `{0}` (empty path) and, for each first edge `e:s→t`, the
family `{w_b(e) + val(P') : P':t⇝*}`. Taking suprema:
`sup_{P'} [w_b(e)+val(P')] = w_b(e) + sup_{P'} val(P') = w_b(e)+V_b(t)`
since `w_b(e)` is constant for fixed first edge. Then
`sup` over the union equals `max(0, max_e [w_b(e)+V_b(t)])`; the outer
`max` with `0` is the empty continuation, and the inner `max` is over
the finite action set (`2n` edges), hence a maximum. ∎

## Cycle / finiteness obligation

The finite graph may contain directed cycles. Let `C` be a directed
cycle reachable from `s` with total regret `W(C)=Σ_{e∈C} w_b(e)`.

- If some reachable cycle has `W(C) > 0`, then repeating it `k` times
  yields continuations of value `k·W(C) + const → +∞`, so
  `V_b(s) = +∞`. No finite Bellman value may be claimed in this case.
- Hence a finite `V_b` geometry exists **only** for feasible fixed `b`,
  defined by the difference-constraint feasibility condition: no
  reachable positive-total-`w_b` cycle in the relevant domain
  (equivalently, the system `V(t)−V(s) ≤ ℓ_b(e)`, `V ≥ 0` is feasible).
  Under feasibility, every `V_b(s)` is finite and the recursion above
  holds with genuine maxima.
- Finite feasible-`b` geometry (e.g. the certified `b=2` tables used as
  discovery targets) must be distinguished from arbitrary `b`: for
  infeasible `b` the implementation records infeasibility and claims
  no finite `V_b` table.

In particular, WP-2's finite `b=2` tables are **evidence that the
solver's inequalities verify**, never a premise of this theorem.

## Semantic conclusion

`V_b(s)` is exactly:

> the maximum future `b`-regret extractable from state `s` under the
> frozen legal pair-state dynamics.

`V_b` is a canonical finite-state value function. It is **not** claimed
to be a universal closed-form Splay potential.

## Corridor corollary (upper half + statement of lower half)

Let `H` be a normalized feasible pair-state potential: `H ≥ 0`,
`H(d)=0` on diagonal source states, and `H(t)−H(s) ≤ ℓ_b(e)` on every
legal edge (equivalently `w_b(e)+H(t)−H(s) ≤ 0`).

- Future side (`V_b ≤ H`, proved here): for any `s` and any finite
  continuation `P:s⇝*` with edges `e_1...e_k`, summing the edge
  constraints telescopes to `H(t_k)−H(s) ≤ −Σw_b(e_i)`, i.e.
  `Σw_b(e_i) ≤ H(s)−H(t_k) ≤ H(s)` using `H ≥ 0`. Taking suprema over
  `P` (empty path gives `0 ≤ H(s)`) yields `V_b(s) ≤ H(s)`.
- Past side (`H ≤ U_b`): proved in `math/theorem_BD3_past_slack.md`
  by summing along diagonal-rooted paths with `H(d)=0`.

Hence, under exactly these pair-state normalization assumptions:

```text
V_b(s) ≤ H(s) ≤ U_b(s)
```

This corollary is **not** extended to arbitrary recency-augmented
potentials; BD0-13 exists precisely to prevent that mistake.

## Review record

- PROVED: 2026-09-22, prover Muse Spark (implementation agent), WP-2 theorem closure.
- REVIEWED: 2026-09-22, independent check `tests/bellman/test_bd002_bd003_semantics.py` (definition, empty path, decomposition, recurrence, finiteness, no-forced-finite-V, semantics, no-universal-potential claim, corridor assumptions) — green.
- Gate: WP-3 semantic debt mining requires this REVIEWED status.
