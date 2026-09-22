# theorem_BD06_recency_update.md — BD0-06 (rho update preserves relative order)

**Obligation:** BD0-06 — `rho(P)` update exactly preserves relative last-access order of seen keys.
**Status:** REVIEWED (lifecycle UNPROVED → PROVED → REVIEWED closed during WP-4; see `math/proof_status.json`).
**Scope:** section 6 relative-recency contract. No absolute timestamps exist.

## Definitions

- History `H=[x_1..x_k]`; last-access time `last(x)=max{i:x_i=x}` (undefined if unseen).
- `rho(H)`: distinct seen keys ordered by decreasing `last` (most recent first).
- `update(rho,x)`: remove `x` if present, prepend `x`.

## Theorem

For every history `H` and key `x`, `update(rho(H),x) = rho(H+[x])`.

*Proof.* Appending `x` sets `last(x)` above all others; all other keys
keep their relative order. Removing `x` from `rho(H)` and prepending
it produces exactly the decreasing-`last` order of `H+[x]`. Unseen keys
stay the complement, tied below seen keys. ∎

## Corollary (seen/unseen complement)

Keys never accessed are omitted and recoverable as `[n] \\ rho`.
Duplicate access moves the key to front (R-03); KEEP/DELETE routing
(R-04/05) does not affect the order logic.

## Review record

- PROVED: 2026-09-22, prover Muse Spark (implementation agent), WP-4.
- REVIEWED: 2026-09-22, independent check `tests/test_wp4_recency.py` (R-01..07 incl. replay property) — green.
- Gate: augmented Bellman claims require this REVIEWED status.
