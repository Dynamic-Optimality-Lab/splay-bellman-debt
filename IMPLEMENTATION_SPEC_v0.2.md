# SPLAY-AM-BD v0.2: Bellman Debt Discovery, Kernel Identification, and Universal-Potential Experiment

**Document type:** Frozen mathematical implementation specification / preregistration blueprint  
**Target problem:** Sleator-Tarjan Dynamic Optimality Conjecture for ordinary bottom-up Splay  
**Primary bridge theorem:** Levy-Tarjan approximate monotonicity <=> dynamic optimality for Splay, under an explicitly audited convention match  
**Experiment short name:** `SPLAY-AM-BD-v0.2`  
**Parent experiment:** `SPLAY-AM-PD-v0.1`, sealed at repository commit `6de1ca2`  
**Parent terminal claim:** `FINITE_EXACT_BN_RESULTS`  
**Parent role:** immutable certified evidence and infrastructure source; never rewritten as v0.2 evidence  
**Primary discovery anchor:** exact fixed-constant Bellman geometry at `b = 2`  
**Primary semantic object:** canonical future competitive regret `V_b`, interpreted operationally as finite-state deletion debt  
**Primary dual object:** canonical past slack `U_b`, interpreted as the maximum admissible creation budget for a normalized feasible potential  
**Primary theorem-mining target:** a compact structural or history-augmented kernel whose exact transition law realizes Bellman debt and can be lifted to a universal Pair Access potential  
**Experimental style:** deterministic, exact, certificate-first, fail-closed, counterexample-guided, two-implementation verification, strict holdout firewalls  
**Primary implementation language:** Python for transparent v0.2 theorem discovery and independent audit; parent v0.1 exact core is inherited read-only; optional Rust acceleration is permitted only behind exact-agreement gates  
**Number of implementation phases:** 19 (`PHASE 00` through `PHASE 18`)  
**Core rule:** the experiment may discover a theorem, disprove a candidate representation, or end with only finite structural results. It may never turn finite Bellman tables, heuristic feature importance, a surviving holdout, or repeated numerical patterns into a universal claim.

---

# 0. Executive purpose

`SPLAY-AM-PD-v0.1` answered its preregistered question cleanly.

It produced an exact paired-Splay transition system, exact finite subsequence overheads through `n=7`, canonical Bellman potential geometry, critical derivatives, feature-language obstruction results, and six frozen universal-potential candidates. The final six candidates all failed the corrected `b_H=2` canonical sandwich gate. The experiment therefore sealed with zero positive theorem candidates and no activated infinite negative family.

The scientific lesson is not:

> "Potential functions do not work."

Nor is it:

> "Dynamic optimality is probably false."

The actual lesson is:

> **The first explicit structural languages did not represent the quantity that the exact Bellman dynamics require.**

The new experiment therefore changes the discovery question.

v0.1 asked:

```text
Which hand-designed structural statistic can serve as H?
```

v0.2 asks:

```text
What conserved combinatorial resource are the canonical Bellman equations already measuring?
```

The primary conceptual interpretation is **deletion debt**.

A request present in the full sequence `X` but deleted from the subsequence `Y` restructures the full-sequence Splay tree `A` while the subsequence tree `B` does nothing. That deleted request can make future accesses in `B` more expensive than the corresponding accesses in `A`. The missing restructuring has therefore created a future competitive liability.

v0.2 treats the canonical future-regret value

```math
V_b(s)
```

as the exact finite operational meaning of that liability:

> the maximum additional `b`-competitive regret that can still be extracted from state `s`.

The end-to-end scientific chain is frozen as:

```math
\boxed{
\text{sealed v0.1 pair dynamics}
\to
\text{fixed-}b\text{ Bellman debt}
\to
\text{exact debt-creation/repayment specimens}
\to
\text{structural / recency kernel}
\to
\text{candidate conserved resource }\Phi
\to
\text{universal KEEP/DELETE law}
\to
\text{approximate monotonicity}
\to
\text{dynamic optimality}
}
```

The intended positive endpoint is one universal constant `b<infinity` and one mathematically explicit potential on a declared Markov state `z`,

```math
\Phi(z)\ge 0,
```

with zero initial potential, such that every legal paired Splay step obeys:

KEEP:
```math
c(B,x)+\Phi(z')-\Phi(z)\le b\,c(A,x),
```

DELETE:
```math
\Phi(z')-\Phi(z)\le b\,c(A,x).
```

The primary state track is the ordinary pair state

```math
z=(A,B).
```

A separately gated augmented track is allowed:

```math
z=(A,B,\rho_X,\rho_Y),
```

where `rho_X,rho_Y` are exact finite relative-recency states defined later. History may not be silently introduced in any other form.

If those inequalities are proved for arbitrary `n` and every legal state in the declared domain, then along every full sequence `X` and subsequence `Y <= X`:

```math
\operatorname{Splay}(Y,T)
+
\Phi(z_m)-\Phi(z_0)
\le
b\,\operatorname{Splay}(X,T).
```

With

```math
\Phi(z_0)=0,\qquad \Phi(z_m)\ge0,
```

this yields

```math
\operatorname{Splay}(Y,T)
\le
b\,\operatorname{Splay}(X,T).
```

That is approximate monotonicity under the frozen convention. Only after the convention audit may the Levy-Tarjan bridge be invoked to claim dynamic optimality.

The intended negative endpoint remains an explicit infinite family

```math
(T_k,X_k,Y_k),\qquad Y_k\preceq X_k,
```

with

```math
\frac{\operatorname{Splay}(Y_k,T_k)}
     {\operatorname{Splay}(X_k,T_k)}
\to\infty.
```

Finite failure of a kernel, finite failure of a potential, a positive-regret cycle for one fixed `b`, or increasing finite residuals are **not** a disproof.

The v0.2 experiment is therefore deliberately allowed to end at any of these scientifically meaningful points:

```text
- exact Bellman-debt characterization only;
- exact structural-kernel insufficiency witnesses;
- exact proof that recency information is necessary for a stated representation family;
- a finite-surviving candidate conserved resource;
- a universal Pair Access proof;
- a proved unbounded negative family;
- resource-limited or representation-inconclusive result.
```

The experiment fails open to new mathematics and fails closed to theorem claims.

---

# 1. Scientific scope and non-goals

## 1.1 Primary scientific question

For the paired Splay dynamics inherited from v0.1 and a fixed candidate constant `b`, define:

```math
w_b(e)=y(e)-b\,a(e),
\qquad
\ell_b(e)=b\,a(e)-y(e).
```

The primary canonical finite-state values are:

```math
U_b(s)=
\inf_{P:\Delta_n\rightsquigarrow s}
\sum_{e\in P}\ell_b(e),
```

and

```math
V_b(s)=
\sup_{P:s\rightsquigarrow *}
\sum_{e\in P}w_b(e),
```

where the empty future is allowed in `V_b`.

The central v0.2 questions are:

1. What exact structural events cause `V_b` to increase after DELETE?
2. What exact structural events cause `V_b` to decrease when a KEEP access pays excess cost?
3. Which edges are Bellman-tight for `V_b`, and what structural object changes exactly enough to pay their regret?
4. Which primitive coordinates are necessary to distinguish states requiring different future debt?
5. Is there a nontrivial structural quotient that preserves paired transition costs and successor behavior?
6. Can a compact kernel explain `V_b`, `U_b`, or at minimum the edgewise amortization law without reading those values?
7. If pair state `(A,B)` is insufficient for a natural law, does relative access recency provide the missing Markov information?
8. Can the discovered debt object be written as an `n`-independent mathematical function?
9. Can its KEEP and DELETE changes be proved universally?
10. If every plausible debt language fails, do the failures expose a scalable **Splay-cost** obstruction rather than merely a representation obstruction?

## 1.2 Primary discovery anchor versus final theorem constant

The exact geometry at

```math
b_{\rm anchor}=2
```

is the primary discovery anchor because:

```text
- it is a simple n-independent constant;
- v0.1 certified b_n^* < 2 for n=2..7;
- v0.1 already computed and independently verified the b=2 U/V geometry through n=7;
- it avoids fitting the geometry itself to each n.
```

Hard rule:

```text
b=2 is a discovery anchor, not a theorem assumption.
```

A final theorem candidate may use another universal constant

```math
b_H\in\mathbb Q_{>0}
```

or, after an explicit proof-system extension, another exactly specified real constant.

Any change of candidate constant creates a new hypothesis version.

## 1.3 Secondary fixed-b robustness panel

To test whether a discovered structural explanation is an artifact of the anchor constant, v0.2 preregisters the secondary exact panel

```text
b = 5/2
b = 3
b = 4
```

on development sizes where resources permit.

These values are diagnostics. They are not candidate tuning knobs.

If resource limits prevent full secondary geometry, `b=2` remains the authoritative discovery anchor and the missing panel is reported as `ROBUSTNESS_PANEL_INCOMPLETE`.

## 1.4 What v0.2 does not claim

The experiment does **not** claim:

```text
- that V_2 itself has a simple closed form;
- that a structural statistic correlating with V_2 is a potential;
- that the canonical b=2 geometry persists qualitatively for all n;
- that b=2 is the true or minimal universal approximate-monotonicity constant;
- that history or recency is necessary merely because state-only candidates failed in v0.1;
- that recency order alone is sufficient merely because it improves finite prediction;
- that O(n) potential range is logically required by the zero-initial primary Pair Access certificate;
- that a finite behavioral quotient automatically has an n-independent description;
- that a candidate passing H1 or H2R is universal;
- that a positive-regret cycle for one fixed b disproves dynamic optimality;
- that failure to find a potential implies the conjecture is false;
- that a black-box predictor is a mathematical explanation;
- that a literature-inspired quantity keeps its original theorem semantics after being transplanted into the paired setting.
```

---

# 2. Parent experiment and inherited evidence

## 2.1 Parent identity

The parent experiment is:

```text
experiment_id: SPLAY-AM-PD-v0.1
sealed_commit: 6de1ca2
terminal_claim: FINITE_EXACT_BN_RESULTS
```

The exact parent archive hash, manifest hash, frozen specification hashes, amendment hashes, final-result hash, and repository remote commit must be loaded from the sealed parent artifacts during Phase 00.

No shortened hash printed in prose is authoritative.

## 2.2 Parent facts expected for import

The following are expected parent facts and must be independently revalidated against the parent seal before they become `CERTIFIED_PARENT_FACT` in v0.2.

Exact reachable-pair counts:

```text
n=2:       4
n=3:      19
n=4:     196
n=5:    1764
n=6:   17424
n=7:  184041
```

Exact finite subsequence overheads:

```math
b_2^*=1,\quad
b_3^*=1,\quad
b_4^*=\frac32,\quad
b_5^*=\frac85,\quad
b_6^*=\frac85,\quad
b_7^*=\frac{23}{14}.
```

Parent `b=2` canonical-geometry summary:

```text
n                 2   3   4    5     6      7
max U_2           4  10  22   38    44     58
max V_2           0   1   2    3     5      6
forced states     2   5  14   42   132    429
```

The expected forced-state count equals the Catalan diagonal count in each certified size.

Parent WP-5 candidate outcome:

```text
H-0001  UH-4 upper failure, first n=5
H-0002  UH-4 upper failure, first n=4
H-0003  UH-4 upper failure, first n=4
H-0004  UH-4 lower failure, first n=5
H-0005  UH-4 lower failure, first n=5
H-0006  UH-4 upper failure, first n=3
```

All six were ultimately rejected. Their preserved UH-5 counterexamples remain downstream supplementary evidence.

## 2.3 Parent facts are evidence, not editable inputs

Parent artifacts are read-only.

v0.2 may:

```text
- verify parent hashes;
- deserialize certified tables;
- derive new v0.2 artifacts from them;
- cite parent counterexamples;
- reproduce selected parent checks;
- copy parent records into a v0.2 import ledger with source hashes.
```

v0.2 may not:

```text
- rewrite parent JSON;
- replace a parent counterexample;
- relabel a parent finite result;
- edit a parent candidate;
- change a parent status;
- repair a parent artifact in place;
- silently use a newly recomputed table as if it were the parent table.
```

Any discovered parent defect triggers:

```text
PARENT_SEAL_MISMATCH
```

and blocks v0.2 theorem-facing execution until resolved by a separately versioned parent erratum.

## 2.4 Holdout inheritance

Two parent validation resources require special treatment.

### n8

The `n=8` exhaustive pair domain is permanently labeled:

```text
PARTIALLY_REVEALED_CANARY_CONTAMINATED
```

because detailed H=0 canary information was exposed during v0.1.

It may be used only as:

```text
CONTAMINATED_EXHAUSTIVE_VALIDATION
```

after a v0.2 candidate is frozen.

It may never be called a fresh holdout.

### HOLDOUT-H1-v0.1

The parent state-only holdout bank remains eligible as a fresh v0.2 holdout only if Phase 00 verifies:

```text
firewall_state == EMPTY
unlock_record == null
bank commitment hash matches parent
no v0.2 discovery namespace has read detailed bank content
```

H1 is valid only for candidate potentials computable from pair state `(A,B)` and its legal next transition.

H1 is **not** a valid fresh test for a potential requiring recency/history fields that are not stored in H1.

---

# 3. Frozen literature sources

v0.2 freezes the exact source versions used for logical bridges or structural inspiration.

Required source set:

```text
L1  Sleator & Tarjan (1985)
    Self-Adjusting Binary Search Trees

L2  Levy & Tarjan
    A Foundation for Proving Splay is Dynamically Optimal
    frozen chosen version of arXiv:1907.06310

L3  Chmel, Haeupler, Hladik, Koucky, Roeyskoe, Rozhon, Sladky, Tarjan (2026)
    Splay trees are almost dynamically optimal
    frozen chosen version of arXiv:2607.18498

L4  Chalermsook & Jiamjitrak (ESA 2020)
    New Binary Search Tree Bounds via Geometric Inversions
    DOI 10.4230/LIPIcs.ESA.2020.28

L0  SPLAY-AM-PD-v0.1 sealed release
    commit 6de1ca2
```

For each source store:

```text
source_id
canonical citation
exact version/date
retrieval location
retrieval UTC timestamp
local SHA-256
sections/theorems actually relied upon
logical role: PREMISE | CONTEXT | FEATURE_INSPIRATION
```

Hard rule:

```text
FEATURE_INSPIRATION never silently becomes a theorem premise.
```

In particular:

```text
- L2 provides the approximate-monotonicity bridge after convention audit.
- L3 is current-frontier context and a source of rank/heavy/gap/bend ideas.
- L4 motivates inversion-style relative potentials and direct BST comparison.
- L1 provides classical Splay semantics/potential context.
```

Any transplant of an L3 or L4 object into the pair-state setting receives a new v0.2 name until a formal equivalence is proved. The implementation must not call a new statistic `gap`, `bend`, or `inversion` merely because it resembles the source quantity.

---

# 4. Frozen mathematical contract

This section is authoritative.

All v0.2 code inherits the parent definitions of:

```text
key universe [n]
BST universe T_n
canonical tree encoding
root depth 0
cost c(T,x)=depth_T(x)+1
ordinary bottom-up Splay S_x(T)
sequence cost
position-based subsequence
pair state (A,B)
diagonal set Delta_n
KEEP and DELETE transitions
pair IDs
reachable domain R_n
path-to-sequence decoding
exact rational arithmetic conventions
```

No v0.2 code may redefine any of these objects.

## 4.1 Pair transition

For pair state

```math
s=(A,B)
```

and key `x`:

KEEP:
```math
K_x(A,B)=(S_xA,S_xB),
```

with

```math
a=c(A,x),\qquad y=c(B,x).
```

DELETE:
```math
D_x(A,B)=(S_xA,B),
```

with

```math
a=c(A,x),\qquad y=0.
```

## 4.2 Regret and slack

For fixed `b`:

```math
w_b(e)=y(e)-b\,a(e),
```

```math
\ell_b(e)=b\,a(e)-y(e)=-w_b(e).
```

The edge potential constraint is:

```math
w_b(e)+\Phi(t)-\Phi(s)\le0.
```

Equivalent:

```math
\Phi(t)-\Phi(s)\le\ell_b(e).
```

## 4.3 Canonical past-slack value

```math
U_b(s)=
\inf_{P:\Delta_n\rightsquigarrow s}
\sum_{e\in P}\ell_b(e).
```

Interpretation:

> the minimum `b`-competitive slack that any legal history must spend to create state `s` from a synchronized start.

## 4.4 Canonical future-regret value

```math
V_b(s)=
\sup_{P:s\rightsquigarrow *}
\sum_{e\in P}w_b(e).
```

The empty continuation is allowed.

Interpretation:

> the maximum additional `b`-competitive regret that can still be extracted from the current state.

v0.2 calls this quantity:

```text
CANONICAL BELLMAN DEBT
```

when used in the deletion-debt interpretation.

This is an interpretation of the already defined value, not a new mathematical definition.

## 4.5 Bellman equations

For finite valid geometry:

```math
V_b(s)=
\max\left(
0,
\max_{e:s\to t}
\left[w_b(e)+V_b(t)\right]
\right).
```

Equivalently:

```math
V_b(t)-V_b(s)\le \ell_b(e)
```

for every edge.

For `U_b`:

```math
U_b(t)=
\min_{e:s\to t}
\left[
U_b(s)+\ell_b(e)
\right]
```

subject to the diagonal source boundary, with the usual multi-source interpretation.

## 4.6 Feasible-potential corridor

For normalized nonnegative pair-state potentials satisfying every edge constraint:

```math
V_b(s)\le H(s)\le U_b(s).
```

At `b=2`, v0.2 treats:

```math
\mathcal I_2(s)=[V_2(s),U_2(s)]
```

as the exact finite admissible corridor.

Hard rule:

```text
The corridor constrains pair-state potentials only.
It does not automatically constrain a potential on a larger augmented state.
```

## 4.7 Exact edgewise debt quantities

For every edge `e:s->t`, define:

```math
\Delta V_b(e)=V_b(t)-V_b(s),
```

```math
\Delta U_b(e)=U_b(t)-U_b(s),
```

```math
R^V_b(e)=w_b(e)+\Delta V_b(e)\le0,
```

```math
R^U_b(e)=w_b(e)+\Delta U_b(e)\le0.
```

Classify exact finite specimens:

```text
V_TIGHT:
  R^V_b(e)=0

U_TIGHT:
  R^U_b(e)=0

KEEP_EXCESS:
  mode=KEEP and w_b(e)>0

CANONICAL_REPAYMENT:
  mode=KEEP and w_b(e)>0 and Delta V_b(e)<0

EXACT_V_REPAYMENT:
  mode=KEEP and w_b(e)>0 and R^V_b(e)=0
  equivalently Delta V_b(e)=-w_b(e)

CANONICAL_CREATION:
  mode=DELETE and Delta V_b(e)>0

MAX_CREATION_TIGHT:
  mode=DELETE and Delta V_b(e)=b*a(e)

NO_DEBT_CHANGE:
  Delta V_b(e)=0
```

These are finite Bellman classifications, not universal structural laws.

## 4.8 Deletion-debt conservation target

The conceptual target is a structural function `D(z)` satisfying:

DELETE creation:
```math
D(z')-D(z)\le b\,c(A,x),
```

KEEP repayment:
```math
c(B,x)-b\,c(A,x)
\le
D(z)-D(z').
```

These are algebraically the Pair Access inequalities.

The experiment is specifically designed to identify the mathematical object whose changes make these statements natural rather than accidental.

---

# 5. State tracks

v0.2 has two explicitly separated state tracks.

## 5.1 Track S - pair-state structural debt

State:

```math
z_S=(A,B).
```

This is the direct continuation of v0.1.

Track S asks whether Bellman debt admits a natural state-only structural realization.

Permitted candidate information:

```text
tree shapes
key order
depth/ancestor/parent structure
subtree intervals
subtree sizes/rank encodings
all-next-key access-path geometry
crossing structure
relative heavy/light structure
formally mapped inversion/gap-like objects
other explicitly frozen state-only combinatorial data
```

Forbidden:

```text
path history
raw X/Y prefix
BFS parent
pair ID as a feature
U/V/G values inside the candidate definition
holdout membership
n-specific lookup tables
```

## 5.2 Track R - recency-augmented debt

Track R is not active merely because Track S is difficult.

It is preregistered because the literature and deletion-debt interpretation make relative access recency a plausible missing state variable.

State:

```math
z_R=(A,B,\rho_X,\rho_Y).
```

`rho_X` is the exact relative most-recent-access order of keys in the full prefix.

`rho_Y` is the exact relative most-recent-access order of keys in the retained subsequence prefix.

Track R candidate potentials may depend on these recency objects.

No other history representation is permitted without a new experiment version or ratified amendment.

## 5.3 Track separation

Every artifact declares:

```text
track: STATE_ONLY
```

or

```text
track: RECENCY_AUGMENTED
```

No result may pool the two tracks without explicit labeling.

A Track R success does not retroactively make a Track S candidate valid.

A Track S failure does not imply history is necessary.

---

# 6. Exact recency-state contract

## 6.1 Relative recency state

For an access prefix `P`, define:

```text
rho(P) = list of distinct keys that have appeared in P,
         ordered from most recently accessed to least recently accessed.
```

Keys never accessed are omitted from the list and are recoverable as the complement in `[n]`.

Thus:

```text
rho = []
```

initially.

Access update:

```text
update(rho,x):
    remove x from rho if present
    prepend x
```

This representation preserves the complete strict order of last-access times among seen keys.

All unseen keys are tied below all seen keys.

No absolute timestamp is retained.

## 6.2 Paired update

For KEEP `x`:

```text
A -> S_x(A)
B -> S_x(B)
rho_X -> update(rho_X,x)
rho_Y -> update(rho_Y,x)
```

For DELETE `x`:

```text
A -> S_x(A)
B -> B
rho_X -> update(rho_X,x)
rho_Y -> rho_Y
```

## 6.3 Initial augmented state

For arbitrary initial tree `T`:

```math
z_0=(T,T,[],[]).
```

A primary augmented potential must satisfy:

```math
\Phi(T,T,[],[])=0.
```

## 6.4 Relabeling invariance

Order-preserving relabeling must preserve every recency relation.

Order reversal is an optional symmetry with explicit key correspondence:

```math
x\mapsto n+1-x.
```

A candidate may not depend on literal integer names except through order position.

## 6.5 Unseen-key ties

A feature requiring a total priority order over unseen keys may not silently break ties.

It must choose one of:

```text
A. keep an explicit partial-order/tie state;
B. quantify over every legal unseen-key completion;
C. use a preregistered deterministic tie-break and label the feature
   TIE_BREAK_DEPENDENT_DIAGNOSTIC.
```

Only A or B may support a theorem claim unless the theorem proves tie-break invariance.

## 6.6 Recency-treap-like diagnostics

A BST that is key-ordered and heap-ordered by recency may be constructed as a diagnostic reference only after its tie semantics are fixed.

Such an object is never called the unique "ideal" Splay tree.

It is a reference object for testing whether Splay's structural debt correlates with recency-order violations.

---

# 7. Kernel and bisimulation contract

## 7.1 Structural kernel

A kernel version is a deterministic function:

```math
K_j: z\mapsto k.
```

A theorem-facing structural kernel may use only declared primitive coordinates.

It may not contain:

```text
U
V
G
Bellman-tight labels
candidate Phi value
state ID
hash of full state, except FULL_STATE control
holdout identity
future trajectory
```

## 7.2 Primitive action alphabet

For fixed labeled keys:

```text
actions = {(KEEP,x),(DELETE,x): x in [n]}.
```

For order-reversal quotienting, action correspondence is explicitly:

```math
(\text{mode},x)\leftrightarrow
(\text{mode},n+1-x).
```

## 7.3 Cost-preserving transition equivalence

States `z,z'` are kernel-equivalent only if, under the declared key correspondence:

```text
- every corresponding action is enabled;
- full-sequence access cost agrees;
- KEEP subsequence access cost agrees;
- DELETE subsequence cost is zero on both;
- successor kernel agrees for every action.
```

For Track R, recency updates are part of the successor state and must be preserved.

## 7.4 Exact behavioral quotient

v0.2 computes a target-independent finite behavioral partition by deterministic partition refinement.

Initial observable signature may contain only primitive immediate data:

```text
track
n
for each x:
  c_A(x)
  c_B(x)
action correspondence metadata
```

Refinement step:

```text
new_class(z) =
canonical(
    old_class(z),
    [(action, immediate costs, old_class(successor(z,action)))]
)
```

Iterate to a fixed point.

This partition is:

```text
BEHAVIORAL-QUOTIENT-v0.2
```

It is not defined using `U` or `V`.

## 7.5 Bellman transport theorem target

The formal note must prove:

> If two states are related by a cost- and action-preserving deterministic bisimulation, then for every fixed `b`, their canonical future-regret value `V_b` agrees; with compatible diagonal/source treatment, the corresponding `U_b` value agrees as well.

No finite quotient is interpreted before this theorem is `PROVED+REVIEWED`.

## 7.6 Structural explanation target

The scientific goal is not merely to compute the behavioral quotient.

It is to find a compact mathematical structural signature whose classes refine or coincide with the exact behavioral classes sufficiently to transport the required debt law.

The full state is a mandatory control and is not considered an explanatory discovery.

---

# 8. Bellman signatures and specimen taxonomy

## 8.1 Bellman signature

For analysis only, attach to each certified state:

```text
U_b
V_b
G_b
incoming U-tight action classes
outgoing V-tight action classes
outgoing regret spectrum
positive-excess KEEP count
DELETE debt-creation count
max exact KEEP excess
max exact Delta V on DELETE
min exact Delta V on KEEP
```

Call this:

```text
BELL-SIG-v0.2
```

Hard rule:

```text
BELL-SIG is a target label.
It may never be used as an input coordinate of a theorem-facing structural kernel.
```

## 8.2 Extremal transition tables

Preserve all edges in development sizes, but create canonical specimen tables for:

```text
all KEEP_EXCESS edges
all EXACT_V_REPAYMENT edges
all CANONICAL_CREATION DELETE edges
all V_TIGHT edges
all U_TIGHT edges
all edges simultaneously U_TIGHT and V_TIGHT
largest exact positive KEEP excess per n
largest exact DELETE Delta V per n
largest exact |Delta V| per structural action family
```

No percentile threshold is authoritative.

## 8.3 Canonical witness selection

When a table requires one representative:

```text
sort by:
n
source pair/state canonical ID
mode
key
target ID
```

and take lexicographically first among exact ties.

## 8.4 Transition explanation question

For every high-value specimen, the theorem-mining report must ask:

```text
What structural object appeared?
What structural object disappeared?
What structural object changed scale?
Did the change occur locally on the access path?
Did it involve nonadjacent ancestor/crossing structure?
Did a recency-order violation appear/disappear?
Did a nested interval family collapse?
Did a heavy/light or gap-like object change?
Can the change be charged to O(c_A) primitive events?
```

These questions are discovery prompts, not claims.

---

# 9. Structural ontology v0.2

All structural coordinates are versioned and defined before target joins.

## 9.1 Pair-tree primitives

Required exact state-only primitive families:

```text
S-depth
S-parent
S-ancestor
S-subtree-size
S-interval
S-all-next-key access paths
S-root relation
S-order-reversal symmetry
```

These inherit exact definitions from v0.1 where unchanged.

## 9.2 Relative classic-Splay rank primitives

The classical Splay potential motivates subtree-size/rank structure.

Authoritative exact storage uses:

```text
subtree size integers
ordered size pairs
reduced ratios
floor-log2 buckets as separately named integer features
symbolic log terms if a proof candidate explicitly requires them
```

A floating logarithm is never an authoritative exact candidate evaluation.

If a final formula uses `log`, finite residual signs require one of:

```text
- symbolic proof;
- certified interval arithmetic with directed rounding;
- exact transformation eliminating the transcendental comparison.
```

## 9.3 Recency-order primitives

For Track R:

```text
seen/unseen indicator
recency rank among seen keys
pairwise recency-order relation
rho_X vs rho_Y disagreement
last-access-order inversions
longest common recency prefix
relative age rank difference
keys seen in X but unseen in Y
```

No absolute time difference is present in the frozen state.

## 9.4 Heap-order violation primitives

Given a tree and a recency partial order:

```text
parent-child recency-correct
parent-child recency-violating
parent-child recency-unresolved due to unseen tie
```

Preserve counts and exact per-edge records.

Also define nonadjacent ancestor-order violations separately.

Do not collapse edge violations and ancestor violations under one feature name.

## 9.5 Crossing-depth primitives

Every crossing quantity must have a standalone mathematical definition.

At minimum instrument:

```text
ancestor relation disagreement depth
nearest common structural witness depth
nested interval crossing depth
recency violation crossing depth
access-path crossing depth
bounded per-node crossing-level indicators
```

If inspired by L2 terminology, the mapping must state exactly what is preserved and what is newly defined.

## 9.6 Interval/nesting debt primitives

Required:

```text
subtree interval in A
subtree interval in B
interval identity
strict-containment disagreement
nested disagreement chain length
nested family count
bounded per-key nesting-level charge
interval endpoints touched by a Splay access
```

## 9.7 Heavy/gap-inspired primitives

These are allowed only with an explicit mapping note.

Possible reference structures:

```text
A relative to B-derived ranks
B relative to A-derived ranks
A relative to rho_X recency priority
B relative to rho_Y recency priority
A and B relative to a shared declared comparator object
```

Every heavy-child tie rule and gap definition is frozen.

Raw components must be preserved.

## 9.8 Geometric-inversion-inspired primitives

Any inversion-style statistic inspired by L4 gets a new v0.2 identifier such as:

```text
PAIR_INV_*
RECENCY_INV_*
INTERVAL_INV_*
```

until a formal equivalence to the published object is proved.

## 9.9 Bounded multiscale primitives

Because repeated scale charging is a plausible source of superconstant loss, v0.2 explicitly permits:

```text
binary scale levels of subtree size
binary scale levels of depth
bounded per-node scale occupancy
one-charge-per-object hierarchical decompositions
nested interval scale signatures
```

Hard rule:

```text
No candidate may hide an unbounded number of charges per primitive object
without recording and proving the resulting global range.
```

## 9.10 Target leakage prohibition

Structural extraction code may read only the frozen state.

It may not read:

```text
U/V/G
Bellman signature
candidate labels
tightness labels
parent criticality
holdout verdict
```

The target join occurs in a separate analysis stage.

---

# 10. Candidate conserved-resource contract

## 10.1 Candidate object

A candidate debt law is:

```math
\Phi_\theta(z)
```

with metadata:

```text
hypothesis_id
parent_hypothesis
track
definition
b_hypothesis
primitive ontology version
uses_recency
uses_history_beyond_recency=false
n_independent_constants
range_claim
proof_obligations
discovery_artifacts
holdout_status
```

## 10.2 Candidate eligibility

A universal candidate must be:

```text
- total on every legal state in its declared track;
- independent of pair/state IDs;
- independent of U/V table lookup;
- independent of b_n^* tables;
- independent of n-specific coefficient tables;
- invariant to order-preserving relabeling;
- deterministic under every declared tie rule;
- accompanied by one universal b_H fixed before fresh holdout contact.
```

## 10.3 Preferred candidate forms

Priority:

```text
D1  bounded sum of local per-node debt atoms
D2  bounded sum of local per-edge debt atoms
D3  directed recency-violation charges
D4  nested interval / crossing-depth charges
D5  relative subtree-rank / classical-potential-derived charges
D6  heavy/gap/inversion-inspired charges with exact new definitions
D7  bounded multiscale charges with O(1) total charge per primitive object
D8  finite combinations of D1-D7
D9  kernel-class potential only if the kernel itself has an n-independent mathematical definition
```

Black-box neural networks, arbitrary lookup tables, and unrestricted symbolic regression cannot become theorem candidates.

## 10.4 Identity and directionality

Primary target:

```math
\Phi(T,T,\rho,\rho)=0
```

whenever the two executions are genuinely synchronized under the candidate's semantics.

For the initial theorem:

```math
\Phi(T,T,[],[])=0.
```

Do not require symmetry:

```math
\Phi(A,B)\neq \Phi(B,A)
```

is allowed and expected.

## 10.5 Nonnegativity

Primary candidate:

```math
\Phi(z)\ge0.
```

A signed potential may be explored only in a separately labeled diagnostic track and cannot enter the primary telescoping theorem until a valid lower-bound argument is supplied.

## 10.6 O(n)-range diagnostic

The literature motivates studying potentials whose total range is `O(n)` when additive initialization terms matter.

v0.2 records:

```text
RANGE_LINEAR_OBSERVED
RANGE_SUPERLINEAR_OBSERVED
RANGE_UNKNOWN
```

on finite domains.

Hard rule:

```text
O(n) range is a structural preference/diagnostic in v0.2,
not a rejection gate for the primary zero-initial certificate.
```

If a candidate requires a bounded nonzero initial potential and therefore an additive `O(n)` term, it enters a separately audited theorem track.

## 10.7 Candidate constant

A candidate constant `b_H` is frozen with the formula.

Changing:

```text
formula
coefficient
tie rule
kernel
recency interpretation
normalization
b_H
```

creates a new hypothesis ID.

---

# 11. Exact arithmetic and numerical policy

## 11.1 Integer/rational geometry

All inherited and newly computed fixed-rational `b` Bellman geometry uses exact integer-scaled weights:

```math
L_{p,q}(e)=p\,a(e)-q\,y(e).
```

No floating point is authoritative.

## 11.2 Candidate formulas with integer/rational atoms

Evaluate exactly with arbitrary-precision integers/rationals.

## 11.3 Candidate formulas containing logarithms

A candidate using logs is not rejected merely because exact rational evaluation is unavailable.

It enters:

```text
TRANSCENDENTAL-CANDIDATE
```

and must use certified sign evaluation.

Permitted methods:

```text
symbolic inequalities
interval arithmetic with directed rounding and sufficient precision
formal monotonicity reduction to integer comparisons
proof assistant / exact real library
```

If a residual interval straddles zero:

```text
SIGN_UNCERTIFIED
```

not PASS.

## 11.4 Discovery statistics

Floating values may be used for:

```text
visualization
ranking
clustering diagnostics
heuristic feature screening
approximate plots
```

They may never define:

```text
a kernel equivalence
a certificate
a counterexample sign
a theorem candidate pass/fail
a claim level
```

---

# 12. Outcome taxonomy

Every phase emits an exact status from a declared namespace.

Core statuses:

```text
PARENT_SEAL_VERIFIED
PARENT_SEAL_MISMATCH

BELL_DEBT_GEOMETRY_CERTIFIED
BELL_DEBT_GEOMETRY_FAIL
ROBUSTNESS_PANEL_INCOMPLETE

STRUCTURAL_ONTOLOGY_COMPLETE
STRUCTURAL_FEATURE_BUG

BEHAVIORAL_QUOTIENT_CERTIFIED
BEHAVIORAL_QUOTIENT_FAIL

KERNEL_VALUE_INSUFFICIENT
KERNEL_TRANSITION_INSUFFICIENT
KERNEL_FINITE_SUFFICIENT
KERNEL_NO_COMPRESSION

RECENCY_TRACK_NOT_ACTIVATED
RECENCY_TRACK_CERTIFIED
RECENCY_MARKOV_FAIL
RECENCY_RESOURCE_LIMIT

DEBT_ATOM_FAMILY_INCONSISTENT
DEBT_ATOM_FAMILY_SURVIVES_FINITE

CANDIDATE_REJECTED_DEV
CANDIDATE_FROZEN
CONTAMINATED_N8_VALIDATION_PASS
CONTAMINATED_N8_VALIDATION_FAIL
FRESH_H1_PASS
FRESH_H1_FAIL
FRESH_H2R_PASS
FRESH_H2R_FAIL

INDEPENDENT_VERIFICATION_FAIL
COUNTEREXAMPLE_FOUND
NO_COUNTEREXAMPLE_FOUND

UNIVERSAL_PROOF_PENDING
UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED
APPROXIMATE_MONOTONICITY_PROVED
DYNAMIC_OPTIMALITY_PROVED

NEGATIVE_FAMILY_NOT_ACTIVATED
NEGATIVE_FAMILY_CANDIDATE
DYNAMIC_OPTIMALITY_DISPROVED

RESOURCE_LIMIT_NO_CLAIM
```

No generic `PASS` may replace a scientifically meaningful status in sealed result objects.

---

# 13. Repository layout

The preferred implementation begins by cloning the sealed parent repository at `6de1ca2` into a new v0.2 repository or branch lineage.

The v0.2 working tree should expose the parent lineage clearly.

```text
SPLAY-AM-BD-v0.2/
|-- README.md
|-- IMPLEMENTATION_SPEC_v0.2.md
|-- WorkPlan.md
|-- Path.md
|-- CHANGELOG.md
|-- CITATIONS.md
|-- LICENSE
|-- pyproject.toml
|-- requirements-lock.txt
|-- .gitignore
|-- parent/
|   |-- PARENT_SEAL.json
|   |-- PARENT_FINAL_RESULT.json
|   |-- PARENT_MANIFEST.sha256
|   |-- PARENT_ARCHIVE.sha256
|   |-- PARENT_WORKPLAN_FINAL.md
|   |-- PARENT_PATH_FINAL.md
|   `-- import_ledger.json
|-- prereg/
|   |-- experiment_v0.2.yaml
|   |-- parent_contract.yaml
|   |-- b_panel.yaml
|   |-- state_tracks.yaml
|   |-- ontology_v0.2.yaml
|   |-- candidate_policy.yaml
|   |-- holdouts.yaml
|   |-- allowed_claims.md
|   |-- forbidden_claims.md
|   `-- prereg_sha256.txt
|-- external/
|   |-- MANIFEST.json
|   `-- papers/
|       |-- L1_sleator_tarjan_1985.pdf
|       |-- L2_levy_tarjan.pdf
|       |-- L3_chmel_et_al_2026.pdf
|       |-- L4_geometric_inversions_2020.pdf
|       `-- SHA256SUMS
|-- math/
|   |-- definitions_v0.2.md
|   |-- theorem_BD1_parent_transport.md
|   |-- theorem_BD2_bellman_debt.md
|   |-- theorem_BD3_bisimulation_transport.md
|   |-- theorem_BD4_recency_state.md
|   |-- theorem_BD5_augmented_path_correspondence.md
|   |-- theorem_BD6_augmented_telescoping.md
|   |-- theorem_BD7_kernel_lift.md
|   |-- theorem_BD8_negative_family_criterion.md
|   |-- proof_status.json
|   `-- latex/
|-- python/
|   |-- inherited/
|   |-- bellman_debt/
|   |-- structure/
|   |-- recency/
|   |-- kernel/
|   |-- mining/
|   |-- holdout/
|   |-- audit/
|   `-- adversary/
|-- schemas/
|   |-- parent_import.schema.json
|   |-- bellman_signature.schema.json
|   |-- specimen.schema.json
|   |-- recency_state.schema.json
|   |-- behavioral_partition.schema.json
|   |-- kernel_result.schema.json
|   |-- debt_atom.schema.json
|   |-- candidate_phi.schema.json
|   |-- candidate_contract.schema.json
|   |-- holdout_commitment.schema.json
|   |-- counterexample.schema.json
|   `-- final_result_v0.2.schema.json
|-- tests/
|   |-- parent/
|   |-- bellman/
|   |-- structure/
|   |-- recency/
|   |-- kernel/
|   |-- candidates/
|   |-- holdout/
|   |-- mutation/
|   `-- seal/
|-- artifacts/v02/
|   |-- parent_import/
|   |-- bellman/
|   |-- specimens/
|   |-- structure/
|   |-- recency/
|   |-- kernels/
|   |-- debt_atoms/
|   |-- hypotheses/
|   |-- holdouts/
|   |-- falsification/
|   |-- adversarial/
|   |-- audits/
|   |-- logs/
|   `-- seal/
`-- scripts/
    |-- run_phase00.sh
    |-- ...
    |-- run_phase18.sh
    `-- reproduce_all_v0.2.sh
```

Separation rules:

```text
- parent/ and inherited parent artifacts are read-only;
- structural extraction may not import Bellman target values;
- holdout firewalls may not import candidate-discovery modules;
- independent audit may read schemas, frozen formulas, and serialized states,
  but not discovery implementations;
- adversarial code may evaluate a frozen candidate but may not mutate it in place.
```

---

# 14. Preregistration files

## 14.1 experiment_v0.2.yaml

Minimum:

```yaml
experiment_id: SPLAY-AM-BD-v0.2
parent:
  experiment_id: SPLAY-AM-PD-v0.1
  sealed_commit: 6de1ca2
target_problem: Sleator-Tarjan dynamic optimality conjecture
bridge: Levy-Tarjan approximate monotonicity
primary_discovery_object: canonical_bellman_debt
primary_anchor_b:
  p: 2
  q: 1
primary_track: STATE_ONLY
secondary_track: RECENCY_AUGMENTED
pair_semantics: inherited_read_only_from_parent
authoritative_arithmetic: exact
finite_evidence_is_theorem: false
```

## 14.2 b_panel.yaml

```yaml
anchor:
  - {p: 2, q: 1, role: DISCOVERY_ANCHOR}
secondary:
  - {p: 5, q: 2, role: ROBUSTNESS_ONLY}
  - {p: 3, q: 1, role: ROBUSTNESS_ONLY}
  - {p: 4, q: 1, role: ROBUSTNESS_ONLY}
candidate_constant_policy:
  must_be_universal_across_n: true
  change_requires_new_hypothesis_id: true
```

## 14.3 state_tracks.yaml

```yaml
STATE_ONLY:
  state: [A, B]
  development_sizes: [2,3,4,5,6,7]
  contaminated_exhaustive_validation: [8]
  fresh_holdout: HOLDOUT-H1-v0.1

RECENCY_AUGMENTED:
  state: [A, B, rho_X, rho_Y]
  exact_required_sizes: [2,3,4]
  exact_stretch_sizes: [5]
  fresh_holdout: HOLDOUT-H2R-v0.1
```

## 14.4 ontology_v0.2.yaml

Freeze every primitive family and definition version before Bellman labels are joined.

## 14.5 holdouts.yaml

Must record:

```yaml
n8:
  status: PARTIALLY_REVEALED_CANARY_CONTAMINATED
  fresh: false

H1:
  inherited: true
  eligible_track: STATE_ONLY
  required_precondition: firewall_EMPTY

H2R:
  inherited: false
  eligible_track: RECENCY_AUGMENTED
  status_at_prereg: TO_BE_GENERATED_AND_QUARANTINED
```

---

# 15. Canonical data schemas

All sealed JSON:

```text
UTF-8
sorted keys
canonical separators
newline termination
integer strings for arbitrary-precision exact fields
explicit schema_version
```

## 15.1 Parent import row

```json
{
  "source_experiment": "SPLAY-AM-PD-v0.1",
  "source_commit": "6de1ca2",
  "artifact_path": "artifacts/...",
  "source_sha256": "...",
  "import_role": "CERTIFIED_PARENT_FACT",
  "v02_copy_sha256": "..."
}
```

## 15.2 Bellman signature row

```json
{
  "schema_version": "BELL-SIG-v0.2",
  "n": 7,
  "b": {"p":"2","q":"1"},
  "state_id": "...",
  "U_scaled": "17",
  "V_scaled": "5",
  "G_scaled": "12",
  "v_tight_actions": [["KEEP",3]],
  "u_tight_actions": [],
  "positive_excess_keep_count": 2,
  "delete_creation_count": 1,
  "max_keep_excess_scaled": "3",
  "max_delete_deltaV_scaled": "2"
}
```

This row is target data and may not enter theorem-facing structural extraction.

## 15.3 Recency state row

```json
{
  "schema_version": "RECENCY-v0.2",
  "n": 6,
  "A_tree_id": 12,
  "B_tree_id": 41,
  "rho_X_mru_to_lru": [4,2,6,1],
  "rho_Y_mru_to_lru": [2,1],
  "unseen_X_sorted": [3,5],
  "unseen_Y_sorted": [3,4,5,6]
}
```

The unseen arrays are redundant but may be serialized as audit fields.

## 15.4 Behavioral partition row

```json
{
  "schema_version": "BQ-v0.2",
  "track": "STATE_ONLY",
  "n": 6,
  "state_id": "...",
  "partition_round": 11,
  "class_id": "...",
  "observable_hash": "...",
  "successor_class_hash": "..."
}
```

## 15.5 Kernel insufficiency witness

```json
{
  "kernel_id": "K-REC-ANC-INT-v1",
  "failure_type": "KERNEL_VALUE_INSUFFICIENT",
  "n": 5,
  "state_1": "...",
  "state_2": "...",
  "same_kernel": true,
  "V1_scaled": "3",
  "V2_scaled": "1",
  "primitive_mismatch": null
}
```

Transition failure uses:

```text
failure_type = KERNEL_TRANSITION_INSUFFICIENT
action
cost mismatch or successor-kernel mismatch
```

## 15.6 Debt atom row

```json
{
  "atom_id": "DA-001",
  "definition_version": "DA-v0.2.1",
  "track": "RECENCY_AUGMENTED",
  "definition": "bounded nested recency-crossing charge",
  "state_value_exact": "...",
  "delta_exact": "...",
  "primitive_support": ["recency","crossing","interval"]
}
```

## 15.7 Candidate Phi record

```json
{
  "hypothesis_id": "PHI-0001",
  "parent_hypothesis": null,
  "track": "RECENCY_AUGMENTED",
  "definition": "...",
  "b_hypothesis": {"p":"2","q":"1"},
  "ontology_version": "ONTOLOGY-v0.2",
  "uses_recency": true,
  "uses_history_beyond_recency": false,
  "uses_UV_lookup": false,
  "n_specific_parameters": false,
  "fresh_holdout": "HOLDOUT-H2R-v0.1",
  "status": "FALSIFICATION_PENDING"
}
```

## 15.8 Counterexample record

```json
{
  "hypothesis_id": "PHI-0001",
  "track": "RECENCY_AUGMENTED",
  "n": 12,
  "mode": "KEEP",
  "key": 8,
  "state_before": "...",
  "state_after": "...",
  "cost_A": 2,
  "cost_B": 7,
  "Phi_before": "...",
  "Phi_after": "...",
  "residual_exact": "...",
  "smallest_under_order": true
}
```

---

# 16. Deterministic implementation order within every phase

Every phase:

```text
VERIFY PARENT / INPUT HASHES
  -> LOAD FROZEN v0.2 CONTRACT
    -> ASSERT TRACK + HOLDOUT FIREWALL
      -> COMPUTE
        -> ASSERT LOCAL INVARIANTS
          -> SAVE RAW APPEND-ONLY OUTPUT
            -> BUILD EXACT CERTIFICATE / WITNESS
              -> INDEPENDENT VERIFY
                -> RUN MUTATION CONTROLS
                  -> WRITE PHASE GATE
                    -> COMMIT / PUSH
```

Scientific failures and rejected hypotheses are preserved.

No phase may delete an inconvenient counterexample to make a later gate pass.

---

# 17. Nineteen-phase implementation plan

# PHASE 00 - Freeze parent seal, literature, v0.2 contract, and theorem obligations

## Goal

Create a clean, auditable boundary between completed v0.1 and new v0.2 work.

## 00.1 Clone exact parent state

Start from parent commit:

```text
6de1ca2
```

Verify local commit against remote.

Before editing `WorkPlan.md` or `Path.md`, preserve their parent final versions under `parent/` with exact hashes.

## 00.2 Verify parent seal

Verify:

```text
FINAL_RESULT
manifest
archive hash
archive member hashes
normative parent spec stack
parent candidate ledger
parent H1 firewall
parent n8 contamination ledger
```

## 00.3 Freeze v0.2 specification

Write this file as:

```text
IMPLEMENTATION_SPEC_v0.2.md
```

and hash it into `prereg/prereg_sha256.txt`.

## 00.4 Create theorem ledger

Before using theorem-dependent shortcuts, create `math/proof_status.json`.

Required obligations:

```text
BD0-01  parent-artifact import preserves exact logical content
BD0-02  V_b equals maximum future regret and satisfies Bellman recursion
BD0-03  U_b equals minimum past slack and satisfies predecessor Bellman recursion
BD0-04  deterministic cost-preserving bisimulation transports V_b
BD0-05  compatible source treatment transports U_b
BD0-06  rho(P) update exactly preserves relative last-access order of seen keys
BD0-07  augmented-state path corresponds exactly to (X,Y,rho_X,rho_Y)
BD0-08  augmented KEEP/DELETE potential inequalities telescope
BD0-09  kernel-defined candidate lifts from kernel classes to original states
BD0-10  finite kernel insufficiency does not imply universal impossibility
BD0-11  positive-regret cycle at fixed b refutes only that b
BD0-12  unbounded reachable cycle/path family with ratio -> infinity refutes approximate monotonicity
BD0-13  pair-state corridor V<=H<=U does not constrain arbitrary augmented-state potentials
BD0-14  candidate b_H must be n-independent before theorem promotion
```

Status:

```text
UNPROVED
PROVED
REVIEWED
BLOCKED
```

## Phase-00 gate

PASS only if:

```text
[ ] parent seal exact
[ ] v0.1 history preserved
[ ] v0.2 spec hash frozen
[ ] literature source ledger frozen
[ ] theorem ledger exists
[ ] H1 firewall verified EMPTY
[ ] n8 labeled contaminated, never fresh
[ ] no v0.2 output exists before prereg hash
```

Failure:

```text
FOUNDATION_NOT_FROZEN
```

---

# PHASE 01 - Reverify inherited Splay, pair dynamics, and b=2 geometry

## Goal

Establish that v0.2 is analyzing the exact object sealed by v0.1.

## 01.1 Read-only import

Load parent:

```text
tree universes
single-tree transition tables
reachable pair sets
b_n^* certificates
b=2 U/V/G geometry
candidate failure ledger
```

through a read-only adapter.

## 01.2 Independent spot/full reproduction policy

Required:

```text
n=2..6:
  full independent reproduction of b=2 U/V local Bellman checks

n=7:
  full streamed certificate verification of serialized b=2 geometry

b_n^*:
  reverify parent certificates without recomputing discovery
```

## 01.3 Parent fact table

Emit one v0.2 import artifact containing:

```text
n
C_n
|R_n|
b_n^*
max U_2
max V_2
#forced b=2 states
parent verifier hash
v0.2 verifier verdict
```

## Phase-01 gate

PASS only if every inherited fact used downstream independently verifies.

Failure:

```text
PARENT_SEAL_MISMATCH
```

---

# PHASE 02 - Build fixed-b Bellman debt geometry and robustness panel

## Goal

Turn canonical Bellman values into explicit deletion-debt analysis objects.

## 02.1 Anchor geometry

For `b=2`, materialize/verify:

```text
U_2
V_2
G_2
V-tight edges
U-tight edges
positive-excess KEEP edges
DELETE debt-creation edges
exact Bellman residuals
```

for `n=2..7`.

## 02.2 Secondary b panel

For each:

```text
5/2, 3, 4
```

compute exact geometry on:

```text
required: n=2..5
stretch:  n=6..7
```

provided `b` passes exact finite feasibility.

## 02.3 Monotonicity diagnostics

Record but do not assume:

```text
how V_b changes as b increases
how U_b changes as b increases
whether structural tight-edge families persist
whether kernel partitions remain stable
```

Any mathematical monotonicity claim requires proof.

## 02.4 Independent verification

Every new fixed-b table receives a clean independent Bellman verifier.

## Phase-02 gate

PASS when the `b=2` anchor geometry is complete and verified.

Secondary panel incompleteness does not block anchor science; it emits:

```text
ROBUSTNESS_PANEL_INCOMPLETE
```

---

# PHASE 03 - Build complete Bellman signatures and extremal specimen tables

## Goal

Create the exact microscope that tells us where debt is created and repaid.

## 03.1 State signature

For every development state, compute `BELL-SIG-v0.2`.

## 03.2 Edge signature

For every edge, compute:

```text
mode
key
a
y
w_b
Delta U
Delta V
R_U
R_V
tightness
access rotation signature
path lengths
```

## 03.3 KEEP excess table

Preserve every edge with:

```math
c(B,x)-2c(A,x)>0.
```

These are the transitions that cannot be paid locally without a potential decrease.

## 03.4 DELETE creation table

Preserve every DELETE edge with:

```math
V_2(t)>V_2(s).
```

These are canonical examples where a deleted restructuring creates more future extractable regret.

## 03.5 Exact repayment table

Preserve every KEEP edge satisfying:

```math
w_2(e)>0,\qquad
R^V_2(e)=0.
```

On these:

```math
V_2(s)-V_2(t)=w_2(e)
```

exactly.

These are highest-priority theorem-mining specimens.

## 03.6 Human-readable trajectories

For canonical representatives store:

```text
A/B before
key/mode
search paths
rotation sequence
A/B after
U/V before/after
exact excess
structural placeholders
```

## Phase-03 gate

Complete when every anchor-domain edge is classified and independently hash-checked.

---

# PHASE 04 - Instrument target-blind structural ontology v0.2

## Goal

Build an intentionally overcomplete structural description without reading Bellman answers.

## 04.1 Separate extraction process

The feature extractor process receives only:

```text
state serialization
tree tables
frozen ontology definition
```

It cannot open Bellman artifacts.

Static import audit must enforce this.

## 04.2 Required pair-state families

Implement Section 9 state-only primitives.

## 04.3 Required symmetry tests

Mirror/order reversal.

Order-preserving relabeling invariance.

## 04.4 Raw components

Composite features must preserve raw atom lists.

Example:

```text
not just nested_disagreement_count=7
but the seven exact interval witnesses.
```

## 04.5 Join only after freeze

After ontology extraction hashes are frozen, a separate script joins structural rows to Bellman labels.

## Phase-04 gate

PASS only if:

```text
[ ] no target leakage
[ ] every coordinate defined
[ ] raw components preserved
[ ] symmetry tests pass
[ ] deterministic rerun hash matches
```

Failure:

```text
STRUCTURAL_FEATURE_BUG
```

---

# PHASE 05 - Compute exact behavioral quotient by partition refinement

## Goal

Ask what information is *operationally* necessary before guessing a potential formula.

## 05.1 Full-state control

Every serialized pair state is unique under `FULL_STATE`.

This baseline must preserve all transitions and values.

## 05.2 Primitive behavioral partition

Run target-independent deterministic partition refinement from primitive action/cost observations.

## 05.3 Fixed point

Stop only when class IDs stabilize exactly.

## 05.4 Independent implementation

A second implementation must produce the same partition up to canonical class renaming.

Canonicalize classes by sorted member IDs before comparison.

## 05.5 Bellman transport audit

Only after BD0-04/05 are `PROVED+REVIEWED`, join the partition to `V_2/U_2`.

Any class containing different transported values is:

```text
BEHAVIORAL_QUOTIENT_FAIL
```

not an interesting scientific result.

## 05.6 Compression report

Record:

```text
#states
#classes
compression ratio
class-size distribution
largest nontrivial classes
smallest n where classes become singleton-heavy
```

A quotient with no compression is still an exact result.

## Phase-05 gate

PASS on exact partition certification.

---

# PHASE 06 - PC-style structural kernel refinement and component ablation

## Goal

Find a mathematically interpretable structural signature that approximates or realizes the behavioral quotient without encoding the target.

## 06.1 Overcomplete K0

Begin with:

```text
pair-tree primitives
ancestor structure
interval structure
subtree-size structure
all-next-key path geometry
crossing structure
bounded multiscale structure
```

Track R coordinates are excluded until Phase 08.

## 06.2 Necessity witness

For each removed coordinate family, search for the lexicographically smallest pair of states such that:

```text
same weakened kernel
but
  different V_2
or
  primitive transition mismatch
or
  different exact behavioral class
```

## 06.3 Three insufficiency labels

```text
KERNEL_VALUE_INSUFFICIENT
KERNEL_TRANSITION_INSUFFICIENT
KERNEL_BEHAVIOR_CLASS_INSUFFICIENT
```

Do not conflate them.

## 06.4 Exact sharpness table

For each coordinate:

```text
removed family
smallest n failing
witness states
which Bellman values differ
which action/successor differs
minimal additional coordinate restoring separation on that witness
```

## 06.5 No "minimal" overclaim

A greedy ablation surviving all single removals is not automatically globally minimal.

Use wording:

```text
COMPONENTWISE_NECESSARY_FINITE
```

unless global minimum is exactly solved.

## Phase-06 gate

Complete when all preregistered ablations have witnesses or exact finite survival.

---

# PHASE 07 - Mine debt creation and repayment transition laws

## Goal

Stop asking "what predicts V?" and ask the sharper question:

> What structural object is created by DELETE and consumed by expensive KEEP?

## 07.1 Delta-first dataset

For every structural primitive/atom `F`:

```math
\Delta F(e)=F(t)-F(s).
```

Primary targets:

```text
DELETE: Delta V_2
KEEP:   -w_2 on positive-excess edges
V-tight equality structure
```

## 07.2 Creation screen

A plausible debt atom must not routinely jump by a scale much larger than `c_A` under a cheap DELETE unless another component provides a proved cancellation.

Flag:

```text
CHEAP_DELETE_LARGE_ATOM_JUMP
```

## 07.3 Repayment screen

On high-excess KEEP edges ask whether destruction of the atom lower-bounds the excess.

## 07.4 Exact constraint search

Permit exact linear and bounded-piecewise combinations of declared atoms.

Primary ranking:

```text
1. exact inequality coverage
2. exact equality on V-tight repayment edges
3. bounded DELETE creation
4. cross-n formula stability
5. expression complexity
```

No `R^2` ranking can outrank exact constraint satisfaction.

## 07.5 Minimal inconsistent subsystem

For every failed atom family, compute a minimal or inclusion-minimal exact inconsistent transition subsystem where feasible.

Preserve it as a scientific result.

## 07.6 Motif extraction

Clustering is heuristic; motifs are exact only after canonical definition.

For every repeated motif preserve:

```text
structural predicate
transition predicate
sizes where observed
exact debt changes
counterexamples to motif universality
```

## Phase-07 gate

The phase may complete with zero surviving atoms.

That is not a pipeline failure.

---

# PHASE 08 - Formalize recency-augmented track and generate fresh H2R holdout

## Goal

Create a rigorously bounded history augmentation without contaminating discovery with an unstructured history variable.

## 08.1 Prove recency-state semantics

BD0-06 and BD0-07 must be `PROVED+REVIEWED` before exact augmented Bellman claims.

## 08.2 Exact augmented reachability

Required exhaustive sizes:

```text
n=2,3,4
```

Stretch:

```text
n=5
```

Reachability begins from:

```text
(T,T,[],[])
```

for every initial `T`.

Generate both KEEP and DELETE successors exactly.

## 08.3 Augmented fixed-b geometry

At `b=2`, compute exact:

```text
reachable augmented states
U_2^R
V_2^R
G_2^R
tight edges
creation/repayment edges
```

on required sizes.

## 08.4 Compare same pair state under different recencies

A crucial table groups augmented states by `(A,B)`.

Ask whether:

```math
V_2^R(A,B,\rho_X,\rho_Y)
```

varies with recency.

If yes, this is exact finite evidence that recency can carry debt information not identified by `(A,B)` **within the augmented formulation**.

It is not a proof that no state-only universal potential exists.

## 08.5 Build HOLDOUT-H2R-v0.1

Before candidate synthesis, create a quarantined fresh bank.

Sizes:

```text
8,10,12,16,24,32
```

States per size:

```text
20,000
```

Total states:

```text
120,000
```

Outgoing transitions:

```math
2\cdot20,000\cdot(8+10+12+16+24+32)
=
4,080,000.
```

Each bank state must include a legal generation history sufficient for independent replay, but candidate-discovery namespaces may not read that history or state.

Stratify generation by preregistered categories:

```text
history length
KEEP/DELETE density
recency divergence
tree-shape family
access-path disparity
structured vs random sequence generator
```

The exact bank membership is quarantined.

## 08.6 Firewall

State machine:

```text
EMPTY
-> BANK_COMMITTED
-> CANDIDATE_SET_FROZEN
-> UNLOCKED_ONCE
```

No backwards transitions.

## Phase-08 gate

Required:

```text
[ ] recency semantics proved
[ ] augmented n<=4 exact geometry certified
[ ] H2R commitment frozen
[ ] discovery namespaces cannot read H2R
[ ] generator cannot silently regenerate a different bank
```

---

# PHASE 09 - Instrument recency, crossing, inversion, rank, and gap-inspired ontology

## Goal

Test whether the missing debt object is related to the historical structural signals suggested by prior Splay analysis.

## 09.1 Target-blind extraction

Exactly as Phase 04: no Bellman reads.

## 09.2 Required families

Implement Section 9 recency primitives plus:

```text
parent-child recency heap violations
nonadjacent ancestor recency violations
crossing depth of recency violations
nested recency-interval violations
relative classic rank discrepancy
recency-priority reference-tree diagnostics
pair-inversion-like diagnostics
heavy/light and gap-inspired diagnostics
bounded multiscale recency charges
```

## 09.3 Unseen-key tie audit

Every affected statistic records one of:

```text
TIE_INVARIANT
TIE_EXPLICIT
TIE_BREAK_DEPENDENT_DIAGNOSTIC
```

No unlabeled tie behavior.

## 09.4 Pair-state versus augmented-state ablation

Compare kernels:

```text
K(A,B)
K(A,B,rho_X)
K(A,B,rho_Y)
K(A,B,rho_X,rho_Y)
```

Componentwise witnesses determine which recency side adds finite identification power.

## Phase-09 gate

Complete on exact extraction + ablation, regardless of whether recency helps.

---

# PHASE 10 - Discover exact debt atoms and local charge decompositions

## Goal

Find small mathematical objects whose changes line up with the conservation law.

## 10.1 Atom eligibility

An atom must have:

```text
tree-theoretic or recency-theoretic definition
exact finite evaluation
order-relabelling semantics
declared local support
declared maximum per-object charge if bounded
```

## 10.2 Creation inequality

Search atom combinations satisfying:

```math
\Delta \Phi_{\rm DELETE}
\le
b\,c_A(x)
```

on development states.

## 10.3 Repayment inequality

Search:

```math
c_B(x)-b\,c_A(x)
\le
\Phi_{\rm before}-\Phi_{\rm after}
```

on KEEP.

## 10.4 Bellman equality diagnostics

Exact equality on V-tight edges is high-value evidence but not mandatory for a valid potential.

Label:

```text
EXPLAINS_V_TIGHT
```

only when exact.

## 10.5 Scale audit

For every atom family measure exact finite growth:

```text
max value by n
max one-step increase
max one-step decrease
charge per node/edge/interval
```

Do not infer asymptotic order from finite data without proof.

## 10.6 Family exhaustion

For each preregistered atom grammar, either:

```text
SURVIVING_FORMULA
```

or an exact inconsistent witness.

## Phase-10 gate

Complete when each preregistered grammar is exhausted or resource-limited with explicit status.

---

# PHASE 11 - Synthesize versioned candidate universal debt laws

## Goal

Convert exact patterns into explicit theorem hypotheses.

## 11.1 Candidate eras

All initial candidates belong to:

```text
ERA-BD-A
```

They may use all v0.2 development evidence.

They may not use:

```text
detailed n8 EV8 result for their own formula
H1 detailed bank
H2R detailed bank
future holdout counterexamples
```

## 11.2 Formula freeze

For each `PHI-*`:

```text
mathematical definition
track
b_H
tie rules
normalization
primitive ontology version
range claim
proof outline
```

Freeze before any holdout unlock.

## 11.3 Finite geometry precheck

For Track S candidates, at their own `b_H`:

```text
verify b_H >= b_n^* on every certified n
compute/reuse U_bH,V_bH as required
test V_bH <= Phi <= U_bH
```

Never test a candidate against the wrong `b` geometry.

For Track R, compute the corresponding augmented geometry on certified augmented sizes where feasible.

## 11.4 No survivor required

Zero candidates is an allowed result.

## Phase-11 gate

A candidate may advance only if its mathematical contract is frozen and all development gates pass.

---

# PHASE 12 - Exact development falsification

## Goal

Kill bad candidates before spending fresh evidence.

## 12.1 State-only development

Use all fully known parent development sizes:

```text
n=2..7
```

These are development, not holdout, in v0.2.

## 12.2 Recency development

Use exact augmented sizes:

```text
n=2..4
```

plus n=5 only if fully certified.

## 12.3 Exact residuals

KEEP:

```math
E_K=
c(B,x)+\Phi(t)-\Phi(s)-b_H c(A,x).
```

DELETE:

```math
E_D=
\Phi(t)-\Phi(s)-b_H c(A,x).
```

## 12.4 Ordered failure

Preserve the lexicographically smallest positive residual and the maximum positive residual.

## 12.5 Candidate failure analysis

Every rejection must answer:

```text
what state distinction did the candidate miss?
which atom/scale failed?
upper-growth or lower-debt failure?
locality failure?
recency insufficiency?
cheap-DELETE blowup?
expensive-KEEP underpayment?
```

The explanation may be `UNKNOWN`, but the exact counterexample is mandatory.

## Phase-12 gate

Only zero-positive-residual candidates advance.

---

# PHASE 13 - Freeze candidate set and consume the correct validation resource once

## Goal

Use the expensive evidence only on candidates that survived development.

## 13.1 Candidate-set commitment

Freeze one candidate-set hash containing all survivors.

No additions after any fresh holdout reveal.

## 13.2 State-only sequence

For every frozen Track S survivor:

```text
1. run n8 contaminated exhaustive validation
2. record CONTAMINATED_EXHAUSTIVE_VALIDATION
3. if still alive, unlock H1 once
4. evaluate every H1 state and transition
5. freeze verdict
```

A failure at n8 kills the candidate before H1 and preserves H1 if no other survivor needs it.

## 13.3 Recency sequence

For every frozen Track R survivor:

```text
unlock H2R once
evaluate all 120,000 states
evaluate all 4,080,000 transitions
independent replay every preserved counterexample
freeze verdict
```

## 13.4 Post-holdout descendants

Any formula changed after H1/H2R reveal gets a new ID and status:

```text
POST_HOLDOUT
```

It may not be called fresh-tested on the consumed bank.

A new genuinely fresh bank is required for a new fresh claim.

## Phase-13 gate

A survivor may advance only with the correct fresh-holdout PASS for its track.

---

# PHASE 14 - Independent implementation and adversarial large-n falsification

## Goal

Try to murder every remaining candidate before proof work.

## 14.1 Clean-room candidate evaluator

Receives only:

```text
mathematical Phi definition
b_H
state schema
Splay cost contract
recency contract if Track R
```

No discovery imports.

## 14.2 Adversarial state families

State-only:

```text
left/right spines
opposite spines
balanced/spine
alternating zig-zag
nested interval disagreement
same access-cost vector but different deep structure
large ancestor disagreement
rank-gap extremes
mirrors
motif inflation from prior failures
```

Recency-augmented adds:

```text
max recency divergence
many X-only recent accesses
same trees / different recency
same recency / different trees
deep nonadjacent recency violations
nested crossing-depth violations
alternating KEEP/DELETE histories
long deletion bursts followed by one KEEP
```

## 14.3 Search engines

At least:

```text
uniform/random legal histories
structured generator
hill climb
simulated annealing
genetic search
motif inflation
rotation-neighborhood search
counterexample generalizer
```

Heuristics propose; exact evaluator disposes.

## 14.4 Mutation controls

Perturb:

```text
one coefficient
one sign
one tie rule
one recency update
one b_H
one action mode
```

The suite must detect known bad mutants.

## Phase-14 gate

No counterexample is a finite-survival condition only.

It is never a proof.

---

# PHASE 15 - Universal structural/kernel/debt proof

## Goal

Stop mining and do mathematics.

At most one primary theorem candidate is promoted at a time.

## 15.1 Domain declaration

The proof must explicitly state:

```text
STATE_ONLY all reachable pair executions
or
RECENCY_AUGMENTED all legal augmented executions
```

If it claims all pair states rather than only reachable ones, prove the stronger domain.

## 15.2 Well-definedness

Prove candidate `Phi` is defined for arbitrary `n`.

## 15.3 Identity

Prove:

```math
\Phi(z_0)=0.
```

## 15.4 Nonnegativity

Prove:

```math
\Phi(z)\ge0.
```

## 15.5 DELETE law

For arbitrary legal state/key:

```math
\Phi(z')-\Phi(z)
\le b_H c(A,x).
```

The proof must explain debt creation structurally.

## 15.6 KEEP law

For arbitrary legal state/key:

```math
c(B,x)+\Phi(z')-\Phi(z)
\le b_H c(A,x).
```

The proof must explain why expensive B accesses consume enough stored debt.

## 15.7 Case partition

At minimum cover Splay structural cases:

```text
root/no rotation
ZIG
LL
RR
LR
RL
```

If the proof uses multiple rotations, specify the block decomposition.

For Track R also partition every recency case required by the formula.

## 15.8 Nonlocal terms

If an access changes charges outside the search path, bound them explicitly.

No "other terms cancel" without a lemma.

## 15.9 Kernel proof option

If the candidate is defined on a kernel quotient:

```text
prove kernel invariance
prove action/cost preservation
prove successor-class preservation
prove potential lift
```

Finite partition refinement is not the universal kernel proof.

## 15.10 No finite premises

No line of the universal proof may rely on:

```text
n<=7
observed maxima
holdout PASS
fitted coefficient optimality
empirical scaling
finite partition stabilization
```

## Phase-15 gate

Only a complete independently reviewed proof yields:

```text
UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED
```

---

# PHASE 16 - Telescope, establish approximate monotonicity, and bridge to dynamic optimality

## Goal

Derive the original theorem from the proved local law.

## 16.1 Telescoping

For arbitrary initial tree `T`, sequence `X`, and subsequence `Y<=X`, construct the paired execution.

Sum local inequalities:

```math
\operatorname{Splay}(Y,T)
+
\Phi(z_m)-\Phi(z_0)
\le
b_H\operatorname{Splay}(X,T).
```

Use:

```math
\Phi(z_0)=0,\qquad
\Phi(z_m)\ge0.
```

Conclude:

```math
\boxed{
\operatorname{Splay}(Y,T)
\le
b_H\operatorname{Splay}(X,T).
}
```

## 16.2 Augmented-state legitimacy

For Track R, the proof must explicitly show that:

```text
rho_X,rho_Y are deterministic functions of the prefixes;
every real (X,Y) execution induces the augmented transitions used in Phase 15;
the potential still telescopes despite history augmentation.
```

## 16.3 Levy-Tarjan audit

Freeze a bridge audit covering:

```text
Splay variant
cost convention
initial-tree convention
subsequence definition
additive terms
constant independence
direction of implication
theorem version
```

## 16.4 Claim sequence

Only if each prior gate passes:

```text
UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED
-> APPROXIMATE_MONOTONICITY_PROVED
-> DYNAMIC_OPTIMALITY_PROVED
```

No combined leap.

---

# PHASE 17 - Negative branch: extract and prove an unbounded real Splay witness family

## Goal

Disprove the conjecture only if the dynamics themselves produce a scalable obstruction.

## 17.1 Activation criteria

The negative branch activates only if there exists a systematic actual-cost motif satisfying all of:

```text
C1  reachable legal paired executions, not only H residuals
C2  explicit parameterized construction candidate
C3  measured ratio or cycle-required b grows with parameter
C4  structure survives independent replay
```

## 17.2 Fixed-b cycle warning

A positive-regret cycle at `b=2` proves only:

```text
b=2 is insufficient on that size/state family.
```

It does not disprove approximate monotonicity.

## 17.3 Required final family

Produce explicit:

```math
(T_k,X_k,Y_k)
```

with `Y_k<=X_k`.

Prove symbolic bounds:

```math
\operatorname{Splay}(X_k,T_k)\le f(k),
```

```math
\operatorname{Splay}(Y_k,T_k)\ge g(k),
```

and:

```math
\frac{g(k)}{f(k)}\to\infty.
```

## 17.4 No solver-defined family

The final family must be closed-form.

"Take the worst solver state for each k" is forbidden.

## 17.5 Reverse bridge

Only after the unbounded subsequence-overhead theorem is complete may the reverse Levy-Tarjan implication be invoked under audited conventions.

---

# PHASE 18 - Seal, reproduce, package, and release

## Goal

Create a deterministic record that distinguishes finite discovery from theorem-level success.

## 18.1 FINAL_RESULT

Generate from artifacts only.

Allowed claim levels:

```text
PARENT_SEAL_ONLY
FINITE_BELLMAN_DEBT_RESULTS
FINITE_KERNEL_OBSTRUCTION_RESULTS
FINITE_DEBT_LAW_MINING_RESULTS
CANDIDATE_DEBT_LAW_SURVIVES_FINITE_TESTS
UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED
APPROXIMATE_MONOTONICITY_PROVED
DYNAMIC_OPTIMALITY_PROVED
DYNAMIC_OPTIMALITY_DISPROVED
```

Exactly one terminal level.

## 18.2 Reproduction

Fresh checkout must:

```text
verify parent seal
rebuild v0.2 deterministic small-size artifacts
reverify imported b=2 geometry
rebuild behavioral quotient for required sizes
recompute exact specimen summaries
reverify every sealed candidate/counterexample
verify holdout commitments
recompute FINAL_RESULT
```

## 18.3 Archive

Create deterministic archive:

```text
SPLAY-AM-BD-v0.2.tar.zst
```

with canonical ordering, normalized metadata, and SHA-256.

## 18.4 Paper-facing reports

Produce:

```text
BELLMAN_DEBT_REPORT.md
KERNEL_SHARPNESS_REPORT.md
HYPOTHESIS_LEDGER.md
THEOREM_MINING_REPORT_v0.2.md
REPRODUCIBILITY.md
AI_USE.md
```

## 18.5 No cleanup by deletion

Unexpected scientific artifacts cause:

```text
seal audit failure
or explicit manifest inclusion with status
```

never silent deletion.

---

# 18. Threat model

The v0.2 seal audits at least the following threats.

```text
T01  parent artifact drift
T02  parent hash accepted from prose instead of artifact
T03  v0.1 failure rewritten as v0.2 discovery
T04  n8 contamination forgotten
T05  H1 detail leaked before candidate freeze
T06  H1 used for a recency candidate lacking required fields
T07  H2R detail leaked before candidate freeze
T08  H2R bank regenerated after candidate inspection
T09  U/V values leak into structural feature extraction
T10  Bellman-tight labels leak into kernel definition
T11  state IDs/hashes act as hidden lookup features
T12  finite behavioral quotient called a universal kernel
T13  value equality confused with transition bisimulation
T14  recency order claimed sufficient without Markov proof
T15  unseen recency ties silently broken
T16  absolute timestamps smuggled into frozen relative-recency state
T17  b=2 treated as theorem-required constant
T18  candidate b tuned after fresh holdout
T19  wrong-b U/V tables used for candidate sandwich
T20  finite residual tolerance hides positive violation
T21  floating logs determine authoritative sign
T22  feature family renamed from literature without equivalence proof
T23  finite O(n)-looking range called asymptotic O(n)
T24  cheap DELETE creates untracked superlinear debt
T25  expensive KEEP paid by hidden negative potential
T26  nonnegativity assumed from finite tests
T27  history-augmented potential telescoping not proved
T28  holdout survivor called theorem
T29  H residual motif mistaken for Splay ratio motif
T30  fixed-b positive-regret cycle called DOC disproof
T31  negative family chosen by solver rather than closed form
T32  proof omits a Splay rotation case
T33  proof hides n-dependent constant
T34  additive overhead smuggled into no-overhead statement
T35  Levy-Tarjan convention mismatch
T36  current 2026 bound used as logical premise
T37  independent verifier imports discovery code
T38  mutation controls fail to catch known corruption
T39  non-deterministic parallel reduction changes witness
T40  resource exhaustion interpreted as scientific negative
T41  failed hypotheses overwritten
T42  counterexamples suppressed
T43  AI assistance silently changes frozen contract
T44  manifest omits untracked scientific files
T45  archive/manifest self-reference creates stale seal
T46  full-state control fails but analysis continues
T47  same weakened kernel has different primitive successors and is still called sufficient
T48  Track S and Track R results pooled without labels
T49  secondary b panel used to cherry-pick final formula without versioning
T50  fresh validation bank reused as fresh after reveal
```

Each threat must map to at least one test, invariant, or manual audit item.

---

# 19. Test matrix

Minimum named tests.

## Parent / foundation

```text
PARENT-01 commit equality
PARENT-02 manifest verification
PARENT-03 FINAL_RESULT schema
PARENT-04 H1 firewall EMPTY
PARENT-05 n8 contamination preserved
PARENT-06 parent normative hashes
```

## Bellman debt

```text
BD-01 exact b=2 edge weights
BD-02 U Bellman inequalities
BD-03 V Bellman inequalities
BD-04 V<=U
BD-05 V-tight equality witnesses
BD-06 DELETE creation classification
BD-07 KEEP excess classification
BD-08 deterministic signature hash
BD-09 independent b=2 reverify
BD-10 secondary-b wrong-geometry canary
```

## Structural ontology

```text
ST-01 no target imports
ST-02 mirror invariance where declared
ST-03 relabel invariance
ST-04 raw atom reconstruction
ST-05 deterministic feature serialization
ST-06 full-state control
```

## Behavioral quotient / kernel

```text
K-01 partition fixed point
K-02 independent partition agreement
K-03 primitive cost preservation
K-04 successor-class preservation
K-05 Bellman transport after theorem gate
K-06 full-state control
K-07 value insufficiency witness validity
K-08 transition insufficiency witness validity
K-09 ablation deterministic
K-10 target-leak mutant caught
```

## Recency

```text
R-01 rho empty initial
R-02 update exact
R-03 duplicate access moves to front
R-04 KEEP updates both
R-05 DELETE updates only X
R-06 seen/unseen complement exact
R-07 relative-order replay from history
R-08 augmented reachability parent witness
R-09 augmented closure
R-10 same-pair/different-recency grouping
R-11 unseen-tie diagnostics
R-12 independent recency implementation
```

## Debt atoms / candidates

```text
D-01 exact atom evaluation
D-02 DELETE creation residual
D-03 KEEP repayment residual
D-04 identity normalization
D-05 nonnegativity
D-06 b_H n-independent metadata
D-07 wrong-b geometry mutant caught
D-08 coefficient mutant caught
D-09 sign mutant caught
D-10 tie-rule mutant caught
D-11 exact smallest counterexample
D-12 independent candidate agreement
```

## Holdouts

```text
HLD-01 n8 never labeled fresh
HLD-02 H1 unread pre-freeze
HLD-03 H1 unlock at most once
HLD-04 H2R commitment hash
HLD-05 H2R unread pre-freeze
HLD-06 H2R unlock at most once
HLD-07 post-holdout formula edit creates new ID
HLD-08 candidate-set hash immutable after unlock
```

## Proof / seal

```text
PR-01 arbitrary-n statement contains no finite premise
PR-02 all Splay structural cases covered
PR-03 recency cases covered if Track R
PR-04 telescoping symbolic check
PR-05 bridge convention audit
PR-06 universal b independence
NEG-01 fixed-b cycle not misclassified
NEG-02 negative family closed-form
NEG-03 symbolic cost bounds
NEG-04 ratio limit proof
SEAL-01 fresh checkout
SEAL-02 manifest completeness
SEAL-03 exact arithmetic only in authoritative fields
SEAL-04 result recomputation
SEAL-05 archive determinism
```

---

# 20. Permanent invariants

At minimum:

```text
INV-001 parent commit is 6de1ca2
INV-002 parent artifacts are read-only
INV-003 parent FINAL_RESULT is imported by hash
INV-004 cost is depth+1
INV-005 Splay variant is ordinary bottom-up
INV-006 pair transitions match parent
INV-007 anchor b is exactly 2/1
INV-008 b=2 is discovery anchor only
INV-009 V empty continuation allowed
INV-010 V>=0
INV-011 pair-state candidate corridor uses candidate's own b
INV-012 structural extractor reads no Bellman target
INV-013 theorem-facing kernel contains no target values
INV-014 behavioral quotient is target-independent
INV-015 full-state control preserves primitive dynamics
INV-016 recency state stores relative order only
INV-017 KEEP recency updates both streams
INV-018 DELETE recency updates X only
INV-019 unseen ties never silently total-ordered
INV-020 Track S and Track R stay separate
INV-021 exact integer/rational arithmetic authoritative
INV-022 float discovery never sets pass/fail
INV-023 every candidate has one frozen b_H
INV-024 every candidate formula edit creates new ID
INV-025 every fresh-holdout reveal freezes candidate set
INV-026 n8 remains contaminated forever
INV-027 H1 only tests Track S
INV-028 H2R only tests Track R unless schema extended before freeze
INV-029 counterexamples are append-only
INV-030 rejected candidates remain in ledger
INV-031 exact residual >0 always rejects
INV-032 no tolerance around zero
INV-033 finite survival never equals proof
INV-034 positive-regret cycle at fixed b never equals disproof
INV-035 negative theorem requires unbounded actual Splay ratio family
INV-036 proof constant independent of n
INV-037 proof formula independent of finite table lookup
INV-038 augmented potential telescope explicitly proved
INV-039 bridge invoked only after convention audit
INV-040 current frontier bound is context only
INV-041 AI cannot silently alter contract
INV-042 every artifact names track
INV-043 every literature-derived object names mapping status
INV-044 O(n) range finite observation not asymptotic proof
INV-045 all exact witness ordering deterministic
INV-046 parallel reductions sorted before seal
INV-047 resource limits emit no scientific conclusion
INV-048 final claim computed from artifacts
INV-049 manifest covers all scientific files
INV-050 release reproduces terminal claim from clean checkout
```

---

# 21. Scaling and resource policy

## 21.1 State-only development

Uses inherited exact pair states through `n=7`.

No need to regenerate pair reachability unless verification requires it.

## 21.2 Augmented recency development

Exact required:

```text
n<=4
```

because augmented state count can grow factorially with recency order.

`n=5` is stretch.

No conclusion follows from inability to exhaust `n=5`.

## 21.3 Implicit edges

Use parent single-tree tables to generate pair successors.

For augmented Track R, recency updates are O(n) or better with canonical compact representation.

## 21.4 Compression

Canonical logical stream hash separate from compressed-file hash.

## 21.5 Parallelism

Safe:

```text
state-local structural extraction
edge-local Bellman signature
holdout residual evaluation
candidate-independent specimen generation
```

Global witness choice requires deterministic reduction.

## 21.6 Resource status

```text
RESOURCE_LIMIT_NO_CLAIM
```

must include:

```text
phase
track
n
last completed artifact
memory/time metadata
scientific claims still valid
scientific claims not attempted
```

---

# 22. Exact outputs to preserve

For each state-only development `n` at `b=2`:

```text
1. parent import hash
2. |R_n|
3. U_2/V_2/G_2 summary
4. complete Bellman signature table
5. V-tight edge table
6. U-tight edge table
7. positive-excess KEEP table
8. DELETE debt-creation table
9. exact repayment table
10. canonical human-readable specimens
11. structural ontology table
12. behavioral quotient
13. structural-kernel ablation table
14. necessity witnesses
15. debt-atom delta table
16. candidate ledger
17. independent audit
18. checksums
```

For augmented sizes:

```text
19. reachable augmented state count
20. recency-state table
21. augmented U/V/G
22. same-pair/different-recency value-separation table
23. recency-kernel ablation table
24. H2R generation/commitment metadata
```

---

# 23. Theorem-mining report structure

`THEOREM_MINING_REPORT_v0.2.md`:

```text
A. Parent v0.1 facts inherited
B. b=2 Bellman debt geometry
C. Debt-creation DELETE edges
D. Debt-repayment KEEP edges
E. V-tight structural motifs
F. Behavioral quotient
G. Pair-state kernel insufficiency witnesses
H. Recency augmentation results
I. Recency/crossing/inversion/gap-inspired atoms
J. Exact inconsistent atom families
K. Surviving debt laws
L. Fresh holdout outcomes
M. Adversarial counterexamples
N. Universal proof status
O. Negative-family status
P. New mathematical questions
```

Every statement labeled:

```text
CERTIFIED FACT
FINITE OBSERVATION
PROVED THEOREM
HYPOTHESIS
HEURISTIC
LITERATURE CONTEXT
```

---

# 24. Candidate-Phi ladder

Every `PHI-*` follows this exact ladder.

```text
PHI-GATE-0   formula well-defined on declared track
PHI-GATE-1   identity normalization
PHI-GATE-2   nonnegativity on development domain
PHI-GATE-3   candidate b_H exact and n-independent
PHI-GATE-4   correct-b canonical geometry / feasibility precheck
PHI-GATE-5   exact KEEP/DELETE residuals on development
PHI-GATE-6S  n8 contaminated validation, Track S only
PHI-GATE-7S  fresh H1, Track S only
PHI-GATE-6R  fresh H2R, Track R only
PHI-GATE-8   clean-room independent implementation
PHI-GATE-9   adversarial large-n search
PHI-GATE-10  symbolic arbitrary-n Pair Access proof
PHI-GATE-11  telescoping + bridge audit
```

The first decisive failure freezes the candidate.

Later evidence is supplementary and never rewrites the first-failure history.

Only `PHI-GATE-10` supports the Pair Access theorem.

Only `PHI-GATE-11` supports dynamic optimality.

---

# 25. Interpretation rules

## 25.1 Bellman debt

Allowed:

> `V_b(s)` is the maximum finite-state future `b`-regret extractable from the certified state under the frozen transition system.

Forbidden:

> `V_b` is the universal closed-form Splay potential.

## 25.2 Structural correlation

Allowed:

> A structural atom exactly matches canonical debt changes on the reported finite specimen family.

Forbidden:

> Therefore that atom is the missing universal potential.

## 25.3 Kernel insufficiency

Allowed:

> Under this finite kernel definition, two states are indistinguishable but require different Bellman values / primitive successors.

Forbidden:

> No structural potential of this general kind can exist, unless the stated class has been mathematically exhausted.

## 25.4 Recency separation

Allowed:

> In the exact augmented finite model, states with the same `(A,B)` but different recency orders can have different augmented Bellman debt.

Forbidden:

> Therefore every universal proof must use history.

## 25.5 Candidate holdout survival

Allowed:

> No counterexample was found in the frozen fresh bank.

Forbidden:

> The conjecture is probably solved.

## 25.6 Candidate failure

Allowed:

> The exact counterexample identifies a missing distinction in this candidate representation.

Forbidden:

> Dynamic optimality is false.

## 25.7 Negative family

Only an explicit infinite actual-cost family with unbounded ratio supports disproof.

---

# 26. Allowed claims by result level

## `FINITE_BELLMAN_DEBT_RESULTS`

Allowed:

> We exactly characterized the canonical future-regret/past-slack geometry and debt-creation/repayment transitions on the reported finite domains.

## `FINITE_KERNEL_OBSTRUCTION_RESULTS`

Allowed:

> We produced exact finite witnesses showing that specified structural kernels do not identify the required value or transition dynamics.

## `FINITE_DEBT_LAW_MINING_RESULTS`

Allowed:

> We exhausted the preregistered finite atom families and preserved exact survivors/obstructions.

## `CANDIDATE_DEBT_LAW_SURVIVES_FINITE_TESTS`

Allowed:

> A frozen explicit candidate survived its required finite development, fresh holdout, independent, and adversarial evaluations.

Not allowed:

> It works for all n.

## `UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED`

Allowed only after arbitrary-n proof.

## `APPROXIMATE_MONOTONICITY_PROVED`

Allowed only after audited telescoping.

## `DYNAMIC_OPTIMALITY_PROVED`

Allowed only after Levy-Tarjan convention audit.

## `DYNAMIC_OPTIMALITY_DISPROVED`

Allowed only after proved unbounded actual-cost family and reverse bridge.

---

# 27. Logging requirements

Every execution log contains:

```text
experiment_id
phase_id
track
UTC timestamp
repository commit
parent commit
IMPLEMENTATION_SPEC_v0.2 SHA-256
parent manifest SHA-256
prereg SHA-256
runtime versions
dependency-lock hashes
command
input hashes
holdout firewall state
candidate-set hash if applicable
exit code
stdout hash
stderr hash
output hashes
wall time metadata
peak memory metadata if available
```

Logs append-only.

Absolute paths, timestamps, CPU model, and wall time never affect scientific results.

---

# 28. Dependency/environment policy

Pin exact versions.

Python exact stack may include:

```text
Python 3.12.x
sympy
zstandard
jsonschema
networkx only for non-authoritative convenience unless independently checked
numpy/pandas for analysis only
scipy/HiGHS for discovery only
mpmath or interval package only under certified-sign policy
```

If Rust acceleration is added:

```text
exact toolchain pinned
Cargo.lock committed
Rust output independently compared to Python exact reference
```

No platform floating behavior may determine a sealed sign.

---

# 29. AI-assistance policy

AI may assist with:

```text
code generation
test design
feature brainstorming
counterexample strategy
literature triage
proof attack
prose
artifact audit
```

AI may not silently:

```text
alter inherited Splay semantics
change recency contract
change b panel
read quarantined holdouts through discovery code
define a kernel using the target
suppress a counterexample
upgrade a finite result to theorem
change a failed formula under the same ID
alter a literature-inspired definition without versioning
```

Every theorem-level mathematical statement remains the responsibility of the human author and must receive independent proof review and/or mechanical checking appropriate to the claim.

Final release includes a substantive AI-use declaration.

---

# 30. Stop conditions

Immediate stop conditions:

```text
STOP-01  parent commit mismatch
STOP-02  parent manifest mismatch
STOP-03  parent exact verifier disagreement
STOP-04  v0.2 prereg hash drift
STOP-05  structural extractor reads Bellman target
STOP-06  kernel contains target/state-ID leakage
STOP-07  behavioral quotient implementations disagree
STOP-08  Bellman transport theorem used before proof
STOP-09  recency replay mismatch
STOP-10  augmented reachable state has no legal parent witness
STOP-11  unseen recency tie silently broken
STOP-12  exact Bellman inequality fails
STOP-13  exact residual sign depends on unresolved float
STOP-14  candidate b changes without new ID
STOP-15  wrong-b geometry used
STOP-16  n8 called fresh
STOP-17  H1 read before Track S candidate freeze
STOP-18  H2R read before Track R candidate freeze
STOP-19  holdout regenerated after reveal
STOP-20  fresh holdout reused as fresh for post-reveal mutant
STOP-21  independent verifier imports discovery code
STOP-22  counterexample overwritten
STOP-23  fixed-b cycle described as DOC disproof
STOP-24  finite pattern described as asymptotic theorem
STOP-25  universal proof contains finite premise
STOP-26  proof omits declared Splay/recency case
STOP-27  bridge convention mismatch
STOP-28  archive manifest incomplete
STOP-29  final claim not recomputable from artifacts
STOP-30  scientific file deleted to make seal clean
```

A stop is evidence, not permission for silent repair.

Repairs create a documented new run/version.

---

# 31. Completion checklist

## Foundation

- [ ] parent commit verified
- [ ] parent seal verified
- [ ] parent WorkPlan/Path preserved
- [ ] v0.2 spec frozen
- [ ] literature frozen
- [ ] theorem ledger frozen
- [ ] H1 firewall verified
- [ ] n8 contamination preserved

## Bellman debt

- [ ] b=2 U/V/G reverified n=2..7
- [ ] Bellman signatures complete
- [ ] V-tight edges complete
- [ ] U-tight edges complete
- [ ] KEEP excess table complete
- [ ] DELETE creation table complete
- [ ] exact repayment table complete
- [ ] independent verifier passes

## Structural ontology

- [ ] target-blind extractor
- [ ] pair-tree primitives
- [ ] rank primitives
- [ ] interval/nesting primitives
- [ ] crossing primitives
- [ ] heavy/gap mapping
- [ ] inversion-like mapping
- [ ] bounded multiscale primitives
- [ ] symmetry tests

## Behavioral quotient

- [ ] exact partition refinement
- [ ] fixed point
- [ ] independent agreement
- [ ] cost preservation
- [ ] successor preservation
- [ ] Bellman transport theorem reviewed
- [ ] compression report

## Kernel sharpness

- [ ] overcomplete K0
- [ ] every planned ablation
- [ ] value insufficiency witnesses
- [ ] transition insufficiency witnesses
- [ ] behavioral-class witnesses
- [ ] no minimality overclaim

## Recency track

- [ ] recency update contract
- [ ] recency replay theorem
- [ ] exact augmented n<=4 reachability
- [ ] augmented b=2 U/V/G
- [ ] same-pair/different-recency table
- [ ] recency ontology
- [ ] H2R bank committed
- [ ] H2R firewall blocks discovery

## Debt atoms

- [ ] delta-first tables
- [ ] cheap-DELETE audit
- [ ] expensive-KEEP audit
- [ ] exact atom searches
- [ ] minimal inconsistent witnesses
- [ ] scale audit

## Candidates

- [ ] formula frozen
- [ ] track frozen
- [ ] b_H frozen
- [ ] identity checked
- [ ] nonnegativity checked
- [ ] correct-b geometry checked
- [ ] development residuals exact
- [ ] candidate-set commitment

## Holdouts

- [ ] n8 correctly labeled contaminated
- [ ] H1 only if Track S survivor
- [ ] H2R only if Track R survivor
- [ ] unlock once
- [ ] independent replay
- [ ] post-holdout mutants new IDs

## Independent/adversarial

- [ ] clean-room implementation
- [ ] structured adversaries
- [ ] history adversaries
- [ ] mutation controls
- [ ] smallest exact counterexamples

## Universal proof

- [ ] arbitrary-n formula
- [ ] nonnegativity proof
- [ ] identity proof
- [ ] DELETE proof
- [ ] KEEP proof
- [ ] all Splay cases
- [ ] all recency cases if needed
- [ ] kernel lift if needed
- [ ] no finite premise
- [ ] universal b

## Bridge

- [ ] telescoping
- [ ] approximate monotonicity statement
- [ ] Levy-Tarjan convention audit
- [ ] final constant statement precise

## Negative branch

- [ ] activation criteria
- [ ] closed-form family
- [ ] symbolic X upper bound
- [ ] symbolic Y lower bound
- [ ] ratio limit
- [ ] reverse bridge

## Seal

- [ ] FINAL_RESULT generated from artifacts
- [ ] manifest complete
- [ ] deterministic archive
- [ ] fresh reproduction
- [ ] failed candidates retained
- [ ] all counterexamples retained
- [ ] AI-use statement
- [ ] claim level exact

---

# 32. Final success definitions

## 32.1 Finite Bellman-debt success

v0.2 is already a successful finite experiment if it produces an independently verified structural characterization of:

```text
where canonical debt is created,
where it is repaid,
which edges are Bellman-tight,
and which structural kernels fail to explain it.
```

No candidate potential is required for this success level.

## 32.2 Kernel-discovery success

A kernel result is structurally successful when it yields a compact, target-blind, mathematically interpretable signature that preserves the primitive dynamics needed by the debt law across development sizes and survives componentwise sharpness tests.

This remains finite evidence until a universal kernel theorem is proved.

## 32.3 Conserved-resource discovery success

A candidate `Phi` is scientifically strong when it:

```text
- has a natural structural interpretation;
- explains debt creation and repayment;
- survives exact development;
- survives the correct fresh holdout;
- survives independent implementation;
- survives adversarial large-n attack;
- uses n-independent constants.
```

Still not a theorem.

## 32.4 Mathematical solution success

The original Dynamic Optimality Conjecture is proved by this route only when:

```math
\Phi(z_0)=0,
\qquad
\Phi(z)\ge0,
```

and for one universal `b` every legal arbitrary-n transition satisfies:

KEEP:
```math
c(B,x)+\Phi(z')-\Phi(z)\le b\,c(A,x),
```

DELETE:
```math
\Phi(z')-\Phi(z)\le b\,c(A,x).
```

Then telescoping proves approximate monotonicity.

After convention-matched Levy-Tarjan invocation, Dynamic Optimality follows.

## 32.5 Mathematical disproof success

Only an explicit infinite actual Splay/subsequence family with unbounded ratio counts.

No finite candidate failure can substitute.

---

# 33. Immediate Experiment-0 deliverable

The first v0.2 milestone is intentionally narrower than a new potential.

Using inherited `n=2..7` state-only geometry at `b=2`, produce a sealed bundle:

```text
A. verified parent import ledger
B. complete BELL-SIG-v0.2 tables
C. complete KEEP_EXCESS tables
D. complete DELETE CANONICAL_CREATION tables
E. complete EXACT_V_REPAYMENT tables
F. complete V-tight/U-tight edge sets
G. target-blind structural ontology
H. exact behavioral quotient
I. structural-kernel ablation witnesses
J. canonical human-readable debt trajectories
K. exact atom-delta tables for preregistered structural families
L. independent verification report
```

The first theorem-mining question is:

> **What structural resource increases on debt-creating DELETE transitions and decreases by at least the required excess on expensive KEEP transitions?**

The second is:

> **What is the smallest target-blind state signature capable of predicting the relevant debt dynamics?**

Only after those questions are answered does candidate synthesis begin.

---

# 34. Recommended first paper/notebook tables

## Table A - inherited exact foundation

```text
n | C_n | |R_n| | b_n^* | max U_2 | max V_2 | #forced at b=2
```

## Table B - debt creation/repayment

```text
n | #KEEP_EXCESS | #EXACT_V_REPAYMENT | #DELETE_CREATION | max KEEP excess | max DELETE DeltaV
```

## Table C - Bellman tight geometry

```text
n | #V-tight | #U-tight | #both-tight | KEEP share | DELETE share
```

## Table D - behavioral quotient

```text
n | #states | #behavior classes | compression | largest class | singleton fraction
```

## Table E - kernel sharpness

```text
kernel | removed coordinate | smallest failure n | value mismatch | transition mismatch | witness
```

## Table F - recency augmentation

```text
n | augmented states | same-(A,B) recency variants | value-separated groups | max V spread
```

## Table G - debt atom families

```text
atom family | DELETE bounded? | KEEP repayment? | V-tight equality? | cross-n stable? | status
```

## Table H - candidate laws

```text
Phi ID | track | b_H | dev | EV8 | H1/H2R | independent | adversarial | proof | status
```

Exact values and display decimals must be separated.

---

# 35. External references to freeze

1. Daniel D. Sleator and Robert E. Tarjan. **Self-Adjusting Binary Search Trees.** Journal of the ACM, 1985.
2. Caleb C. Levy and Robert E. Tarjan. **A Foundation for Proving Splay is Dynamically Optimal.** Frozen selected version of arXiv:1907.06310.
3. Petr Chmel, Bernhard Haeupler, Richard Hladik, Michal Koucky, Antti Roeyskoe, Vaclav Rozhon, Ondrej Sladky, and Robert E. Tarjan. **Splay trees are almost dynamically optimal.** Frozen selected version of arXiv:2607.18498, 2026.
4. Parinya Chalermsook and Wanchote Po Jiamjitrak. **New Binary Search Tree Bounds via Geometric Inversions.** ESA 2020, DOI 10.4230/LIPIcs.ESA.2020.28.
5. `SPLAY-AM-PD-v0.1` sealed release, commit `6de1ca2`.

The v0.2 release stores local immutable copies or content hashes.

---

# 36. Final frozen statement of purpose

The experiment is complete only when its artifacts can answer, without ambiguity:

```text
1. Was the parent v0.1 seal imported exactly?
2. What does V_b mean operationally in the paired transition system?
3. At b=2, exactly where is future regret created by DELETE?
4. At b=2, exactly where is excess KEEP cost repaid by a debt decrease?
5. Which transitions are Bellman-tight?
6. What target-blind behavioral quotient preserves primitive paired dynamics?
7. How much does that quotient compress the finite state space?
8. Which structural coordinates are componentwise necessary to reproduce the quotient/value behavior?
9. Which pair-state structural kernels fail, with what exact witnesses?
10. Does relative recency add finite identification power beyond (A,B)?
11. If so, what exact recency distinction matters?
12. Which recency/crossing/interval/rank/inversion/gap-inspired atoms track debt changes?
13. Which atom families are exactly inconsistent with the required creation/repayment laws?
14. What candidate conserved-resource laws survive development?
15. Which candidate is killed by which smallest exact counterexample?
16. Was the correct fresh holdout used for each track?
17. Did any candidate survive independent and adversarial falsification?
18. Has any candidate been proved for arbitrary n?
19. If yes, are KEEP and DELETE both proved under one n-independent b?
20. Does the potential telescope from synchronized initial state?
21. Does that prove approximate monotonicity under the frozen convention?
22. Does the exact Levy-Tarjan bridge then prove Dynamic Optimality?
23. If the positive route fails, is there an actual Splay-cost motif rather than merely an H-residual motif?
24. If so, has it been converted to a closed-form infinite family?
25. Does that family's subsequence-overhead ratio provably diverge?
26. What is the strongest claim level justified by artifacts alone?
27. Can an independent researcher reproduce that claim from a fresh checkout?
```

The implementation must be allowed to answer any of these questions negatively.

The governing scientific principle is:

> **Every failed representation must either yield an exact missing distinction or remain honestly unexplained; every theorem claim must be universal.**

The experiment's immediate objective is not "fit a better potential."

It is:

```math
\boxed{
\text{identify the conserved resource represented by Bellman debt}
}
```

and then determine whether that resource can be proved to obey:

```math
\boxed{
\text{DELETE creates only bounded debt}
\quad\land\quad
\text{expensive KEEP consumes proportional debt}.
}
```

If that universal conservation law exists and is proved, the Pair Access inequalities follow, approximate monotonicity follows, and - after the audited Levy-Tarjan bridge - the original Dynamic Optimality Conjecture is resolved positively.

If instead the exact paired dynamics expose a closed-form family whose required competitive factor diverges, the conjecture is resolved negatively.

Anything in between remains finite theorem-discovery evidence.

**Fail open to mathematical evidence. Fail closed to theorem claims.**
