# CHANGELOG

## WP-4 (2026-09-22)
- GATED_PASS: BD0-06/07 REVIEWED (SHA 2E4ED189.../866C4E56...); augmented n2/3/4 (20/235/8764) + n5 stretch (496264); b=2 geometry + canary GREEN (4/19/196 groups); H2R 120k/4.08M committed, BANK_COMMITTED, discovery-blind; 14-stat recency ontology; atoms D1-D7 all INCONSISTENT (D5 repay 99.5% near-miss); R/D/HLD 21/21 + full 70/70 + STRESS_PASS. Bugs closed: heap key mismatch, markdown-normalize in review checks.

## WP-3 theorem closure (2026-09-22)
- BD0-04 REVIEWED (SHA 1CC8663E...F1C0ACFC2) + BD0-05 REVIEWED (SHA 4ED550C1...37C9CFB2), lifecycles preserved; future-vs-source distinction explicit.
- Quotient audit: V_TRANSPORT_APPLICABLE (method-correct, vacuous on singletons), U_TRANSPORT_BLOCKED_BY_SOURCE_CONTRACT (no redesign). Findings preserved; BD0-06..14 untouched (BD0-10 option B).
- Re-ran: phases 04-07 PASS, pytest 43/43, stress + gate-matrix + byte audit PASS. Only transport labels changed (documented). H1 EMPTY, no WP-4 artifacts. Hygiene policy docs/large_file_hygiene.md.

## WP-3 (2026-09-22)
- GATED_PASS: blind 39-scalar ontology n=2..7; quotient KERNEL_NO_COMPRESSION (classes==R, dual-agreement, transport BLOCKED on BD0-04/05); K0 ablation (all TRANSITION_INSUFFICIENT, diagonal-collapse lesson); delta mining winner (rank_sign_neg,+1) with n6/n7 streamed validation (35-45%); ST/K 16/16 + BD 10/10 + STRESS_PASS. Bugs closed: docstrip audit, report keys, test shadowing, one real symmetry bug (one-sided nesting fixed, rebuild stable).

## WP-2 theorem closure (2026-09-22)
- BD0-02 REVIEWED (theorem_BD2 SHA B3AD40D8...FA48F9) + BD0-03 REVIEWED (theorem_BD3_past_slack SHA 95A15388...99D278), lifecycles preserved; corridor corollary joint in BD0-02 (upper) + BD0-03 (past), pair-state-only with BD0-13 guard.
- Independent review 6/6 + byte audit green; gate matrix prereg/theorem_gate_matrix.yaml (BD0-01..15, fail-closed consumers); BD0-04..14 remain UNPROVED.
- Re-ran: phase01 identical, pytest 27/27, stress STRESS_PASS, gate matrix PASS. H1 EMPTY, no WP-3 artifacts.

## WP-2 (2026-09-22)
- GATED_PASS: anchor b=2 n=2..7 verified (R exact, maxU/V match, Bellman fixed points green); BELL-SIG 203911 rows + extremal specimens + trajectories; panel 5/2,3,4 solved n=2..6, n=7 skipped (ROBUSTNESS_PANEL_INCOMPLETE); independent dict-core audit PASS n=2..6; BD-01..10 10/10; stress STRESS_PASS. Bugs closed: sparse pair_id sizing, import-scan precision.

## WP-1 reseal (2026-09-22)
- BD0-15 UNPROVED -> PROVED -> REVIEWED: full one-way R_pi proof in math/theorem_BD9_recency_v_blindness.md (SHA 51352C45...AFB85A0) + independent test tests/parent/test_bd015_recency_v_blindness.py (5/5).
- Literature: SA-02 (SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.2.md) freeze methods; L1 BIBLIOGRAPHIC_IDENTITY (DOI 10.1145/3828.3835, no paywall bypass); L4 LOCAL_BYTES (CC-BY PDF, SHA 7E97911B...A38458); L2/L3 PARENT_INHERITED_BYTES re-verified; MANIFEST + SHA256SUMS + CITATIONS updated.
- Gates: check_phase00 (REVIEWED + literature asserts), check_reseal_acceptance A1-A20 RESEAL_PASS, pytest 11/11, stress PASS. H1 EMPTY, no WP-2+ artifacts.

## v0.2.1 (2026-09-22)
- Audit follow-up: R_pi one-way wording, multi-phase matrices with set-based seal, BD0-15 UNPROVED with theorem_BD9.
- Audit remediation: SA-01 recency-V blindness, parent bootstrap lock, transcendental branch, STOP corrections, threat and discovery-split matrices.

## v0.2.0 (2026-09-22)
- Initial WorkPlan and Path freeze: 6-phase plan covering SPEC PHASE 00-18.

## WP-1 (2026-09-22)
- Foundation seal: parent bootstrap verification, spec freeze, literature ledger, prereg freeze, theorem ledger BD0-01..15.
