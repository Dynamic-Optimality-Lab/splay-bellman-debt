# theorem_BD9_recency_v_blindness.md — SA-01 one-way blindness (BD0-15)

**Obligation:** BD0-15 — same-`(A,B)` implies equal augmented `V_b^R`.
**Status at plan freeze:** UNPROVED (transitions UNPROVED→PROVED→REVIEWED during WP-1; WP-4 canary gated on PROVED+REVIEWED).
**Scope:** all `n`, all fixed `b`, augmented track `z=(A,B,ρX,ρY)` per §6 contract.

## Definitions

- `π(A,B,ρX,ρY) = (A,B)`.
- `R_π` defined by `z1 R_π z2 ⟺ π(z1) = π(z2)`.
- Actions: `(KEEP,x)` and `(DELETE,x)` for `x ∈ [n]`, enabled in every augmented state.
- KEEP successor: `(S_xA, S_xB, update(ρX,x), update(ρY,x))` with `a=c(A,x)`, `y=c(B,x)`.
- DELETE successor: `(S_xA, B, update(ρX,x), ρY)` with `a=c(A,x)`, `y=0`.
- Edge weight `w_b(e) = y − b·a` depends only on `(A,B,x,mode)`.

## Lemma (one-way)

If `π(z1) = π(z2) = (A,B)` then for every action `(mode,x)`:

1. the same action is enabled from both states;
2. `a` and `y` (hence `w_b`) agree;
3. projected successors agree: `π(z1') = π(z2') = (A',B')` for the shared `(A,B)→(A',B')` transition;
4. successor recency states are deterministic functions of `(ρX,ρY,x,mode)` but remain `R_π`-compatible for the `V`-recursion below.

*Proof.* Directly from the §6 paired-update rules: the `(A,B)` transition and costs read only `(A,B,x,mode)`, never `ρX,ρY`. ∎

## Theorem

`R_π` is a cost-preserving bisimulation in the one-way sense needed: `π(z1)=π(z2) ⟹ z1∼z2` for the future-reward structure. Consequently for every fixed `b`:

```text
V_b^R(A,B,ρX,ρY) = V_b^R(A,B,ρ′X,ρ′Y)
```

*Proof sketch (to be completed + reviewed in WP-1).* By induction on the Bellman recursion `V_b(s)=max(0,max_e[w_b(e)+V_b(t)])`: base `0` agrees; inductive step uses the Lemma (same `w_b` options, same projected successor classes, hence same suprema). The converse (`z1∼z2 ⟹ π(z1)=π(z2)`) is explicitly NOT claimed — different `(A,B)` states may still be behaviorally bisimilar. ∎

## Canary consequence

Group augmented states by `(A,B)`; assert `max V_b^R − min V_b^R == 0` exactly per group. Any violation ⇒ `RECENCY_V_CANARY_FAIL` (implementation failure).

## Review record

- [ ] PROVED (WP-1 prover + date + commit)
- [ ] REVIEWED (independent reviewer + date + commit; must check one-way statement, no converse smuggled in)
- Gate: WP-4 canary requires both boxes ticked.
