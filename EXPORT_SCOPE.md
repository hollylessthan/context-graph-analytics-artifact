# Export and release gates

This PR contains only frozen **summary records** and human-readable provenance. It does not yet make the paper independently reproducible.

## Required before release
1. Export original stage-local compressed context evidence: `evaluation/followup/label-stage-audit/{catalogs,factorial,pairs,support}.json.gz`; verify source hashes.
2. Extract the original 264-call paired archive from research Actions run 40120563599, artifact ID 12571928596. Retain `scored-results.json`, `responses.jsonl`, `provider-trace.jsonl`, `contexts.json`, `collection-summary.json`, and `paired-summary.json`. Review for sensitive information.
3. Import minimal deterministic retrieval, analysis, and scoring code with pinned dependencies and licenses.
4. Regenerate all paper tables from raw saved evidence in one offline command, not from manually copied expected counts.
5. Generate source commit and SHA256 export manifests, record clean CI validation, document external component licensing and scope.
6. Tag `artifact-v1.0` only after validation; deposit the exact release on Zenodo and then cite the DOI in the paper.

No new paid model calls needed or authorized.
