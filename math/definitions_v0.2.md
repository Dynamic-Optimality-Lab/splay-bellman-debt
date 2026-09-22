# definitions_v0.2.md — frozen mathematical contract (inherits parent, never redefines)

Keys `[n]`, BST universe `T_n`, canonical encoding, root depth 0,
cost `c(T,x)=depth+1`, bottom-up Splay `S_x(T)`, pair `(A,B)`,
diagonal `Δ_n`, KEEP `K_x(A,B)=(S_xA,S_xB)`, DELETE `D_x(A,B)=(S_xA,B)`,
reachable domain `R_n`, exact rational conventions with `L_{p,q}=p·a−q·y`.

Fixed-b: `w_b=y−b·a`, `ℓ_b=b·a−y`, `U_b=inf_{Δ⇝s}Σℓ_b`,
`V_b=sup_{s⇝*}Σw_b` (empty continuation allowed), corridor `V_b≤H≤U_b`
for pair-state potentials only. Augmented state `(A,B,ρX,ρY)` with
relative recency lists, KEEP updates both, DELETE updates X only,
initial `(T,T,[],[])`. SA-01: `R_π` one-way blindness ⇒ same-`(A,B)`
same `V_b^R`.
