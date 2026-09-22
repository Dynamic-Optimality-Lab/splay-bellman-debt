# REPRODUCIBILITY.md — fresh-checkout reproduction (SEAL-01)

```sh
git clone https://github.com/Dynamic-Optimality-Lab/splay-bellman-debt
cd splay-bellman-debt
sh scripts/reproduce_all_v0.2.sh
```

The script verifies (fail-closed): parent seal (PARENT-01..06), prereg hashes,
ledger BD0 set, small-size rebuilds (n≤4 Splay tables + reachability +
extraction + quotient agreement), b=2 spot reverify, candidate/counterexample
reverify (PHI residuals recomputed), holdout commitments + firewall states,
FINAL_RESULT recompute equality, manifest coverage, archive determinism
(rebuild + SHA compare).

Full n≤7 rebuilds are documented in phase logs (already executed); the
reproduction script favors fast exact spot-checks plus hash-locked artifacts
for the largest sizes, and says so where it does.
Python >=3.12, stdlib + zstandard required (see requirements-lock.txt).
No network access needed except the initial clone (parent evidence is vendored
under parent/; H2R bank is committed).
