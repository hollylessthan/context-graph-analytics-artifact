# Export and release gates

This PR includes frozen summary records, paired scored outcomes, SQL, contexts and human-readable provenance. Paired outcome counts are reproducible offline; the full original/factorial benchmark is not yet independently reproducible.

## Required before release
1. **Pending repo upload:** Four original stage-local source files have been provided and their hashes, 576 context records, and 864 stage contrasts were checked offline. Add `evidence/stage-local-evidence.zip` to enable the built-in trace re-aggregation in CI. Original paths: `evaluation/followup/label-stage-audit/{catalogs,factorial,pairs,support}.json.gz`; verify source hashes.
2. **Completed for scored outcomes:** The curated paired evidence ZIP from research Actions run 40120563599 is committed and integrity-checked. It contains scored-results, contexts, provider trace, plan and paired summaries. Opaque model-response payloads were excluded. Raw text-level response replication is outside this sanitized export's scope.
3. Import minimal deterministic retrieval, analysis, and scoring code with pinned dependencies and licenses.
4. Regenerate all paper tables from raw saved evidence in one offline command, not from manually copied expected counts.
5. Generate source commit and SHA256 export manifests, record clean CI validation, document external component licensing and scope.
6. Tag `artifact-v1.0` only after validation; deposit the exact release on Zenodo and then cite the DOI in the paper.

No new paid model calls needed or authorized.
