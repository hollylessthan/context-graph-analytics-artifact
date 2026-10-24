# Claims-to-evidence map

All checks run offline on the committed exported evidence. Python line numbers below are approximate and should be updated after the final code freeze.

| Paper claim | Source record | Verification |
|---|---|---|
| Table I four task rows and 30/36 vs 25/36 | `evidence/primary-results.json` E2_task_pass | `scripts/check_additional_claims.py`; `scripts/check_export.py` |
| 3,696 identity checks with zero violations | `evidence/invariance-gate-phase-a.json` graph/task perturbations | `scripts/check_additional_claims.py` |
| Order sensitivity 22/13 and 12/15 | `evidence/offline-analysis.json` summary at 8000 cap | `scripts/check_additional_claims.py` |
| ID permutation ranges 14–27 and 14–22 | `evidence/review-followups.json` permutation_summary | `scripts/check_additional_claims.py` |
| Table II all 16 factorial cells, 576 contexts | `evidence/stage-local-evidence.zip`: factorial.json.gz | `scripts/reproduce_stage.py` |
| Stage impacts 48/218/171 and packing 44/72 | `evidence/stage-local-evidence.zip`: pairs and factorial | `scripts/reproduce_stage.py` |
| 84 strict gaps; 36 join, 8 other, 37 absent, 3 relationships | `evidence/stage-local-evidence.zip`: support.json.gz | `scripts/check_additional_claims.py` |
| 50/55 passing trials with edge-complete context | `evidence/stage-local-evidence.zip`: support.json.gz | `scripts/check_additional_claims.py` |
| Table III each support stratum | `evidence/context-graph-paired-evidence-curated.zip`: plan.json and scored-results.json | `scripts/reproduce_paired.py` |
| P3 five two-error lists and separate P2 COLUMNS validation | same scored-results.json | `scripts/reproduce_paired.py` |
| 41 feasible packing witnesses and 40 original-order relevance overrides | `evidence/stage-local-evidence.zip`: pairs.json.gz | `scripts/reproduce_stage.py` |
| Table III totals: 264 calls, 132 pairs; 92/34/6/0 outcomes | `evidence/context-graph-paired-evidence-curated.zip`: scored-results.json and paired-summary.json | `scripts/reproduce_paired.py` |
| Three discordant cases | `evidence/context-graph-paired-evidence-curated.zip`: scored-results.json | `scripts/reproduce_paired.py` |
| Two external probes: 0/72 ID changes; LightRAG 72/72 shuffle | `evidence/external-selection-summary.json` | `scripts/check_additional_claims.py` |

The scripts now check the listed paper-level aggregates from frozen records. This is retrospective record-based verification, not rerunning the original inference or SQL execution.
