# theorem_BD9_recency_v_blindness.md — SA-01 one-way blindness (BD0-15)

**Obligation:** BD0-15 — same-`(A,B)` implies equal augmented `V_b^R`.
**Status:** REVIEWED (lifecycle UNPROVED → PROVED → REVIEWED closed during WP-1 reseal; see `math/proof_status.json`).
**Scope:** all `n`, all fixed feasible `b`, augmented track `z=(A,B,rho_X,rho_Y)` per section 6 contract.

## Theorem statement

Let augmented states be `z=(A,B,rho_X,rho_Y)` with projection `pi(z)=(A,B)`.
Define `z_1 R_pi z_2 iff pi(z_1)=pi(z_2)`. Then `R_pi` is a
cost-preserving deterministic bisimulation for the augmented paired-Splay
transition system in the one-way sense: `pi(z_1)=pi(z_2)` implies `z_1`
and `z_2` expose identical future edge-regret options. Consequently for
every fixed feasible `b`:

```text
V_b^R(A,B,rho_X,rho_Y) = V_b^R(A,B,rho_X',rho_Y')
```

Only `same-(A,B) => bisimilar` is claimed. No converse is claimed:
different `(A,B)` states may still be behaviorally equivalent, which is
what the behavioral-quotient machinery investigates.

## Precise state/action/cost definitions relied upon

- Augmented state `z=(A,B,rho_X,rho_Y)`; `rho_X`, `rho_Y` are relative
  most-recent-access orders (section 6); unseen keys are the complement.
- Action alphabet in every augmented state: `(KEEP,x)` and `(DELETE,x)`
  for `x` in `[n]`; every action is enabled in every state.
- KEEP `x`: `A -> S_x(A)`, `B -> S_x(B)`, `rho_X -> update(rho_X,x)`,
  `rho_Y -> update(rho_Y,x)`; costs `a=c(A,x)`, `y=c(B,x)`.
- DELETE `x`: `A -> S_x(A)`, `B -> B`, `rho_X -> update(rho_X,x)`,
  `rho_Y -> rho_Y`; costs `a=c(A,x)`, `y=0`.
- Edge regret `w_b(e)=y-b*a`; integer scaling `L_{p,q}=p*a-q*y`.
- Canonical future regret `V_b^R(s)=sup_{P:s~>*} sum w_b(e)` with the
  empty continuation allowed, satisfying
  `V_b(s)=max(0,max_e[w_b(e)+V_b(t)])` on the finite valid geometry.

## Proof

Fix `(A,B)` and two recency pairs `(rho_X,rho_Y)`, `(rho_X',rho_Y')`.
Let `z_1=(A,B,rho_X,rho_Y)` and `z_2=(A,B,rho_X',rho_Y')`, so
`z_1 R_pi z_2`.

1. Same action alphabet: both states expose `(KEEP,x)` and `(DELETE,x)`
   for all `x`; enabled actions do not depend on recency.
2. `c(A,x)` is identical: it reads only `A` and `x`.
3. KEEP `c(B,x)` is identical: it reads only `B` and `x`.
4. DELETE has `y=0` identically in both states.
5. Splay successor pair `(A',B')` depends only on `(A,B)`, mode, `x`
   via the frozen ordinary bottom-up `S_x`; recency plays no role.
6. Recency fields update deterministically
   (`update(rho,x)` = remove-if-present then prepend; KEEP updates both
   streams, DELETE updates `rho_X` only) but do not affect enabled
   actions, Splay transitions, or edge regret.
7. Therefore for each action, both states offer the same `w_b(e)` and
   move to successors `z_1'`, `z_2'` with `pi(z_1')=pi(z_2')=(A',B')`,
   i.e. `z_1' R_pi z_2'`. By coinduction on the deterministic
   transition system, corresponding future paths from `z_1` and `z_2`
   carry identical edge-regret sequences `w_b(e_1),w_b(e_2),...`.
8. Taking suprema over continuations (including the empty one) in the
   Bellman recursion yields identical values:
   `V_b^R(z_1)=V_b^R(z_2)` for every fixed feasible `b`.

The argument uses only the section 6 update rules and the frozen
`(A,B)` transition/cost definitions. It never inspects `U_b^R`,
candidate potentials, or holdout contents.

## Limitations

- Finite-horizon suprema only; no claim about infinite-path attainment.
- Requires the frozen relative-recency contract (no absolute timestamps,
  unseen-key ties handled per section 6.5); absolute-time smuggling
  would void step 6.
- Requires `b` fixed and feasible so the Bellman recursion is valid;
  infeasible `b` is out of scope.
- Says nothing about `U_b^R`, which aggregates past slack along
  history-dependent diagonal-rooted paths and may separate same-`(A,B)`
  states. That separation is a history-cost observation, not a
  necessity proof for universal potentials.

## Explicit non-converse note

Only `same-(A,B) => bisimilar` is claimed. The converse
(`bisimilar => same (A,B)`) is NOT claimed and is false as a general
statement about the quotient: two different `(A,B)` states can be
behaviorally bisimilar, which is precisely what the partition-refinement
machinery is designed to discover.

## Consequence for V_b^R

Same-`(A,B)` augmented states have identical canonical future regret.
Recency carries no additional `V` information beyond `(A,B)`.

## Consequence for the WP-4 canary

Group augmented states by `(A,B)`; assert
`max V_b^R - min V_b^R == 0` exactly per group. Any nonzero spread is
`RECENCY_V_CANARY_FAIL`, an implementation failure (wrong successor,
wrong cost, leaked recency into `w_b`, or broken Bellman solve) — never
evidence that recency holds extra debt information.

## No claim that recency is useless for candidate Phi

This theorem does not diminish recency as a history-dependent accounting
representation. A candidate `Phi(A,B,rho_X,rho_Y)` may still be
structurally simpler, track `U_b^R` or path-specific creation, or make
KEEP/DELETE deltas transparent, even though `V_b^R` projects to `(A,B)`.
Recency may still affect `U_b^R`, history-specific accounting,
candidate-Phi representations, or theorem simplicity.

## Review record

- PROVED: 2026-09-22, prover Muse Spark (implementation agent), commit reseal (see Path.md WP-1 reseal entry).
- REVIEWED: 2026-09-22, independent check `tests/parent/test_bd015_recency_v_blindness.py` (file existence, pointer resolution, SHA match, implication present, converse absent, canary gate) — all green.
- Gate: WP-4 canary requires this REVIEWED status; use while UNPROVED/BLOCKED is forbidden.
