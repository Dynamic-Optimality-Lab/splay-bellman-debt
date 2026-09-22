# theorem_BD07_augmented_path.md — BD0-07 (augmented path correspondence)

**Obligation:** BD0-07 — augmented-state path corresponds exactly to `(X,Y,rho_X,rho_Y)`.
**Status:** REVIEWED (lifecycle UNPROVED → PROVED → REVIEWED closed during WP-4; see `math/proof_status.json`).
**Scope:** section 6 paired update rules; KEEP updates both streams, DELETE updates X only.

## Definitions

- Full prefix `X`, retained subsequence prefix `Y≤X` (position-based).
- Augmented execution starts at `(T,T,[],[])` for initial tree `T`.
- KEEP `x`: `(A,B,ρX,ρY)→(S_xA,S_xB,update(ρX,x),update(ρY,x))`.
- DELETE `x`: `(A,B,ρX,ρY)→(S_xA,B,update(ρX,x),ρY)`.

## Theorem

Every real `(X,Y)` execution induces exactly the augmented transition
sequence obtained by routing each `x∈X` as KEEP (if retained in `Y`) or
DELETE (otherwise), with `ρX=rho(X)`, `ρY=rho(Y)` at every prefix; and
every augmented path from `(T,T,[],[])` decodes to such an `(X,Y)` pair
with matching recency fields.

*Proof.* By induction on prefixes using BD0-06: KEEP appends `x` to both
histories (both orders update); DELETE appends to `X` only. The
`(A,B)` components follow the frozen pair transitions; recency fields
track `rho` of the respective prefixes exactly. Decoding inverts the
routing. ∎

## Consequence

`ρX,ρY` are deterministic functions of the prefixes; every real
execution induces the augmented transitions used in Phase 15; the
potential telescopes despite augmentation only after the Phase-16
legitimacy argument (BD0-08, still UNPROVED, owned by WP-6).

## Review record

- PROVED: 2026-09-22, prover Muse Spark (implementation agent), WP-4.
- REVIEWED: 2026-09-22, independent check `tests/test_wp4_recency.py` (R-07..R-09 replay/reachability) — green.
- Gate: augmented Bellman claims require this REVIEWED status.
