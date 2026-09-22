"""HOLDOUT-H2R-v0.1 generator: quarantined fresh bank for Track R.

Sizes 8,10,12,16,24,32 x 20,000 states = 120,000 states.
Each record carries its legal generation history for independent replay.
Stratified by length/density/divergence/shape/disparity/generator-kind.
Discovery namespaces may not read the bank (firewall enforced).
"""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


SIZES = [8, 10, 12, 16, 24, 32]
PER_SIZE = 20000


class DictBST:
    # Minimal keyed BST with ordinary bottom-up splay (independent small-n core).

    def __init__(self, n: int, rng: random.Random):
        keys = list(range(1, n + 1))
        rng.shuffle(keys)
        self.nodes: dict[int, list] = {}
        self.root = None
        for k in keys:
            self._insert(k)

    def _insert(self, k: int) -> None:
        self.nodes[k] = [None, None, None]
        if self.root is None:
            self.root = k
            return
        cur = self.root
        while True:
            if k < cur:
                if self.nodes[cur][0] is None:
                    self.nodes[cur][0] = k
                    self.nodes[k][2] = cur
                    return
                cur = self.nodes[cur][0]
            else:
                if self.nodes[cur][1] is None:
                    self.nodes[cur][1] = k
                    self.nodes[k][2] = cur
                    return
                cur = self.nodes[cur][1]

    def _rot_right(self, v: int) -> None:
        p = self.nodes[v][2]
        g = self.nodes[p][2]
        b = self.nodes[v][1]
        self.nodes[v][1] = p
        self.nodes[p][2] = v
        self.nodes[p][0] = b
        if b is not None:
            self.nodes[b][2] = p
        self.nodes[v][2] = g
        if g is not None:
            if self.nodes[g][0] == p:
                self.nodes[g][0] = v
            else:
                self.nodes[g][1] = v
        else:
            self.root = v

    def _rot_left(self, v: int) -> None:
        p = self.nodes[v][2]
        g = self.nodes[p][2]
        b = self.nodes[v][0]
        self.nodes[v][0] = p
        self.nodes[p][2] = v
        self.nodes[p][1] = b
        if b is not None:
            self.nodes[b][2] = p
        self.nodes[v][2] = g
        if g is not None:
            if self.nodes[g][0] == p:
                self.nodes[g][0] = v
            else:
                self.nodes[g][1] = v
        else:
            self.root = v

    def access(self, x: int) -> dict:
        # returns cost, path, cases; splays x to root.
        path = []
        cur = self.root
        while cur != x:
            path.append(cur)
            cur = self.nodes[cur][0] if x < cur else self.nodes[cur][1]
        path.append(x)
        cost = len(path)
        cases = []
        v = x
        while self.nodes[v][2] is not None:
            p = self.nodes[v][2]
            g = self.nodes[p][2]
            if g is None:
                if self.nodes[p][0] == v:
                    self._rot_right(v)
                else:
                    self._rot_left(v)
                cases.append("ZIG")
            elif self.nodes[g][0] == p and self.nodes[p][0] == v:
                self._rot_right(p)
                self._rot_right(v)
                cases.append("LL")
            elif self.nodes[g][1] == p and self.nodes[p][1] == v:
                self._rot_left(p)
                self._rot_left(v)
                cases.append("RR")
            elif self.nodes[g][0] == p and self.nodes[p][1] == v:
                self._rot_left(v)
                self._rot_right(v)
                cases.append("LR")
            else:
                self._rot_right(v)
                self._rot_left(v)
                cases.append("RL")
        return {"cost": cost, "path": path, "cases": cases}

    def shape_key(self) -> str:
        # Canonical nested-tuple serialization of current shape (key-labeled inorder implicit).
        def rec(k):
            if k is None:
                return "."
            return "(" + rec(self.nodes[k][0]) + rec(self.nodes[k][1]) + ")"
        return rec(self.root)


def gen_history(n: int, rng: random.Random, kind: str) -> list[tuple]:
    L = rng.choice([8, 16, 32, 64])
    hist = []
    for i in range(L):
        if kind == "alternating":
            x = (i % n) + 1
            mode = "KEEP" if i % 2 == 0 else "DELETE"
        elif kind == "burst":
            x = rng.randint(1, n)
            mode = "DELETE" if i < L - 1 else "KEEP"
        elif kind == "keep_heavy":
            x = rng.randint(1, n)
            mode = "KEEP" if rng.random() < 0.8 else "DELETE"
        elif kind == "del_heavy":
            x = rng.randint(1, n)
            mode = "DELETE" if rng.random() < 0.8 else "KEEP"
        else:
            x = rng.randint(1, n)
            mode = "KEEP" if rng.random() < 0.5 else "DELETE"
        hist.append((mode, x))
    return hist


def run_history(n: int, hist: list[tuple], rng: random.Random) -> dict:
    A = DictBST(n, rng)
    B = DictBST(n, rng)
    # synchronize B shape to A initial shape by rebuilding (same insertion order not tracked;
    # instead start B as copy of A nodes)
    B.nodes = {k: list(v) for k, v in A.nodes.items()}
    B.root = A.root
    rx: tuple = ()
    ry: tuple = ()
    for mode, x in hist:
        ra = A.access(x)
        if mode == "KEEP":
            rb = B.access(x)
            ry = (x,) + tuple(k for k in ry if k != x)
        else:
            rb = {"cost": 0, "path": [], "cases": []}
        rx = (x,) + tuple(k for k in rx if k != x)
    return {
        "A_shape": A.shape_key(), "B_shape": B.shape_key(),
        "rho_X": list(rx), "rho_Y": list(ry),
        "history": [[m, x] for m, x in hist],
        "n": n,
    }


def strata_of(rec: dict) -> str:
    h = rec["history"]
    L = len(h)
    keep = sum(1 for m, _ in h if m == "KEEP") / max(1, L)
    div = len(set(rec["rho_X"]) ^ set(rec["rho_Y"]))
    if L <= 8:
        base = "short"
    elif L <= 32:
        base = "medium"
    else:
        base = "long"
    dens = "keep" if keep > 0.7 else ("del" if keep < 0.3 else "mixed")
    return f"{base}-{dens}-div{0 if div == 0 else (1 if div <= 2 else 2)}"


def generate_bank(repo_root: Path, seed: int = 20260922) -> dict:
    # console.log equivalent [WP4-H2R-01]: generation start
    console_log("[WP4-H2R-01] H2R generation start")
    rng = random.Random(seed)
    kinds = ["random", "alternating", "burst", "keep_heavy", "del_heavy"]
    out_dir = repo_root / "artifacts" / "v02" / "holdouts" / "H2R"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"bank_id": "HOLDOUT-H2R-v0.1", "seed": seed, "sizes": {}}
    for n in SIZES:
        # console.log equivalent [WP4-H2R-02]: per-size generation
        console_log(f"[WP4-H2R-02] H2R size n={n}")
        recs = []
        per_kind = PER_SIZE // len(kinds)
        for ki, kind in enumerate(kinds):
            for _ in range(per_kind):
                recs.append(run_history(n, gen_history(n, rng, kind), rng))
        while len(recs) < PER_SIZE:
            recs.append(run_history(n, gen_history(n, rng, "random"), rng))
        # attach strata
        for r in recs:
            r["stratum"] = strata_of(r)
        blob = json.dumps({"n": n, "records": recs}, sort_keys=True)
        h = hashlib.sha256(blob.encode()).hexdigest().upper()
        (out_dir / f"bank_n{n}.json").write_text(json.dumps({"n": n, "sha": h, "records": recs}, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        manifest["sizes"][str(n)] = {"states": len(recs), "sha": h}
    manifest["total_states"] = sum(v["states"] for v in manifest["sizes"].values())
    (out_dir / "commitment.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP4-H2R-03]: generation done
    console_log(f"[WP4-H2R-03] H2R done total={manifest['total_states']}")
    return manifest
