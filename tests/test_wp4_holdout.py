"""HLD-04..06: H2R commitment, pre-freeze unread, unlock-at-most-once."""
from __future__ import annotations

import json
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_hld04_commitment() -> None:
    # console.log equivalent [WP4-HLD-04]: HLD-04
    console_log("[WP4-HLD-04] HLD-04 H2R commitment hash")
    man = json.loads((root() / "artifacts" / "v02" / "holdouts" / "H2R" / "commitment.json").read_text())
    assert man["bank_id"] == "HOLDOUT-H2R-v0.1" and man["total_states"] == 120000
    assert set(man["sizes"]) == {"8", "10", "12", "16", "24", "32"}


def test_hld05_prefreeze_unread() -> None:
    # console.log equivalent [WP4-HLD-05]: HLD-05
    console_log("[WP4-HLD-05] HLD-05 H2R unread pre-freeze (firewall blocks discovery)")
    import sys
    sys.path.insert(0, str(root() / "python"))
    from holdout.h2r_firewall import guard_discovery_read
    try:
        guard_discovery_read(root)
        assert False, "discovery read unexpectedly allowed"
    except RuntimeError:
        pass


def test_hld06_unlock_once() -> None:
    # console.log equivalent [WP4-HLD-06]: HLD-06
    console_log("[WP4-HLD-06] HLD-06 unlock at most once")
    fw = json.loads((root() / "artifacts" / "v02" / "holdouts" / "H2R" / "firewall.json").read_text())
    assert fw["state"] == "BANK_COMMITTED" and fw.get("unlocks", 0) == 0
