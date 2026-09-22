# theorem_BD3_past_slack.md — BD0-03 (U past-slack / predecessor recursion)

**Obligation:** BD0-03 — `U_b` equals minimum past slack and satisfies predecessor Bellman recursion.
**Status:** REVIEWED (lifecycle UNPROVED → PROVED → REVIEWED closed during WP-2 theorem closure; see `math/proof_status.json`).
**Scope:** frozen pair-state transition system, fixed `n`, fixed rational `b`,
full diagonal source set `Δ_n` per the frozen contract.
No finite computation is used as a premise.

## Definitions

- Legal pair states: reachable domain `R_n`; diagonal source set
  `Δ_n = {(T,T)}` (all synchronized pairs), multi-source convention.
- Legal edges as in BD0-02. Edge slack
  `ℓ_b(e) = b·a(e) − y(e) = −w_b(e)`; scaling `L_{p,q}=p·a−q·y`.
- A diagonal-rooted history reaching `t`, written `P:Δ_n⇝t`, is a finite
  directed path of legal edges from some `d ∈ Δ_n` to `t`. States with
  no diagonal-rooted path are outside the reachable domain and out of scope.
- `U_b(t) = inf_{P:Δ_n⇝t} Σ_{e∈P} ℓ_b(e)`. The infimum is over finite
  legal histories; it may be `−∞` if negatively unbounded (see below).

## Source boundary (exact)

Under the frozen multi-source convention, for every diagonal source state:

```text
U_b(d) = 0
```

The empty history at `d` has value `0`, and no history can beat it once
feasibility excludes negative-slack cycles reachable on diagonal-rooted
paths (see finiteness section); the implementation initializes
diagonals to `0` exactly on this basis. Any deviation from this
convention would require a separately versioned contract.

## Lemma (path decomposition)

For non-source `t`, every legal diagonal-rooted path ending at `t`
decomposes uniquely as a diagonal-rooted path to some `s` plus a last
legal edge `e:s→t`:

```text
P:Δ_n⇝s  +  e:s→t   (value Σ_P ℓ + ℓ_b(e))
```

*Proof.* A path of length ≥1 ending at `t` has a unique final edge;
removing it leaves a diagonal-rooted path to its source. Length-zero
paths occur only at source states, covered by the boundary. ∎

## Theorem (predecessor recursion)

Assume all relevant infima are finite (feasible case below). Then for
non-source `t`:

```text
U_b(t) = min_{e:s→t} [U_b(s) + ℓ_b(e)]
```

with `U_b(d)=0` on sources.

*Proof.* Partition histories by their last edge (Lemma). For fixed last
edge `e:s→t`, `inf_{P:Δ⇝s}[Σ_P ℓ + ℓ_b(e)] = (inf_{P:Δ⇝s} Σ_P ℓ) + ℓ_b(e)
= U_b(s)+ℓ_b(e)` since `ℓ_b(e)` is constant for the class. Taking infima
over the finitely many incoming-edge classes gives the minimum. ∎

## Cycle / finiteness obligation

Since `ℓ_b = −w_b`, a reachable negative-slack cycle is exactly a
positive-regret cycle.

- If a diagonal-rooted reachable cycle has total slack `< 0`,
  repetition drives histories to `−∞`, so the infimum is `−∞` and no
  finite `U_b` table may be claimed.
- Finite `U_b` geometry therefore requires fixed-`b` feasibility: no
  reachable negative-slack cycle on diagonal-rooted paths in the
  relevant domain (the same feasibility condition as BD0-02, dual side).
- Finite feasible-`b` tables (e.g. certified `b=2`) are verification
  targets, never proof premises.

## Semantic conclusion

`U_b(t)` is exactly:

> the minimum accumulated `b`-slack among legal diagonal-rooted
> histories reaching `t`.

No stronger wording is claimed here. In particular, this note does not
call `U_b` the "maximum creation budget" — that operational gloss
belongs to the feasible-potential corridor and requires the separate
derivation recorded in BD0-02's corollary section.

## Corridor corollary (past half; joint statement in BD0-02)

Let `H` satisfy the BD0-02 corollary assumptions (`H ≥ 0`, `H(d)=0`,
`H(t)−H(s) ≤ ℓ_b(e)`). For any diagonal-rooted `P:Δ_n⇝s` with edges
`e_1...e_k`, summation gives `H(s)−H(d) ≤ Σℓ_b(e_i)`, i.e.
`H(s) ≤ Σℓ_b(e_i)` using `H(d)=0`. Taking infima over `P` yields
`H(s) ≤ U_b(s)`. Combined with BD0-02's future side:

```text
V_b(s) ≤ H(s) ≤ U_b(s)
```

Valid only under the exact normalized nonnegative pair-state
assumptions. Never extended to arbitrary augmented potentials (BD0-13).

## Review record

- PROVED: 2026-09-22, prover Muse Spark (implementation agent), WP-2 theorem closure.
- REVIEWED: 2026-09-22, independent check `tests/bellman/test_bd002_bd003_semantics.py` — green.
- Gate: WP-3 semantic debt mining requires this REVIEWED status.
