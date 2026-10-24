# Context-Graph Analytics: Reproduction Artifact

**Validated evidence export, pending release review and archival.** Companion to *Evaluating Context-Graph Construction for Analytical Agents: Hidden Confounders and Lessons from a Controlled Benchmark* by Fangyu Lo (Independent Researcher).

Original code and studies: https://github.com/hollylessthan/context-graph-analytics-study

## Offline summary validation
Run the following commands with Python 3.11+. No API keys or paid calls needed:

```bash
python scripts/check_export.py
python scripts/reproduce_stage.py evidence/stage-local-evidence.zip
python scripts/reproduce_paired.py evidence/context-graph-paired-evidence-curated.zip
```

 GitHub Actions also checks these summaries.

Current checks verify frozen original totals 30/36 versus 25/36, eight factorial combinations for both methods, 44 packing-selected evidence-set changes, and paired/external audit summary provenance. **The companion stage and paired checks re-aggregate individual frozen trace records, but no check re-runs the LLM or original SQL evaluator.**

The 264-call paired run was curated from [an expiring workflow artifact 12571928596](https://github.com/hollylessthan/context-graph-analytics-study/actions/runs/40120563599/artifacts/12571928596). The scored outputs, SQL, contexts, plans and provider event ledger are now included in `evidence/context-graph-paired-evidence-curated.zip`; opaque provider-response payloads are intentionally excluded.

The frozen evidence was published as [artifact-v1.0](https://github.com/hollylessthan/context-graph-analytics-artifact/releases/tag/artifact-v1.0) and archived as [10.5281/zenodo.23628013](https://doi.org/10.5281/zenodo.23628013). This post-release documentation update is not part of the immutable v1.0 archive. See [EXPORT_SCOPE.md](EXPORT_SCOPE.md) for reproduction limits.

## Raw paired evidence and reproduction

A curated, SHA-256-manifested export of the 264-call paired run is committed as `evidence/context-graph-paired-evidence-curated.zip`. The original archive contains model response text and response identifiers; those are intentionally omitted to keep the public release minimal and avoid unneeded response metadata exposure. The tradeoff is that reviewers cannot independently re-extract SQL from raw responses. These files are not required to recompute scored outcomes. The curated evidence preserves scored SQL, contract decisions, contexts, plan, provider ledger, and summary.

Run `python scripts/reproduce_paired.py evidence/context-graph-paired-evidence-curated.zip` to recompute the 132 paired pass/fail outcomes from individual saved scores, rather than trusting the summary alone. The committed ZIP has been checked against its source export by Git blob identity and file-level SHA-256 digests. It does not regenerate model calls.

## Stage-local factorial evidence

The four compressed originals (`catalogs.json.gz`, `factorial.json.gz`, `pairs.json.gz`, `support.json.gz`) have been independently SHA-256 checked against the frozen summary. The repository's `scripts/reproduce_stage.py` recomputes all 16 factorial cells, 44/72 packing-only changed contexts, and 48/218/171 changed selections by stage from record-level traces. The ZIP is now committed and its trace-level verification passed in [CI run 40136118512](https://github.com/hollylessthan/context-graph-analytics-artifact/actions/runs/40136118512).

## Offline checks included in the release

```bash
python scripts/check_export.py
python scripts/check_additional_claims.py
python scripts/reproduce_stage.py evidence/stage-local-evidence.zip
python scripts/reproduce_paired.py evidence/context-graph-paired-evidence-curated.zip
```

These checks re-aggregate frozen records only. The original research repository may not be publicly accessible; the archived ZIPs are self-contained for the reported checks.
