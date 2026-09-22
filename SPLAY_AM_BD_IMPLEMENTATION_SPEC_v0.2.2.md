# SPLAY-AM-BD v0.2.2 — Spec Amendment SA-02 (ratified)

**Parent spec:** `SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.md` + SA-01 (`SPLAY_AM_BD_IMPLEMENTATION_SPEC_v0.2.1.md`)
**Amendment:** SA-02 — literature freeze methods for inaccessible sources
**Status:** RATIFIED (2026-09-22) — triggered by WP-1 post-completion audit (literature-freeze gap)
**Normative effect:** clarifies section 3 ledger requirements; base + SA-01 unchanged
except where stated; no frozen bytes rewritten; no history rewrite.

## Rule

A literature source is frozen by one explicit method:

```text
LOCAL_BYTES            exact local PDF bytes, SHA-256 recorded
PARENT_INHERITED_BYTES exact bytes inherited from the sealed parent by verified hash
BIBLIOGRAPHIC_IDENTITY immutable canonical identity (no legal local bytes available)
```

`BIBLIOGRAPHIC_IDENTITY` records: title, authors, venue, year,
volume/issue/pages where available, DOI or canonical identifier,
retrieval URL or metadata endpoint, retrieval UTC timestamp, logical
role, exact sections/results relied upon, and
`local_bytes_present: false`. It is a terminal freeze state, not a
placeholder. Paywalls are never bypassed. A DOI string alone without
this record is not a freeze.

## Application

- L1 (Sleator–Tarjan 1985): no legal local bytes in parent or
  repository. Frozen by `BIBLIOGRAPHIC_IDENTITY` (DOI
  `10.1145/3828.3835`, JACM 32(3):652–686, 1985). Reliance limited to
  the widely reproduced bottom-up splaying definition, cross-checked
  by parent fixtures and independent implementations.
- L4 (Chalermsook–Jiamjitrak ESA 2020): publicly available CC-BY
  publication. Frozen by `LOCAL_BYTES`
  (`external/papers/L4_geometric_inversions_2020.pdf`).

## Ratification record

- Audit: WP-1 post-completion literature gap (2026-09-22).
- This file is new; `IMPLEMENTATION_SPEC_v0.2.md` and SA-01 bytes preserved.
- Ledger: `external/MANIFEST.json` carries per-source `freeze_method`.
