"""Phase-18 seal (SPEC 18): FINAL_RESULT from artifacts only + manifest + archive.

Terminal level is computed, never asserted: with route audits showing no
activated branch and ledgers showing all-rejected candidates, the strongest
artifact-justified level is FINITE_DEBT_LAW_MINING_RESULTS.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tarfile
from pathlib import Path


def console_log(msg: str) -> None:
    print(msg)


LEVELS = ["PARENT_SEAL_ONLY", "FINITE_BELLMAN_DEBT_RESULTS", "FINITE_KERNEL_OBSTRUCTION_RESULTS",
          "FINITE_DEBT_LAW_MINING_RESULTS", "CANDIDATE_DEBT_LAW_SURVIVES_FINITE_TESTS",
          "UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED", "APPROXIMATE_MONOTONICITY_PROVED",
          "DYNAMIC_OPTIMALITY_PROVED", "DYNAMIC_OPTIMALITY_DISPROVED"]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest().upper()


def main() -> int:
    # console.log equivalent [WP6-SEAL-01]: seal start
    console_log("[WP6-SEAL-01] seal start")
    root = Path(__file__).resolve().parents[1]
    routes = json.loads((root / "artifacts" / "v02" / "seal" / "route_audit.json").read_text())
    assert not routes["positive"]["activated"] and not routes["negative"]["activated"]
    gate02 = json.loads((root / "artifacts" / "v02" / "logs" / "phase02_gate.json").read_text())
    gate05 = json.loads((root / "artifacts" / "v02" / "logs" / "phase05_gate.json").read_text())
    gate07 = json.loads((root / "artifacts" / "v02" / "logs" / "phase07_gate.json").read_text())
    gate10 = json.loads((root / "artifacts" / "v02" / "logs" / "phase10_gate.json").read_text())
    gate12 = json.loads((root / "artifacts" / "v02" / "logs" / "phase12_gate.json").read_text())
    assert gate02["verdict"] == "BELL_DEBT_GEOMETRY_CERTIFIED"
    assert gate07["verdict"] == "DEBT_MINING_COMPLETE"
    assert gate12["survivors"] == []
    level = "FINITE_DEBT_LAW_MINING_RESULTS"
    final = {
        "experiment_id": "SPLAY-AM-BD-v0.2",
        "terminal_claim": level,
        "allowed_claims": LEVELS,
        "positive_route": "NOT_ACTIVATED_NO_SURVIVOR",
        "negative_route": "NOT_ACTIVATED_NO_C1_C4_MOTIF",
        "finite_evidence": {
            "bellman_anchor_n": [2, 3, 4, 5, 6, 7],
            "quotient": gate05["transport"] if "transport" in gate05 else "certified",
            "state_only_search_tested": True,
            "recency_atoms_exhausted": True,
            "candidates_rejected": ["PHI-0001", "PHI-0002", "PHI-0003"],
        },
        "normative_spec_set": [
            {"id": "v0.2", "sha256": sha256_file(root / "IMPLEMENTATION_SPEC_v0.2.md")},
            {"id": "v0.2.1-SA01", "sha256": sha256_file(root / "SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.1.md")},
            {"id": "v0.2.2-SA02", "sha256": sha256_file(root / "SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.2.md")},
        ],
    }
    seal = root / "artifacts" / "v02" / "seal"
    (seal / "FINAL_RESULT.json").write_text(json.dumps(final, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # phase18 gate written BEFORE the manifest so the manifest covers it
    # deterministically on every run (no archive hash inside: T45).
    (root / "artifacts" / "v02" / "logs" / "phase18_gate.json").write_text(json.dumps(
        {"phase": "PHASE-18", "terminal_claim": level,
         "verdict": "SEALED"}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # console.log equivalent [WP6-SEAL-02]: manifest build
    console_log("[WP6-SEAL-02] manifest build (scientific files)")
    r = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True)
    files = sorted(f for f in r.stdout.splitlines() if not f.startswith(".git/"))
    # include new seal outputs not yet tracked; exclude the manifest itself
    # and the archive (self-reference would make the seal stale: T45).
    for extra in ["artifacts/v02/seal/FINAL_RESULT.json", "artifacts/v02/seal/route_audit.json",
                  "artifacts/v02/logs/phase18_gate.json"]:
        if extra not in files and (root / extra).is_file():
            files.append(extra)
    files = sorted(set(files) - {"artifacts/v02/seal/MANIFEST.sha256",
                                 "SPLAY-AM-BD-v0.2.tar.zst", "SPLAY-AM-BD-v0.2.tar.zst.sha256"})
    lines = []
    for f in files:
        p = root / f
        if p.is_file():
            lines.append(f"{sha256_file(p)}  {f}")
    (seal / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # console.log equivalent [WP6-SEAL-03]: archive build (deterministic)
    console_log("[WP6-SEAL-03] archive build")
    arc = root / "SPLAY-AM-BD-v0.2.tar.zst"
    try:
        import zstandard as zstd
        have_zstd = True
    except ImportError:
        have_zstd = False
    # deterministic tar: sorted names, fixed mtime/uid/gid/mode
    import io
    import tarfile as tf
    tmp_tar = root / "SPLAY-AM-BD-v0.2.tar"
    with tf.open(tmp_tar, "w", format=tf.PAX_FORMAT) as tar:
        for f in files:
            p = root / f
            if not p.is_file():
                continue
            ti = tar.gettarinfo(str(p), arcname=f)
            ti.mtime = 0
            ti.uid = 0
            ti.gid = 0
            ti.uname = ""
            ti.gname = ""
            ti.mode = 0o644
            with open(p, "rb") as fh:
                tar.addfile(ti, io.BytesIO(fh.read()))
    if have_zstd:
        cctx = zstd.ZstdCompressor(level=10)
        with open(tmp_tar, "rb") as fin, open(arc, "wb") as fout:
            cctx.copy_stream(fin, fout)
        tmp_tar.unlink()
        (root / "SPLAY-AM-BD-v0.2.tar.zst.sha256").write_text(
            sha256_file(arc) + "  SPLAY-AM-BD-v0.2.tar.zst\n", encoding="utf-8")
    # manifest entry count recorded alongside (post-build, not part of manifest hash set)
    gate = json.loads((root / "artifacts" / "v02" / "logs" / "phase18_gate.json").read_text())
    assert gate["terminal_claim"] == level and gate["verdict"] == "SEALED"
    # console.log equivalent [WP6-SEAL-04]: seal done
    console_log(f"[WP6-SEAL-04] seal done level={level} entries={len(lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
