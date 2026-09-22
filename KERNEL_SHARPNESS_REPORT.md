# KERNEL_SHARPNESS_REPORT.md — behavioral quotient + ablation (FINITE OBSERVATION)

## Behavioral quotient (target-independent, dual-implementation agreement)

| n | states | classes | compression | largest | singletons |
|---|---|---|---|---|---|
| 2 | 4 | 4 | 1.0 | 1 | 4 |
| 3 | 19 | 19 | 1.0 | 1 | 19 |
| 4 | 196 | 196 | 1.0 | 1 | 196 |
| 5 | 1764 | 1764 | 1.0 | 1 | 1764 |
| 6 | 17424 | 17424 | 1.0 | 1 | 17424 |
| 7 | 184041 | 184041 | 1.0 | 1 | 184041 |

Result: KERNEL_NO_COMPRESSION (1 refinement round everywhere).
V-transport APPLICABLE by method (BD0-04 REVIEWED); U-transport
BLOCKED_BY_SOURCE_CONTRACT (BD0-05 REVIEWED, quotient lacks source treatment).

## K0 ablation (COMPONENTWISE_NECESSARY_FINITE, never global minimality)

Every K0/removal verdict: KERNEL_TRANSITION_INSUFFICIENT at every n.
K0_full witnesses (diagonal pairs): (0,3), (0,6), (0,15), (0,43), (0,133), (0,430).
Lesson: pure-difference features collapse synchronized states; absolute shape
coordinates are the identified missing distinction (not a sufficiency theorem).

## Recency

Augmented states: n2 20, n3 235, n4 8764, n5-stretch 496264.
SA-01 canary GREEN (4/19/196 groups, zero V-spread).
Atoms D1–D7: all DEBT_ATOM_FAMILY_INCONSISTENT (exact counters preserved;
D5_rank repay 3318/3334 at n4 is a near-miss, not a survivor).
