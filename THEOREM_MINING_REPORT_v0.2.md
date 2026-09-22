# THEOREM_MINING_REPORT_v0.2.md — full mining record with claim labels

## A. Parent v0.1 facts inherited (CERTIFIED FACT)
R 4/19/196/1764/17424/184041; b* 1,1,3/2,8/5,8/5,23/14; b=2 maxU/maxV/forced
per BELLMAN_DEBT_REPORT; H-0001..0006 rejected (supplementary).

## B. b=2 Bellman debt geometry (CERTIFIED FACT)
Table in BELLMAN_DEBT_REPORT.md; Bellman equalities verified exactly.

## C. Debt-creation DELETE edges (FINITE OBSERVATION)
Counts per n in table B; canonical witnesses in artifacts/v02/specimens.

## D. Debt-repayment KEEP edges (FINITE OBSERVATION)
EXACT_V_REPAYMENT counts per n in table B.

## E. V-tight structural motifs (FINITE OBSERVATION)
V-tight/U-tight counts per n in table B; motif predicates per mode in debt_atoms.

## F. Behavioral quotient (CERTIFIED FACT on method; FINITE OBSERVATION on values)
KERNEL_NO_COMPRESSION; dual agreement; transport audit in kernels/transport_audit.json.

## G. Pair-state kernel insufficiency witnesses (FINITE OBSERVATION)
K0_full diagonal witnesses per n; COMPONENTWISE_NECESSARY_FINITE only.

## H. Recency augmentation results (CERTIFIED FACT on canary; FINITE OBSERVATION else)
States 20/235/8764 (+496264 stretch); canary GREEN; U-spread is history-cost data.

## I. Recency/crossing/inversion/gap-inspired atoms (FINITE OBSERVATION)
14 recency stats; D1–D7 coverage tables in debt_atoms/recency_atoms.json.

## J. Exact inconsistent atom families (CERTIFIED FACT on verdicts)
All D1–D7 DEBT_ATOM_FAMILY_INCONSISTENT with exact counters.

## K. Surviving debt laws (HYPOTHESIS: none)
Zero survivors; ledger in HYPOTHESIS_LEDGER.md.

## L. Fresh holdout outcomes (CERTIFIED FACT)
None consumed: H1 UNREAD, H2R BANK_COMMITTED/0, n8 UNCONTACTED.

## M. Adversarial counterexamples (HYPOTHESIS: none sought)
Campaign NOT_ACTIVATED (no survivors).

## N. Universal proof status (PROVED THEOREM: none)
No Pair Access proof attempted (no object). BD0-08/09/11/12/14 stay UNPROVED legitimately.

## O. Negative-family status (PROVED THEOREM: none)
C1–C4 all false; no actual-cost motif. H-residual failures are not ratio motifs.

## P. New mathematical questions (HEURISTIC/CONTEXT)
1. Absolute-coordinate kernels for transition preservation.
2. Why rank_sign_neg tracks ~40% of debt deltas.
3. Whether any compact recency accounting makes KEEP/DELETE deltas transparent.

## Tables A–H (§34, exact integers; display decimals labeled)
- A (foundation): R per n above; b* per n above; maxU/maxV/forced per table B.
- B (creation/repayment): table B in BELLMAN_DEBT_REPORT.md.
- C (tight geometry): V-tight/U-tight/both per table B + phase03 summaries.
- D (quotient): table in KERNEL_SHARPNESS_REPORT.md.
- E (kernel sharpness): all-TRANSITION verdicts + diagonal witnesses above.
- F (recency): states/canary/maxU/maxV per phase08 summaries.
- G (atoms): n4 create/repay fractions in WP-4 entry; full tables in recency_atoms.json.
- H (candidates): HYPOTHESIS_LEDGER.md table.

## Purpose questions Q1–27 (§36, answered from artifacts alone)
1. Parent seal imported exactly? Yes (BOOTSTRAP_MANIFEST + PARENT-01..06).
2. What does V_b mean? Maximum finite-state future b-regret (BD0-02 REVIEWED).
3. Where is future regret created by DELETE? DELETE_CREATION tables per n.
4. Where repaid by KEEP? EXACT_V_REPAYMENT tables per n.
5. Which transitions are Bellman-tight? V-tight/U-tight tables per n.
6. What target-blind quotient preserves dynamics? Primitive cost/successor partition (singletons).
7. How much compression? None (1.0 at all n).
8. Which coordinates are componentwise necessary? All removals fail (transition-type witnesses).
9. Which pair-state kernels fail, with witnesses? K0 + removals, diagonal pairs.
10. Does recency add finite identification power beyond (A,B)? For V: no (canary GREEN); for accounting: open.
11. What recency distinction matters? None for V; violation counts track debt partially (finite).
12–13. Which atoms track/track-fail debt changes? D5/D3 partial; all families exactly inconsistent.
14–15. Survivors/killers? Zero survivors; killers listed in ledger.
16. Correct fresh holdout per track? None needed (no survivors); wiring verified (H1↔S, H2R↔R).
17. Independent/adversarial survivors? None (agreement held; campaign gated).
18–20. Proved for arbitrary n? No. KEEP+DELETE under one b? No object. Telescope? No.
21–22. Monotonicity/DOC? Neither proved nor disproved.
23–25. Actual-cost motif/closed form/divergence? None observed; not attempted.
26. Strongest artifact-justified claim? FINITE_DEBT_LAW_MINING_RESULTS.
27. Reproducible from fresh checkout? Yes (REPRODUCIBILITY.md + reproduce_all_v0.2.sh).
