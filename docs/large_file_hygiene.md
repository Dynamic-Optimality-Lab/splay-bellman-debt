# Large-file hygiene policy (WP-3 closure; non-normative guidance)

Git history is never rewritten to remove committed evidence
(`structure/n7.json`, `specimens/n7/signatures.json` remain as-is).

For future large artifacts:

- prefer deterministic `.json.zst` (canonical JSON bytes, sorted keys,
  fixed compression level) over raw `.json`;
- or deterministic sharding (`n7_part_00.json`, ...) with a manifest of
  per-shard SHA-256 plus a logical-stream SHA-256 of the concatenation;
- record logical-stream SHA-256 in the phase gate log;
- verify by stream-decode + hash, never by file-size heuristics.

This policy does not alter logical scientific content and does not
block theorem closure.
