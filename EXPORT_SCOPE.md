# Export and release gates

This PR includes frozen summary records, paired scored outcomes, SQL, contexts and human-readable provenance. Paired outcome counts are reproducible offline; the full original/factorial benchmark is not yet independently reproducible.

## Required before release
1. CI now fetches and hash-checks the four pinned stage-local compressed files into an artifact ZIP. The resulting ZIP must be inspected and added to the release package. Export original stage-local compressed context evidence: `evaluation/followup/label-stage-audit/{catalogs,factorial,pairs,support}.json.gz`; verify source hashes.
2. **Completed for scored outcomes:** The curated paired evidence ZIP from research Actions run 40120563599 is committed and integrity-checked. It contains scored-results, contexts, provider trace, plan and paired summaries. Opaque model-response payloads were excluded. Raw text-level response replication is outside this sanitized export's scope.
3. Import minimal deterministic retrieval, analysis, and scoring code with pinned dependencies and licenses.
4. Regenerate all paper tables from raw saved evidence in one offline command, not from manually copied expected counts.
5. Generate source commit and SHA256 export manifests, record clean CI validation, document external component licensing and scope.
6. Tag `artifact-v1.0` only after validation; deposit the exact release on Zenodo and then cite the DOI in the paper.

No new paid model calls needed or authorized.
