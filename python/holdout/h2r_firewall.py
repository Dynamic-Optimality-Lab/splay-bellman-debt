"""H2R firewall: EMPTY -> BANK_COMMITTED -> CANDIDATE_SET_FROZEN -> UNLOCKED_ONCE.

No backwards transitions. Second unlock or regen-after-reveal fails closed.
Discovery namespaces must call guard() before any bank read; guard raises
unless the state machine permits it.
"""
from __future__ import annotations

import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


STATES = ["EMPTY", "BANK_COMMITTED", "CANDIDATE_SET_FROZEN", "UNLOCKED_ONCE"]


def state_file(repo_root: Path) -> Path:
    return repo_root / "artifacts" / "v02" / "holdouts" / "H2R" / "firewall.json"


def read_state(repo_root: Path) -> dict:
    sf = state_file(repo_root)
    if not sf.is_file():
        return {"state": "EMPTY", "unlocks": 0}
    return json.loads(sf.read_text(encoding="utf-8"))


def write_state(repo_root: Path, state: dict) -> None:
    state_file(repo_root).write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def transition(repo_root: Path, to: str) -> dict:
    cur = read_state(repo_root)["state"]
    order = {s: i for i, s in enumerate(STATES)}
    if order[to] != order[cur] + 1:
        raise RuntimeError(f"firewall illegal transition {cur} -> {to}")
    st = read_state(repo_root)
    st["state"] = to
    if to == "UNLOCKED_ONCE":
        st["unlocks"] = st.get("unlocks", 0) + 1
        if st["unlocks"] > 1:
            raise RuntimeError("firewall second unlock blocked")
    write_state(repo_root, st)
    # console.log equivalent [WP4-FW-01]: firewall transition
    console_log(f"[WP4-FW-01] firewall {cur} -> {to}")
    return st


def guard_discovery_read(repo_root: Path) -> None:
    # Discovery namespaces call this before any bank-content read.
    # Bank content is NEVER readable by discovery code, in any state:
    # only the post-unlock evaluation harness (not discovery) may read it.
    raise RuntimeError("firewall blocks discovery read of H2R bank content")
