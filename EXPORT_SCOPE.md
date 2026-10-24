# Release readiness and reproduction boundary

## Verified in GitHub Actions

The 2026-10-24 [run 40136118512](https://github.com/hollylessthan/context-graph-analytics-artifact/actions/runs/40136118512) passed all three offline checks on the committed evidence:

- Source-frozen original comparison summaries: 30/36 and 25/36.
- Stage-local evidence ZIP: four matching compressed-source hashes, 576 factorial contexts, all 16 factorial counts, 44 packing-only changed sets, and stage-local change totals.
- Paired scored-results ZIP: 264 operations, 132 pairs, 44 cases, and the 92/34/6/0 pass-transition table, with per-entry integrity checks.

These checks **re-aggregate frozen evidence**, not regenerate graph construction, retrieve contexts from source catalogs, run SQL, or call LLMs. Do not claim full experiment re-execution.

## Remaining release gates

1. Inspect released archives for credentials, secrets, personal information, and licensing restrictions. Do not assume a successful checksum test implies publication safety.
2. Preserve a manifest tying this export to the frozen source commits, run IDs, original archive hashes, and artifact commit. The metadata in `PROVENANCE.md` is a first step, not a substitute for a complete byte-level manifest.
3. Decide whether a full deterministic retrieval/scoring rerun is needed. If so, export minimally necessary code and pinned dependencies, and test them separately. It is not necessary for the current frozen-result re-aggregation claim.
4. Make the exact verified commit immutable as `artifact-v1.0`, archive that release on Zenodo and check that Zenodo contains the expected evidence ZIP files.
5. Only after the DOI exists, cite that fixed archive from the paper.

No new paid model calls are required or authorized.
