# BELLMAN_DEBT_REPORT.md — SPLAY-AM-BD v0.2 canonical debt geometry (CERTIFIED FACT)

Anchor `b=2/1`, `n=2..7`. All inequalities independently verified (object core
+ dict-core audit); fixed points exact; witnesses preserved.

| n | R | maxU_2 | maxV_2 | KEEP_EXCESS | EXACT_V_REPAYMENT | DELETE_CREATION | maxExcess | maxDelDV | V-tight | U-tight |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 |
| 3 | 19 | 10 | 1 | 4 | 4 | 12 | 1 | 1 | 12 | 14 |
| 4 | 196 | 22 | 2 | 72 | 72 | 228 | 2 | 2 | 160 | 194 |
| 5 | 1764 | 38 | 3 | 938 | 894 | 3060 | 3 | 3 | 1614 | 1910 |
| 6 | 17424 | 44 | 5 | 11768 | 10478 | 40148 | 4 | 5 | 17326 | 19636 |
| 7 | 184041 | 58 | 6 | 151534 | 124728 | 529016 | 5 | 6 | 193512 | 210642 |

Secondary panel `5/2, 3, 4` solved on `n=2..6` (all feasible); `n=7` skipped
(`ROBUSTNESS_PANEL_INCOMPLETE`, anchor authoritative). Monotonicity across `b`
recorded as FINITE_OBSERVATION only.

Evidentiary status: FINITE_OBSERVATION / CERTIFIED FACT on stated domains.
No universal closed form is claimed for `V_2`.
