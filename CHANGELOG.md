# CHANGELOG

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
