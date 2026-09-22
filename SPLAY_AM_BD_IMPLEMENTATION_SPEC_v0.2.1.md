# SPLAY-AM-BD v0.2.1 — Spec Amendment SA-01 (ratified)

**Parent spec:** `SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.md` (PHASE 00–18, §§0–36)
**Amendment:** SA-01 — recency-`V` blindness + `parent/` bootstrap + transcendental branch + STOP corrections
**Status:** RATIFIED (2026-09-22) — triggered by external compliance audit `AUDIT_FAIL_REPAIRABLE` against v0.2.0 plan
**Normative effect:** parent v0.2 unchanged except where stated below; base + SA-01 + WorkPlan v0.2.1 normative elsewhere.

## SA-01.1 Recency-`V` blindness theorem (amends §8.4)

Recency updates `ρX,ρY` change neither the enabled action set, the `(A,B)→(A′,B′)` Splay transitions, nor costs `w_b(e)=y−b·a`. Hence for fixed `(A,B)`:

```text
z1 ∼ z2 ⟺ π(z1) = π(z2) = (A,B)
```

is a cost-preserving bisimulation. Therefore for every fixed `b`:

```text
V_b^R(A,B,ρX,ρY) = V_b^R(A,B,ρ′X,ρ′Y)
```

necessarily. Phase 08.4 is replaced by:

```text
same (A,B) ⟹ same V_b^R (assert; any nonzero spread ⇒ RECENCY_V_CANARY_FAIL, implementation failure)
```

Recency remains scientifically valuable as a history-dependent accounting representation: `U_b^R`, path-specific creation, candidate-`Φ` deltas, and structural simplicity. Adds theorem obligation BD0-15 (projection `π` is a cost-preserving bisimulation ⇒ same-`(A,B)` same `V_b^R`) as PROVED+REVIEWED gate for the WP-4 canary.

## SA-01.2 `parent/` bootstrap clarification (amends §13 separation)

```text
BOOTSTRAP_PARENT_IMPORT:
  populate parent/ exactly once from verified parent artifacts
  verify hashes
  freeze parent/ manifest (parent/BOOTSTRAP_MANIFEST.sha256)
  transition parent/ -> READ_ONLY_LOCKED
after lock:
  every mutation of parent/ is fatal (STOP-01/02/03)
```

Source parent repo always immutable; v0.2 `parent/` snapshot has one authorized initialization.

## SA-01.3 Transcendental sign branch (clarifies §11.3 + §24)

```text
RATIONAL:       exact arbitrary-precision rational residual
TRANSCENDENTAL: symbolic / directed certified-interval residual
  interval entirely <= 0 -> certified
  interval entirely > 0  -> counterexample
  interval straddles 0   -> SIGN_UNCERTIFIED (not PASS)
```

No floating-point epsilon decides a sealed sign.

## SA-01.4 STOP-ID corrections (amends §30 wiring)

- Exact `>0` rejection is T20; float-dependent sign is STOP-13 (not STOP-20; STOP-20 is fresh-holdout reuse).
- STOP-05..08 (target leakage / kernel / quotient / premature transport) belong primarily to WP-3 (state-only mining), not WP-2.
- Full corrected WP mapping lives in `prereg/stop_control_matrix.yaml` (machine-checked).

## Ratification record

- Audit verdict: `AUDIT_FAIL_REPAIRABLE` (2026-09-22), 5 findings (1 spec-level + 4 plan-level + 2 hardening).
- This file + WorkPlan v0.2.1 + `prereg/threat_control_matrix.yaml` + `prereg/stop_control_matrix.yaml` + `prereg/discovery_splits.yaml` close all 5.
- Next stamp on acceptance: `WORKPLAN_v0.2.1_COMPLIANT_FROZEN`.
