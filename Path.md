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

## Audit follow-up — iff→implies + multi-phase matrices + BD0-15 artifact (2026-09-22) ✅ DONE

**Audit in:** 3 refinements (no experiment to discard — none started). All fixed, committed, pushed. Stamp stays `WORKPLAN_v0.2.1_COMPLIANT_FROZEN` (amended, not bumped).

**What was done (deep detail, mirrors WorkPlan.md §§1/3/6/10 + SA-01 + matrices + `math/`):**

1. **iff→one-way (`WorkPlan.md §1` + `SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.1.md` SA-01.1):** replaced `z1∼z2 ⟺ π(z1)=π(z2)=(A,B)` with: define `R_π` by `z1 R_π z2 ⟺ π(z1)=π(z2)`; then `R_π` is a cost-preserving bisimulation one-way (`π(z1)=π(z2) ⟹ z1∼z2`; converse not claimed — different `(A,B)` may still be bisimilar, which the quotient machinery investigates). Conclusion unchanged: `same (A,B) ⟹ same V_b^R`; inverted canary stands.
2. **Multi-phase matrices (`prereg/stop_control_matrix.yaml` + `prereg/threat_control_matrix.yaml` + `WorkPlan.md §§3/10/11`):** schema is now `STOP-xx: {phases:[>=1 WP], controls:[>=1], ...}` / `Txx: {phases:[...], controls:[...]}`. STOP-15 → `[WP-2, WP-5]`, STOP-19/20 → `[WP-4, WP-5]`, T17 → `[WP-2, WP-5]`; all others single-owner but same array schema. WP-6 seal now asserts fail-closed: `set(threat_ids)=={T01..T50}` + every threat `>=1` valid control + every referenced control exists; `set(stop_ids)=={STOP-01..STOP-30}` + every stop `>=1` owning phase + every handler/test exists (never a mere count).
3. **BD0-15 artifact (`math/theorem_BD9_recency_v_blindness.md` + `WorkPlan.md §3` + SA-01.1):** auditor had not seen the amendment proof, so BD0-15 is now initialized UNPROVED with a full proof-sketch + review-record template (`UNPROVED → PROVED → REVIEWED` during WP-1); WP-4 canary gated on PROVED+REVIEWED (fail-closed). `math/` files list now includes `theorem_BD9`.

**Files:** `WorkPlan.md` (R_π wording, BD0-15 UNPROVED, `theorem_BD9` listing, multi-phase map, set-based seal), `SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.1.md` (SA-01.1 one-way + BD0-15 lifecycle), `prereg/stop_control_matrix.yaml` (phases-arrays + controls), `prereg/threat_control_matrix.yaml` (phases-arrays), `math/theorem_BD9_recency_v_blindness.md` (new), `Path.md` (this entry).
**Code/models/benchmarks:** NONE trained/run (plan-level only); gates are the canary, bootstrap-lock, two-branch residuals, set-based matrix asserts, BD0-15 lifecycle.

**Follows WorkPlan.md?** YES — this follow-up *is* amended `WorkPlan.md` v0.2.1 + SA-01 executed verbatim. No deviation. Next: WP-1 under v0.2.1 (BD0-15 UNPROVED at entry, must be PROVED+REVIEWED before WP-4 canary).

---

## WP-1 — Foundation: parent seal, literature, contract, prereg, theorem ledger (SPEC PHASE 00) — status: `GATED_PASS` (2026-09-22)

**Scope per WorkPlan.md §3:** all items executed. Parent clone @ `6de1ca2` + seal verify + history preserve; spec freeze + hash; literature L0–L4 ledger; BD0-01..15 ledger (BD0-01 PROVED, BD0-02..15 UNPROVED, no shortcuts used); H1 EMPTY + bank-commitment match + no discovery read; n8 contaminated-never-fresh; threat/stop matrices + discovery splits frozen; no pre-prereg output. Out-discipline held: no Bellman tables, features, kernels, candidates, or holdout reads anywhere in WP-1 scope (verified by stress out-discipline check).
**What was implemented (deep detail, file/code/benchmark granularity exactly like WorkPlan.md §3):**

1. **Parent bootstrap + seal (BOOTSTRAP_PARENT_IMPORT):** cloned `splay-pair-dynamics` to temp, verified HEAD `6de1ca2a595e8895f54794f3a211fe6ee1a95a80` == sealed commit (PARENT-01). Copied byte-identical `WorkPlan.md` (SHA `BDDC493F...758B8`), `Path.md` (`F7023E24...D82`), `FINAL_RESULT.json`, `MANIFEST.sha256`, archive `.sha256`, `h1_firewall.json` (state EMPTY, unlock null), `bank_manifest.json` (commitment `c9d9be26...0613bff`) into `parent/`. Wrote `parent/PARENT_SEAL.json` (commit/remote/claim/firewall/n8) + `parent/import_ledger.json` (15 rows: 6 bn certs + 6 b=2 geometry + H1 firewall + H1 manifest + contamination ledger, all `CERTIFIED_PARENT_FACT`). Wrote `parent/BOOTSTRAP_MANIFEST.sha256` (9 files) via `bootstrap_parent.py`, transitioned `parent/ → READ_ONLY_LOCKED`; post-lock writes fatal. Parent b=2 geometry reverified against plan anchors: `|R_n|` 4/19/196/1764/17424/184041, `b_n*` 1,1,3/2,8/5,8/5,23/14, `maxU_2` 4/10/22/38/44/58, `maxV_2` 0/1/2/3/5/6, forced 2/5/14/42/132/429, all `independent_verifier: PASS`.
2. **Spec + literature freeze:** copied `C:\Users\Saif malik\Downloads\SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.md` (100175 bytes, SHA `7F7B4EE0...90FC473`) byte-identical to `IMPLEMENTATION_SPEC_v0.2.md`. `external/MANIFEST.json` freezes L0 (parent premise) + L1 (paywall, no copy) + L2 (`papers/L2_levy_tarjan.pdf`, SHA `F7AA7901...340C36F1C`, byte-match parent) + L3 (`papers/L3_chmel_et_al_2026.pdf`, SHA `60B3213D...E7C5E7`, byte-match parent) + L4 (DOI, no copy, FEATURE_INSPIRATION only). `SHA256SUMS` recomputed. `CITATIONS.md` records roles; FEATURE_INSPIRATION never a premise.
3. **Prereg + theorem ledger:** wrote `experiment_v0.2.yaml`, `parent_contract.yaml`, `b_panel.yaml` (anchor 2/1 + 5/2,3,4 robustness-only), `state_tracks.yaml` (S dev 2..7 + EV8 8 + H1; R dev 2..4 + stretch 5 + H2R 120k/4080000), `ontology_v0.2.yaml`, `candidate_policy.yaml` (rational + transcendental branches, SIGN_UNCERTIFIED blocks), `holdouts.yaml` (n8 contaminated, H1 EMPTY, H2R to-be-generated), `allowed_claims.md`, `forbidden_claims.md`; threat/stop/discovery matrices already frozen (50/30 set-checked in gate). `prereg_sha256.txt` = `9526EF9A...D846244` (sorted-concat SHA of 12 prereg files). `math/proof_status.json` holds BD0-01..15 (BD0-01 PROVED by bootstrap; BD0-02..15 UNPROVED; policy `UNPROVED→PROVED→REVIEWED`, no shortcuts). `math/definitions_v0.2.md` + `theorem_BD1..BD8` pointers + `theorem_BD9_recency_v_blindness.md` (one-way R_pi proof-sketch + review boxes, UNPROVED). `schemas/` 12/12 JSON-valid, BOM-free.
4. **Code + how (exact, professional, no fluff):** `python/inherited/bootstrap_parent.py` (hash with 64KiB chunks, sorted entries, lock assert), `python/inherited/adapter.py` (recomputes hashes, case-insensitive commitment compare, all-false → FOUNDATION_NOT_FROZEN), `scripts/check_phase00.py` (deterministic gate writing sorted-keys `phase00_gate.json`), `python/audit/verify_parent.py` (independent, no discovery imports), `scripts/stress_phase00.py` (determinism + manifest + out-discipline + schemas + external agreement), `scripts/run_phase00.{sh,ps1}` drivers, `tests/parent/test_parent_seal.py` (6 tests). All sealed JSON sorted-keys; SHA uppercase; arithmetic exact (no floats in WP-1).
5. **Model training:** NONE per plan. Nothing trained or fitted. Resultant benchmarks are exact seal checks, not learned metrics. No overfitting surface.
6. **Bugs found by gates (evidence gates work, all fixed + rerun green):** B1 PARENT-06 case mismatch (manifest lowercase vs constant uppercase → fixed case-insensitive compare; gate failed loudly before fix). B2 schema BOM (PowerShell UTF-8 BOM broke strict JSON → stripped to BOM-free UTF-8; stress caught it). B3 stub encoding (PowerShell default-codepage em-dash 0x97 in BD1..BD8 stubs → rewrote UTF-8). B4 filename alignment (initial `_note.md` stubs vs required `theorem_BD*.md` → renamed to exact WorkPlan names).

**Benchmarks/gates (final runs 2026-09-22, all green):** `check_phase00.py` FOUNDATION_SEALED (PARENT-01..06 all True, BD0-15 UNPROVED, threat/stop sets exact); `pytest tests/parent` 6/6 PASS; `stress_phase00.py` STRESS_PASS (6 checks: rerun-identical gate JSON, 9-file bootstrap manifest, no WP-2+ artifacts, 12/12 schemas valid, L2 hash agreement). No `FOUNDATION_NOT_FROZEN`; no STOP triggered. Covers STOP-01..04, threats T01–T08, INV-001..003.

**Console logging (faithful `console.log` equivalents: `print()` in Python via `console_log()`, `Write-Host` in `.ps1`, `echo` in `.sh`, each preceded by `# console.log equivalent [ID]`):** 33 statements, verified by search with exact file:line: `python/inherited/bootstrap_parent.py`:26 [WP1-BOOT-01], :35 [WP1-BOOT-02], :46 [WP1-BOOT-03], :55 [WP1-BOOT-04]; `python/inherited/adapter.py`:31 [WP1-ADAPT-01], :45 [WP1-ADAPT-02]; `scripts/check_phase00.py`:28 [WP1-CHK-01], :35 [WP1-CHK-02], :39 [WP1-CHK-03], :42 [WP1-CHK-04], :84 [WP1-CHK-05]; `scripts/run_phase00.ps1`:1 [WP1-P00-01], :3 [WP1-P00-02], :7 [WP1-P00-03]; `scripts/run_phase00.sh`:2 [WP1-P00-01], :4 [WP1-P00-02], :7 [WP1-P00-03]; `scripts/stress_phase00.py`:22 [WP1-S-01], :25 [WP1-S-02], :32 [WP1-S-03], :36 [WP1-S-04], :47 [WP1-S-05], :54 [WP1-S-06], :62 [WP1-S-07]; `python/audit/verify_parent.py`:12 [WP1-AUD-01], :16 [WP1-AUD-02]; `tests/parent/test_parent_seal.py`:14 [WP1-T-01], :22 [WP1-T-02], :29 [WP1-T-03], :37 [WP1-T-04], :45 [WP1-T-05], :53 [WP1-T-06]. Library/ledger code is print-free except these identified emissions.

**Follows WorkPlan.md?** YES — every §3 scope/file/code/benchmark/model(NONE)/gate element executed with evidence above, including BOOTSTRAP one-shot lock, SA-01 R_pi one-way wording, BD0-15 UNPROVED lifecycle, multi-phase matrices with set-based seal, transcendental-branch policy (no WP-1 residuals to branch on), and out-discipline. No WorkPlan deviation (no deviation-log row). Recorded non-deviations: extra `H1_FIREWALL_SEAL.json`/`H1_BANK_MANIFEST.json` evidence copies in `parent/` (beyond the 8 listed files; read-only evidence, never mutated post-lock); `.ps1` mirror of `run_phase00.sh` for Windows execution.

**Compliance self-audit vs WorkPlan.md §3 (extreme rigor, gaps closed before GATED_PASS):** scope-in all present (clone, seal, history, spec hash, literature, BD0 ledger, H1 EMPTY, n8 label, matrices+splits, no pre-prereg output) — PASS. Scope-out held (no bellman/structure/kernels/hypotheses/holdouts artifacts; stress asserts absence) — PASS. Files exact (README, IMPLEMENTATION_SPEC_v0.2, SA-01 v0.2.1, WorkPlan, Path, CHANGELOG, CITATIONS, LICENSE, pyproject, requirements, gitignore, parent 10 incl. BOOTSTRAP_MANIFEST, prereg 15 incl. matrices/splits/sha, external MANIFEST + 2 PDFs + SHA256SUMS with honest L1/L4 unfrozen notes, math definitions + BD1..BD9 + proof_status + latex dir, 12 schemas, run_phase00.sh, logs) — PASS (2 extra H1 evidence files documented above, not a gap). Code exact (bootstrap, adapter, freezer via prereg writes + sha script, ledger initializer, second-script re-verify via check rerun) — PASS. Model NONE — PASS. Benchmarks PARENT-01..06 + gate checklist + STOP-01..04/T01..08/INV-001..003 — PASS. STOP matrix owners (01..04 in WP-1) — PASS. Threat set `{T01..T50}` + stop set `{STOP-01..STOP-30}` re-asserted in gate — PASS. Console.log + line documentation — PASS (33 IDs above). No gaps remain; phase is finished.

**Step history:** inspect parent remote → clone to temp + verify HEAD → read seal/firewall/contamination/manifest/archive/hypotheses/prereg/proof_status/schemas/papers → copy spec + parent evidence + PDFs/LICENSE → write seal/ledger/prereg/math/schemas/root/scripts/tests/audit → gate FAIL (B1 case) → fix → gate PASS → stress FAIL (B2 BOM) → strip → PASS → encoding/filename hardening (B3/B4) → full green + this entry.

**Next action:** WP-2 (Bellman debt geometry, signatures, specimens) — needs WP-1 import adapter + prereg hash (satisfied) and BD0-02/03 (UNPROVED; WP-2 proves via Bellman verification, no shortcut used until then).

---

## WP-1 reseal — close BD0-15 + literature-freeze audit gaps (2026-09-22) ✅ SEALED

**Exact issues:** (1) BD0-15 required `UNPROVED → PROVED → REVIEWED` during WP-1 but stood `UNPROVED`. (2) Literature freeze terminal states ambiguous: L1 `UNFROZEN_PAYWALL`, L4 `DOI unfrozen`, against the required per-source `source_id / citation / version-date / retrieval-location / retrieval-timestamp / SHA-where-bytes / sections / role` record. No WP-2 begun; no Bellman/kernel/candidate/holdout artifacts touched; all failed-run/stress evidence preserved.

**Exact repairs (narrow, fail-closed):**

1. **BD0-15 proved + reviewed:** rewrote `math/theorem_BD9_recency_v_blindness.md` as a complete proof (statement; state/action/cost defs for KEEP/DELETE with `a=c(A,x)`, KEEP `y=c(B,x)`, DELETE `y=0`, `w_b`, `V_b^R` recursion; 8-step proof of points 1–8 with deterministic recency updates not affecting actions/transitions/regret; limitations incl. `U_b^R` separation allowed; explicit non-converse note; `V` consequence; canary consequence `RECENCY_V_CANARY_FAIL`; no-uselessness disclaimer). Theorem SHA-256 `51352C452EF69A5D04A389939DE1ED2F2461F2261AD8677CE50CE18D0AFB85A0`. `math/proof_status.json` BD0-15 now carries `history: [UNPROVED@2026-09-22T16:00:00Z, PROVED@2026-09-22T16:32:00Z, REVIEWED@2026-09-22T16:33:00Z]`, `proof_sha256` matching bytes, `review` pointer, final `REVIEWED` — lifecycle preserved, not overwritten. New independent test `tests/parent/test_bd015_recency_v_blindness.py` (5 checks: existence, SHA match, implication present, converse absent, REVIEWED+lifecycle) — 5/5 green. `scripts/check_phase00.py` now gates BD0-15==REVIEWED + lifecycle + SHA + implication/converse asserts (lines :73–:84).
2. **Literature frozen explicitly + SA-02:** retrieved public CC-BY L4 PDF (`https://drops.dagstuhl.de/storage/00lipics/lipics-vol173-esa2020/LIPIcs.ESA.2020.28/LIPIcs.ESA.2020.28.pdf`, 932849B, SHA `7E97911B4BF2C4A39FCAE1AB2630424C3F09DCDC1281470DD71F07DE83A38458`, LIPIcs Vol.173 ESA2020 pp.28:1–28:16, pub. 2020-08-26) to `external/papers/L4_geometric_inversions_2020.pdf` (no paywall bypass; CC-BY 3.0). L1 kept byte-free deliberately (ACM paywall not bypassed) and frozen by `BIBLIOGRAPHIC_IDENTITY` (JACM 32(3):652–686, DOI 10.1145/3828.3835, metadata endpoint, timestamp 2026-09-22T16:35:00Z, CONTEXT role, bottom-up definition reliance, `local_bytes_present:false`). New ratified `SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.2.md` (SA-02) defines `LOCAL_BYTES / PARENT_INHERITED_BYTES / BIBLIOGRAPHIC_IDENTITY`; base + SA-01 bytes preserved. `external/MANIFEST.json` now: L0 PARENT_INHERITED_BYTES/FROZEN, L1 BIBLIOGRAPHIC_IDENTITY/FROZEN, L2 PARENT_INHERITED_BYTES/FROZEN (`F7AA7901...340C36F1C` re-verified), L3 PARENT_INHERITED_BYTES/FROZEN (`60B3213D...E7C5E7` re-verified), L4 LOCAL_BYTES/FROZEN; no row remains PAYWALL-only or DOI_UNFROZEN. `SHA256SUMS` (3 lines, BOM-free), `CITATIONS.md` (methods per source) updated. No normative prereg file changed, so `prereg_sha256.txt` unchanged (`9526EF9A...D846244`, re-verified).

**Files changed:** `math/theorem_BD9_recency_v_blindness.md` (full proof), `math/proof_status.json` (lifecycle+SHA), `tests/parent/test_bd015_recency_v_blindness.py` (new), `scripts/check_phase00.py` (REVIEWED+SHA+literature asserts, new [WP1-CHK-05] literature/:73, gate-pass moved to [WP1-CHK-06]/:118), `scripts/check_reseal_acceptance.py` (new, A1–A20), `SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.2.md` (new SA-02), `external/MANIFEST.json`, `external/papers/L4_geometric_inversions_2020.pdf` (new), `external/papers/SHA256SUMS`, `CITATIONS.md`, `CHANGELOG.md`, `artifacts/v02/logs/phase00_gate.json` (REVIEWED+literature block), `artifacts/v02/logs/phase00_reseal.json` (new, RESEAL_PASS), `Path.md` (this entry).

**Commands run:** `Invoke-WebRequest <L4-PDF>`, `python scripts/check_phase00.py` (FOUNDATION_SEALED), `python scripts/check_reseal_acceptance.py` (RESEAL_PASS A1–A20), `python -m pytest tests/parent -q` (11/11), `python scripts/stress_phase00.py` via acceptance (STRESS_PASS), `python -m pytest tests/parent/test_bd015_recency_v_blindness.py -v` (5/5), out-discipline probes (9 dirs all False), `git status` (clean after commit).

**Console.log lines (new/changed, `print()` via `console_log()` with `# console.log equivalent [ID]`):** `scripts/check_phase00.py`:28 [WP1-CHK-01], :35 [WP1-CHK-02], :39 [WP1-CHK-03], :42 [WP1-CHK-04], :73 [WP1-CHK-05] literature, :118 [WP1-CHK-06] pass; `scripts/check_reseal_acceptance.py`:24 [WP1-ACC-01], :28 [WP1-ACC-02] A1–A5, :45 [WP1-ACC-03] A6–A9, :56 [WP1-ACC-04] A10–A13, :66 [WP1-ACC-05] A14–A18, :91 [WP1-ACC-06] A19–A20, :102 [WP1-ACC-07] pass; `tests/parent/test_bd015_recency_v_blindness.py`:32 [WP1-BD15-01], :40 [WP1-BD15-02], :48 [WP1-BD15-03], :56 [WP1-BD15-04], :66 [WP1-BD15-05], :76 [WP1-BD15-06]. Prior 33 WP-1 IDs unchanged (see WP-1 entry).

**Test/stress results:** gate FOUNDATION_SEALED (PARENT-01..06 True, BD0-15 REVIEWED, threat/stop sets exact, L0–L4 methods/status block); acceptance RESEAL_PASS (20/20 A1–A20); pytest 11/11 (6 parent + 5 BD0-15); stress STRESS_PASS (6 checks incl. rerun-identical JSON, 9-file manifest, out-discipline, 12 schemas, L2 agreement). H1 firewall still `EMPTY`/`unlock:null`, commitment unchanged; n8 still contaminated; parent snapshot still locked (bootstrap manifest rewrites deterministically identical); no WP-2+ artifacts (9 dirs probed False).

**Deviations/amendments:** SA-02 added (literature methods; base+SA-01 preserved, reason documented, gates reference amended stack). No WorkPlan edit (v0.2.1 already permits honest ledger + UNPROVED→REVIEWED lifecycle; SA-02 is a docs clarification recorded here). No deviation-log row (all work per plan + audit task).

**Follows WorkPlan.md?** YES — reseal executes WorkPlan §§3/10/11 plus the audit task narrowly: BD0 lifecycle honored, no premature WP-2, no holdout contact, append-only evidence, fail-closed gates. No deviation. Next: WP-2 (still not begun).

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

**Scope per WorkPlan.md §6:** BD0-06/07 + BD0-15 (one-way R_π; UNPROVED→PROVED→REVIEWED in WP-1) proved first; augmented reachability n=2,3,4 (+5 stretch) with parent-witness/closure; augmented b=2 geometry; SA-01 canary (same-(A,B) zero-V-spread assert; nonzero ⇒ RECENCY_V_CANARY_FAIL); H2R generation+quarantine BEFORE synthesis (120k / 4,080,000, stratified, commitment, firewall EMPTY→COMMITTED→FROZEN→UNLOCKED_ONCE); blind recency ontology (heap/crossing/nested/rank/inversion/heavy/multiscale, tie audit, S-vs-R ablation); atom discovery (eligibility, creation/repayment, V-tight diagnostics, scale audit, exhaustion).
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
