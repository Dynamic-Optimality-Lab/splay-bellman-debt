# Path.md — Implementation Tracker for SPLAY-AM-BD v0.2 (mirrors WorkPlan.md exactly)

**Experiment:** `SPLAY-AM-BD-v0.2` | **Plan:** `WorkPlan.md` (WP-1…WP-6 ← SPEC PHASE 00–18, §§0–36)
**Repo:** https://github.com/Dynamic-Optimality-Lab/splay-bellman-debt
**Parent:** https://github.com/Dynamic-Optimality-Lab/splay-pair-dynamics @ `6de1ca2` (`FINITE_EXACT_BN_RESULTS`, read-only source)
**Rule (task-critical, never forgotten):** as implementation moves forward, *every* step is documented here — what was implemented, with what evidence, and **whether it follows WorkPlan.md or not, with deep detail exactly like WorkPlan.md** (same phase structure, same scope / files / code-how / model-benchmarks / anti-overfitting / gates granularity). Deviations, if any, get their own dated entry with cause, impact, and corrective versioning. Failed hypotheses, counterexamples, and stopped runs are preserved, never overwritten. This file is updated in every phase as work proceeds — THIS IS NOT OPTIONAL.
**Status convention per WP phase:** `PENDING` (not started) / `IN_PROGRESS` (underway) / `GATED_PASS` (all gates green) / `GATED_FAIL` (a named failure label emitted) / `BLOCKED` (waiting on dependency) / `DEVIATED` (off-plan — requires deviation entry).

---

## Step 0 — Clone, clear-check, deep study, plan creation (2026-09-22) ✅ DONE

**What was done (deep detail, mirrors WorkPlan.md §0):**

1. **Cloned** `https://github.com/Dynamic-Optimality-Lab/splay-bellman-debt` into workspace `Splay-Wtv/splay-bellman-debt`. Evidence: `git remote -v` → `origin https://github.com/Dynamic-Optimality-Lab/splay-bellman-debt (fetch/push)`; `git status` → `On branch main, No commits yet, nothing to commit`; `Get-ChildItem -Force` → `.git` only; `git ls-files` → empty (no output). Branch `main`, zero commits.
2. **Parent remote verified (plan-time only; full seal audit is WP-1):** `git ls-remote https://github.com/Dynamic-Optimality-Lab/splay-pair-dynamics HEAD` → `6de1ca2a595e8895f54794f3a211fe6ee1a95a80 HEAD`, matching sealed commit `6de1ca2` in spec. No parent clone made yet; no parent artifact trusted from prose.
3. **Previous-results clearing check:** probed for `artifacts/`, `WorkPlan.md`, `Path.md`, any code/caches — all absent (only `.git/` exists, `Test-Path … → True` for repo root, `False` for every artifact path). **Conclusion: nothing to delete; the "only new results after the changes" guarantee holds vacuously at plan time.** Recorded in `WorkPlan.md §0`. No files deleted, no history rewritten — so nothing could have been silently lost. Append-only rule frozen in plan (§0.3 + §§10–11) to preserve it.
4. **Deep-studied the full frozen spec** (`SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.md`: §§0–36, PHASE 00–18, T01–T50, INV-001–050, full test matrix, §31 checklist, §33 Experiment-0 bundle A–L, §34 tables A–H, §36 Q1–27) end-to-end before writing any plan. Verified quantitative anchors carried into plan: `|R_n|` 4,19,196,1764,17424,184041; `b_n*` 1,1,3/2,8/5,8/5,23/14; b=2 `maxU` 4,10,22,38,44,58 / `maxV` 0,1,2,3,5,6 / forced 2,5,14,42,132,429; H-0001..0006 rejections; anchor `b=2/1` + panel 5/2,3,4; tracks STATE_ONLY (dev 2..7, EV8 8, H1) vs RECENCY (dev 2..4+stretch5, H2R 120k states / 4,080,000 transitions over 8,10,12,16,24,32×20k); BD0-01..14; PHI-GATE-0..11; 9 terminal claim levels; 27 purpose questions.
5. **Created `WorkPlan.md` (6 phases WP-1…WP-6, coverage matrix SPEC 00–18 → WP, per-phase scope/files/code-how/model-benchmarks/brutal-anti-overfitting, global charter §9, cross-cutting rules §10, acceptance §11) and this `Path.md`.** Both written into the repo (`splay-bellman-debt/WorkPlan.md`, `splay-bellman-debt/Path.md`). No implementation code written yet; no artifacts produced; no gates run. No AI-driven semantic change: Splay/cost/reachability/encoding untouched; no rounding; no kernel/atom/candidate defined; no finite-evidence promotion; no counterexample exists to suppress; no holdout touched.
6. **Workload decision recorded:** 6 work phases (not 5, not 19) per `WorkPlan.md §0.5` — flawless division proof in `WorkPlan.md §2` (every PHASE 00–18, every §0–36, every T01–T50 / INV-001–050 / test ID mapped). More phases not needed; fewer would blob unrelated gates.

**Follows WorkPlan.md?** YES — exactly. This step *is* `WorkPlan.md §0` executed verbatim: clone → list → clear-check → parent-remote check → study → plan. No deviation. Next: WP-1 begins (entry below).

**Evidence:** git outputs + `Test-Path`/`Get-ChildItem` results quoted above (re-runnable: `git remote -v; git status; Get-ChildItem -Force; git ls-files` in repo dir; `git ls-remote https://github.com/Dynamic-Optimality-Lab/splay-pair-dynamics HEAD` anywhere).
**Files created this step:** `WorkPlan.md` (plan v0.2.0 FROZEN), `Path.md` (this file).
**Plan commit:** `01cea5c` on `main` (2026-09-22) — `WorkPlan.md` + `Path.md` committed and pushed to `origin/main`; working tree clean. Standing instruction from owner: commit + push whenever a unit of work is done — applied here and to be applied going forward without being told every time.

---

## Audit remediation — WorkPlan v0.2.1 COMPLIANT FROZEN (2026-09-22) ✅ DONE

**Verdict in:** `AUDIT_FAIL_REPAIRABLE` (5 findings; 0 experiments discarded — none started). All fixed, committed, pushed. New stamp: `WORKPLAN_v0.2.1_COMPLIANT_FROZEN`.

**What was done (deep detail, mirrors WorkPlan.md §§1/3/6/7/9/10/11 + SA-01):**

1. **Finding 1 — SPEC BUG, recency-`V` blindness (`WorkPlan.md §1` + `§6` + new `SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.1.md` SA-01.1):** proved `π(A,B,ρX,ρY)=(A,B)` is a cost-preserving bisimulation (same actions, same `(A,B)→(A′,B′)` transitions, same `w_b`), hence `V_b^R(A,B,ρX,ρY)=V_b^R(A,B,ρ′X,ρ′Y)` necessarily. WP-4 scope now asserts `same (A,B) ⟹ same V_2^R` with `RECENCY_V_CANARY_FAIL` on any nonzero spread (implementation failure, never debt evidence); recency value redirected to `U_b^R`, path-specific creation, `Φ` deltas, simplicity. Added BD0-15 gate + `RECENCY_V_CANARY` benchmark. Theorems before shortcuts: BD0-15 PROVED+REVIEWED required.
2. **Finding 2 — `parent/` contradiction (`WorkPlan.md §3` + SA-01.2):** replaced "create `parent/` + any write raises STOP" with `BOOTSTRAP_PARENT_IMPORT`: populate once → verify → write `parent/BOOTSTRAP_MANIFEST.sha256` → `READ_ONLY_LOCKED`; post-lock mutation fatal (STOP-01/02/03). `import_ledger.json` written only inside bootstrap. Source repo always immutable.
3. **Finding 3 — transcendental branch (`WorkPlan.md §7` + SA-01.3):** residual evaluator split into `RATIONAL` (exact rational, `>0` rejects per T20, float-sign → STOP-13) and `TRANSCENDENTAL` (certified interval: `≤0` certified / `>0` counterexample / straddles → `SIGN_UNCERTIFIED`, blocks promotion). No epsilon. Benchmarks + WP-6 acceptance updated.
4. **Finding 4 — STOP wiring (`WorkPlan.md §§5/7/10` + SA-01.4):** `>0` rejection is T20 (not STOP-20); float-sign is STOP-13; STOP-20 is holdout reuse. Corrected WP map (WP-2: 12,15; WP-3: 05–08; WP-4: 09–11,16,19,20; WP-5: 13–15,17–22; WP-6: 23–30; WP-1: 01–04) + new `prereg/stop_control_matrix.yaml`.
5. **Finding 5 — hardening (`WorkPlan.md §§3/9/10/11`):** new `prereg/threat_control_matrix.yaml` (T01–T50 → controls + phase; WP-6 asserts count==50) + `prereg/discovery_splits.yaml` (internal Track-S/Track-R discovery/validation masks + b-panel + seed policy frozen before any target search; no adaptive held-out choice).

**Files (all created/edited, hashed at commit):** `WorkPlan.md` (v0.2.0 → v0.2.1), `SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.1.md` (SA-01), `prereg/threat_control_matrix.yaml`, `prereg/stop_control_matrix.yaml`, `prereg/discovery_splits.yaml`, `Path.md` (this entry).
**Code/models/benchmarks:** NONE trained/run (plan-level only); resultant benchmarks are the corrected gates above (canary, bootstrap-lock, two-branch residuals, STOP matrices, count==50 + splits-hash checks).
**Brutal-testing note:** canary + matrices + splits exist to make future training (WP-3/4/5 kernels/atoms/Phi) face entirely-different benchmarks; no training data touched.

**Follows WorkPlan.md?** YES — this remediation *is* `WorkPlan.md` v0.2.1 (§§1/3/6/7/9/10/11) + SA-01 executed verbatim with evidence above. No deviation. No experiment discarded. Next: WP-1 begins under v0.2.1.

---

## WP-1 — Foundation: parent seal, literature, contract, prereg, theorem ledger (SPEC PHASE 00) — status: `PENDING`

**Scope per WorkPlan.md §3:** parent clone @ `6de1ca2` + seal verify + history preserve; spec freeze + hash; literature L0–L4 ledger; BD0-01..14 ledger; H1 EMPTY + n8 contaminated; no pre-prereg output. Out: no Bellman/features/kernels/candidates/holdout-reads.
**What was implemented:** _nothing yet — entry will record files (README/IMPLEMENTATION_SPEC/parent/prereg/external/math/schemas/scripts/logs), code (read-only adapter, prereg freezer, ledger initializer) + how, model training (NONE) + benchmarks (PARENT-01..06, Phase-00 gate), and follows-WorkPlan verdict with evidence when work starts._
**Follows WorkPlan.md?** _TO BE RECORDED per-step as work proceeds (YES/NO + deep detail + evidence + deviation entry if NO)._
**Next action:** begin WP-1 per `WorkPlan.md §3`.

---

## WP-2 — Fixed-b Bellman debt geometry, signatures, extremal specimens (SPEC PHASE 01, 02, 03) — status: `PENDING`

**Scope per WorkPlan.md §4:** read-only parent import + independent reproduction (n=2..6 full, n=7 streamed, `b_n*` reverify); import fact table; b=2 anchor n=2..7 (U/V/G, tight edges, excess/creation, residuals); panel 5/2,3,4 (2..5 required, 6..7 stretch); diagnostics recorded-not-assumed; independent verifier; BELL-SIG + edge signatures + KEEP_EXCESS/DELETE_CREATION/EXACT_V_REPAYMENT/tight tables + canonical witnesses + trajectories.
**What was implemented:** _nothing yet — entry will record files (`python/bellman_debt/`, `python/audit/`, schemas, `artifacts/v02/{parent_import,bellman,specimens,audits,logs}`, scripts, tests), code + exact-arithmetic how, model training (NONE — exact DPs) + benchmarks (BD-01..10, anchor gate), and follows-WorkPlan verdict with evidence._
**Follows WorkPlan.md?** _TO BE RECORDED._
**Next action:** needs WP-1 seal (import adapter + prereg hash).

---

## WP-3 — State-only ontology, behavioral quotient, kernel ablation, debt-law mining (SPEC PHASE 04, 05, 06, 07) — status: `PENDING`

**Scope per WorkPlan.md §5:** blind Track-S extraction (audit-enforced, join-after-freeze); all state families + raw components + symmetry + determinism; FULL_STATE control; target-independent refinement to fixed point + second-implementation agreement + BD0-gated transport + compression report; overcomplete K0 + per-family witnesses (VALUE/TRANSITION/CLASS_INSUFFICIENT) + sharpness + COMPONENTWISE_NECESSARY wording; delta-first datasets + creation/repayment screens + exact linear/piecewise search (coverage-first ranking) + inconsistent subsystems + motifs.
**What was implemented:** _nothing yet — entry will record files (`python/structure/`, `python/kernel/`, `python/mining/`, ontology YAML, `artifacts/v02/{structure,kernels,debt_atoms,audits}`, scripts, tests), code + how, **model specifics (kernels K_j + atom combos; training data = dev Track-S anchor geometry; resultant benchmarks = coverage/V-tight/DELETE-bounded/stability/complexity/compression) + brutal entirely-different testing (held-out n, EV8-contaminated, different b/families/code/regime) + anti-overfitting actions**, gates (ST/K), and follows-WorkPlan verdict._
**Follows WorkPlan.md?** _TO BE RECORDED._
**Next action:** needs WP-2 anchor geometry.

---

## WP-4 — Recency track, augmented geometry, H2R holdout, recency ontology, debt atoms (SPEC PHASE 08, 09, 10) — status: `PENDING` ⭐ MODEL-TRAINING

**Scope per WorkPlan.md §6:** BD0-06/07 proved first; augmented reachability n=2,3,4 (+5 stretch) with parent-witness/closure; augmented b=2 geometry; same-pair/different-recency separation table (finite only); H2R generation+quarantine BEFORE synthesis (120k / 4,080,000, stratified, commitment, firewall EMPTY→COMMITTED→FROZEN→UNLOCKED_ONCE); blind recency ontology (heap/crossing/nested/rank/inversion/heavy/multiscale, tie audit, S-vs-R ablation); atom discovery (eligibility, creation/repayment, V-tight diagnostics, scale audit, exhaustion).
**What was implemented:** _nothing yet — entry will record files (`python/recency/`, `python/holdout/h2r_*`, recency ontology, `python/mining/atoms.py`, schemas, `artifacts/v02/{recency,holdouts/H2R,debt_atoms,audits}`, scripts, tests), code (ρ state/updates, BFS, H2R sampler, firewall) + how, **model specifics (recency atoms D1–D9; training = augmented n≤4(+5); resultant benchmarks = creation/repayment/V-tight/scale/stability) + brutal testing (stretch-5, H2R-scale regimes, recency splits, different b/code/target) + anti-overfitting (pre-synthesis commitment, blind firewall, new-ID rules, tie mutants)**, gates (R/D/HLD), and follows-WorkPlan verdict._
**Follows WorkPlan.md?** _TO BE RECORDED._
**Next action:** needs WP-2/WP-3 + BD0-06/07; H2R must precede WP-5 synthesis.

---

## WP-5 — Candidate synthesis, development falsification, holdout consumption, independent+adversarial (SPEC PHASE 11, 12, 13, 14) — status: `PENDING` ⭐ MODEL-VALIDATION

**Scope per WorkPlan.md §7:** ERA-BD-A synthesis (dev-only evidence); per-PHI freeze (def/track/b_H/ties/normalization/ontology/range/proof-outline; change→new ID); correct-b precheck; exact dev falsification (S n=2..7, R n≤4(+5), E_K/E_D exact, smallest+max residuals, failure analysis); set commitment; correct once-only validation (S: EV8→H1; R: H2R 120k+4.08M + replay; POST_HOLDOUT new IDs); clean-room evaluator; adversary families+engines; mutations + smallest counterexamples. Ceiling: finite survival only.
**What was implemented:** _nothing yet — entry will record files (`python/mining/synthesize.py`, holdout evaluators, clean-room audit, `python/adversary/`, schemas, `artifacts/v02/{hypotheses,falsification,holdouts,adversarial,audits}`, scripts, tests), code + how, **validation on ENTIRELY different benchmarks (EV8-contaminated vs H1/H2R-fresh, independent code, large-n adversaries, wrong-b/coefficient/sign/tie mutants) + anti-overfitting**, gates (D/HLD, PHI-GATE-0..9), and follows-WorkPlan verdict._
**Follows WorkPlan.md?** _TO BE RECORDED._
**Next action:** needs WP-2/3/4 + H2R commitment + frozen candidates.

---

## WP-6 — Universal proof, telescoping+bridge, negative branch, seal+release (SPEC PHASE 15, 16, 17, 18) — status: `PENDING`

**Scope per WorkPlan.md §8:** ≤1 primary candidate at a time; domain/definedness/identity/nonnegativity/DELETE/KEEP/case-partition (Splay + recency, nonlocal bounds, kernel lift; no finite premises) + review → PA lemma; telescoping (+augmented legitimacy) + Levy–Tarjan audit → monotonicity → optimality; negative branch only on C1–C4 (closed-form family, symbolic f/g, g/f→∞, reverse bridge); FINAL_RESULT (one of 9 levels) from artifacts; fresh-checkout reproduction; deterministic `SPLAY-AM-BD-v0.2.tar.zst`; reports (DEBT/KERNEL/HYPOTHESES/MINING/REPRO/AI_USE); no deletion cleanup; answers §36 Q1–27.
**What was implemented:** _nothing yet — entry will record files (`math/` proofs+latex, `artifacts/v02/seal/`, archive, reports, scripts, tests), proof work + how, model training (NONE) + benchmarks (PR/NEG/SEAL), and follows-WorkPlan verdict._
**Follows WorkPlan.md?** _TO BE RECORDED._
**Next action:** needs WP-5 survivor (positive) and/or C1–C4 motif (negative); otherwise finite-seal path.

---

## Deviation log (empty — no deviations)

| Date | Phase | Deviation | Cause | Impact | Corrective versioning |
|---|---|---|---|---|---|
| — | — | _none_ | — | — | — |

## Stop / resource-limit log (empty — no stops)

| Date | Phase | Code | Evidence | Resolution |
|---|---|---|---|---|
| — | — | _none_ | — | — |
