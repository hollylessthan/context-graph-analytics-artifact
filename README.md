# Context-Graph Analytics: Reproduction Artifact

**Staged export, not yet a completed reproducibility release.** Companion to *Evaluating Context-Graph Construction for Analytical Agents: Hidden Confounders and Lessons from a Controlled Benchmark* by Fangyu Lo (Independent Researcher).

Original code and studies: https://github.com/hollylessthan/context-graph-analytics-study

## Offline summary validation
Run `python scripts/check_export.py` with Python 3.11+. No API keys or paid calls needed. GitHub Actions also checks these summaries.

Current checks verify frozen original totals 30/36 versus 25/36, eight factorial combinations for both methods, 44 packing-selected evidence-set changes, and paired/external audit summary provenance. **They do not reproduce the original experiment from raw traces.**

The 264-call paired run was curated from [workflow artifact 12571928596](https://github.com/hollylessthan/context-graph-analytics-study/actions/runs/40120563599/artifacts/12571928596). The scored outputs, SQL, contexts, plans and provider event ledger are now included in `evidence/context-graph-paired-evidence-curated.zip`; opaque provider-response payloads are intentionally excluded.

Read [EXPORT_SCOPE.md](EXPORT_SCOPE.md) before approving a versioned release or Zenodo deposition.

## Raw paired evidence and reproduction

A curated, SHA-256-manifested export of the 264-call paired run is committed as `evidence/context-graph-paired-evidence-curated.zip`. The original archive contains opaque provider-response payloads; those are intentionally omitted from the curated evidence ZIP, while preserving the scored SQL, model-output-based contract decisions, contexts, plan, provider ledger, and summary.

Run `python scripts/reproduce_paired.py evidence/context-graph-paired-evidence-curated.zip` to recompute the 132 paired pass/fail outcomes from individual saved scores, rather than trusting the summary alone. The committed ZIP has been checked against its source export by Git blob identity and file-level SHA-256 digests. It does not regenerate model calls.

## Stage-local factorial evidence

The four compressed originals (`catalogs.json.gz`, `factorial.json.gz`, `pairs.json.gz`, `support.json.gz`) have been independently SHA-256 checked against the frozen summary. The repository's `scripts/reproduce_stage.py` recomputes all 16 factorial cells, 44/72 packing-only changed contexts, and 48/218/171 changed selections by stage from record-level traces. Once `evidence/stage-local-evidence.zip` is committed, CI automatically runs this check. Until then, the script can be run locally with a ZIP containing `stage-local/<filename>.json.gz`.
