# Release readiness and reproduction boundary

## Verified in GitHub Actions

The 2026-10-24 [run 40136118512](https://github.com/hollylessthan/context-graph-analytics-artifact/actions/runs/40136118512) passed the archived offline checks on the committed evidence:

- Source-frozen original comparison summaries: 30/36 and 25/36.
- Stage-local evidence ZIP: four matching compressed-source hashes, 576 factorial contexts, all 16 factorial counts, 44 packing-only changed sets, and stage-local change totals.
- Paired scored-results ZIP: 264 operations, 132 pairs, 44 cases, and the 92/34/6/0 pass-transition table, with per-entry integrity checks.

These checks **re-aggregate frozen evidence**, not regenerate graph construction, retrieve contexts from source catalogs, run SQL, or call LLMs. Do not claim full experiment re-execution.

## Archived release and remaining scope

1. **Completed preliminary publication scan:** reviewer inspection reported no credentials, tokens, email addresses, or home-directory paths in the exported artifacts. This is not a guarantee against every possible sensitive datum or license issue; the documented third-party license review remains relevant.
2. Preserve a manifest tying this export to the frozen source commits, run IDs, original archive hashes, and artifact commit. The metadata in `PROVENANCE.md` is a first step, not a substitute for a complete byte-level manifest.
3. Decide whether a full deterministic retrieval/scoring rerun is needed. If so, export minimally necessary code and pinned dependencies, and test them separately. It is not necessary for the current frozen-result re-aggregation claim.
4. The original frozen artifact was released as `artifact-v1.0` at DOI [10.5281/zenodo.23628013](https://doi.org/10.5281/zenodo.23628013). Its archival files remain unchanged.
5. Documentation and provenance corrections were released as `artifact-v1.0.1` at DOI [10.5281/zenodo.23628731](https://doi.org/10.5281/zenodo.23628731). The experimental evidence is identical; the manuscript cites this updated release. Existing Zenodo archives are immutable and may contain the metadata text present at their respective tags.

No new paid model calls are required or authorized.
