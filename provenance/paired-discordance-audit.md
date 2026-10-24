# Artifact-level audit: frozen paired planner run 40120563599

**Scope:** audit of the six paired numerical correctness transitions from original (000) pass to selection-counterfactual (001) fail. No new model calls, changed model prompts, benchmark edits, or post-hoc experiments.

## Source and integrity
- Frozen run: https://github.com/hollylessthan/context-graph-analytics-study/actions/runs/40120563599/job/120950986817
- [Preserved artifact](https://github.com/hollylessthan/context-graph-analytics-study/actions/runs/40120563599/artifacts/12571928596), artifact 12571928596.
- Read `paired-results/{scored-results.json,responses.jsonl,provider-trace.jsonl,contexts.json,collection-summary.json,paired-summary.json}`.
- Exactly **264 scored operations**, **264 responses**, **264 unique operation IDs**, and **264 reserved_before_send + 264 provider_response events**. All responses identify `gpt-6.1-sol`; the collector reports complete.
- Only **88 unique request hashes** because each of the 88 arm/context combinations is reused across three fresh repetitions; this is expected, not an indication of reused responses. Do not write "264 unique request hashes."
- Collector ledger: 264 calls, 726,738 input tokens, 147,620 output tokens, **USD 3.62234950**.
- Paired correctness transitions (000,001): 92 both pass; 34 both fail; six 000-only pass; zero 001-only pass. Original 98/132 vs changed 92/132, difference -4.55 percentage points. Repetitions within the same graph/task are dependent.

## Audit of all six discordant paired repetitions
| Case | Repetition | Counterfactual failure stage | SQL evidence |
| --- | --- | --- | --- |
| canonical / schema_llm / graph 1 / P3 | 1 | numerical_scoring: numerical_mismatch | 000 checks `order_status <> 'delivered'`; 001 checks only `delivered_at IS NULL` for delivered eligibility |
| canonical / schema_llm / graph 1 / P3 | 2 | numerical_scoring: numerical_mismatch | Same loss of `order_status` eligibility test |
| canonical / schema_llm / graph 1 / P3 | 3 | numerical_scoring: numerical_mismatch | Same loss of `order_status` eligibility test |
| canonical / schema_llm / graph 2 / P3 | 2 | numerical_scoring: numerical_mismatch | Same loss of `order_status` eligibility test |
| canonical / schema_llm / graph 2 / P3 | 3 | numerical_scoring: numerical_mismatch | Same loss of `order_status` eligibility test |
| canonical / simple_llm / graph 1 / P2 | 3 | sql_validation: Function not allowed: COLUMNS | 001 calls `COLUMNS('^review_.*id$')` as an identifier; blocked by frozen SQL validator |

- All five P3 altered queries are **valid and executable**, but fail numerical scoring; original queries explicitly test `order_status` to classify non-delivered orders. Altered queries use the existence/non-nullness of `order_delivered_customer_date` instead of the status. These are not equivalent business rules.
- In **both P3 affected graph contexts**, the original records include `olist_orders_dataset.csv HAS_COLUMN olist_orders_dataset.csv.order_status`, while the altered records omit it. Altered contexts also replace other records, so the effect cannot be attributed *exclusively* to that one fact.
- The P2 altered query is a distinct **SQL-validation** failure, not an observed numerical mismatch after execution. The original and altered contexts also differ in several facts. Do not combine P2 with five executable semantic failures in the narrative.
- Same-case controls: graph 1 P3 transitions in all three repetitions; graph 2 P3 transitions twice, while repetition 1 fails for both arms (000 SQL validation, 001 numerical mismatch); P2 transitions once, while the first two repetitions pass in both arms.
- No evidence of provider error or missing response in the inspected collector ledger and scoring artifact.

## Independent validation (provider-free)

`scripts/validate_paired_discordance.py` writes `evaluation/followup/paired-discordance-validation.json`. It recomputes contexts from the frozen plan, P3 unit reasons from the raw Olist CSVs, and (with `--artifact-dir`) prints the frozen evaluator's error lists. No model or SQL-runtime calls.

**1. Context side: in the P3 cases `order_status` is not merely one omitted fact; it is invisible.**

| Case | Stratum | 000 edge-missing | 001 edge-missing | `order_status` anywhere in 000 / 001 |
|---|---|---|---|---|
| schema_llm g1 P3 | edge_lost | none | `orders.order_status` | yes / **no** |
| schema_llm g2 P3 | edge_lost | none | `orders.order_status` | yes / **no** |
| simple_llm g1 P2 | edge_missing_set_changed | `review_id`, English category | `review_id` | yes / yes |

In both P3 counterfactual contexts, `orders.order_status` is the *only* required item lost under edge credit, and no record mentions the identifier at all. The planner contract forbids inferring absent physical identifiers. A delivery-timestamp proxy is therefore the expected behavior of a contract-following planner, not an arbitrary error. Other records also differ (10–12 per arm), so this is still not a single-fact intervention.

**2. Data side: the proxy changes exactly one unit's exclusion reason and no metric value.** Recomputing P3 reasons on the raw data, the contract rule (`order_status = 'delivered'`) reproduces the frozen reference exclusions exactly in both periods. Under the proxy rule (non-null `order_delivered_customer_date`):

| Period | Included units (contract / proxy) | Reasons that differ |
|---|---|---|
| 2017-11 | 7,288 / 7,288, identical sets | 1 order (`2d1e2d5b…`, status `delivered`, missing customer delivery date): `missing_lifecycle_timestamp` → `not_eligible_delivered` |
| 2018-04 | 6,798 / 6,798, identical sets | none |

Because the included sets are identical, every reported value is unchanged by the proxy itself: period means, stage legs, negative-leg counts, delta, within/mix and segment contributions. The only evaluator check it fails is the 2017-11 exclusion-by-reason count (255 vs 256 and 1 vs 0). **Prediction:** if the five altered P3 queries differ from correct SQL only in the eligibility rule, each failure's error list contains only `exclusions.2017-11.not_eligible_delivered` and `exclusions.2017-11.missing_lifecycle_timestamp`. If other errors appear, the altered SQL also differs elsewhere.

**Confirmed against the preserved artifact** ([error check](../evaluation/followup/paired-discordance-artifact-error-check.md)): each of the five P3 001 operations fails with exactly these two errors and no others, and every paired 000 arm passes:

```text
exclusions.2017-11.not_eligible_delivered: count_mismatch
exclusions.2017-11.missing_lifecycle_timestamp: count_mismatch
```

Every other checked output (period n and means, stage legs, negative-leg counts, delta, within/mix, segments, top-5 ranking) matches the reference within tolerance. This confirms the evaluator-level prediction; it does not prove the full SQL texts are equivalent outside the eligibility predicate.

To confirm from the artifact:

```bash
python scripts/validate_paired_discordance.py --artifact-dir <paired-results> \
  --output evaluation/followup/paired-discordance-validation.json
```

**3. P2: same missing identifier in both arms; most consistent with stochastic workaround behavior.** `review_id` is missing under edge credit in *both* arms. The altered arm additionally regains the English-category column, so it has better support, not worse. The failing 001 repetition tried to guess the review-ID column with `COLUMNS('^review_.*id$')`, which the frozen allowlist rejects. Repetitions 1–2 pass in both arms. This case does not support an evidence-loss explanation and should be reported separately as a contract-workaround failure.

**What this changes in the wording.** The defensible answer-level claim is narrower than "selected evidence changed the analytical answer". It is: removing the only visible `order_status` identifier led the planner, in 5 of 6 repetitions across two graphs, to substitute a timestamp proxy. On this data the proxy misclassifies one excluded order in one period, and the strict unit-level contract fails, while every reported metric value is unaffected (confirmed from the artifact's evaluator error lists). This is a real contract-level consequence, and also a concrete example of how a strict unit-row evaluator converts an almost-equivalent rule into a binary failure. Both readings belong in the paper.

## Interpretation: strongest warranted claim
Under a frozen, paired, standardized-presentation planner experiment, a selected evidence change **coincided** with five executable SQL answers replacing a required order-status eligibility rule with a delivery-timestamp proxy and failing numerical scoring. The original contexts exposed `order_status`; the altered contexts omitted that fact. This is a **plausible evidence-visibility pathway**, not a clean single-fact causal intervention.

The remaining discordance involved an unsupported SQL construct. Results cluster in **three of 44 graph/task cases**; the six paired differences are not six independent problem examples. External component probes in PR #61 did not reproduce the ID-packing mechanism. General method/framework prevalence and superiority are unproven.

## Limitations and follow-up adjudication
- [x] Reconcile operation counts, provider response completeness, model name, collector ledger, stages and paired summary.
- [x] Inspect SQL eligibility condition for all five executable discordances; identify distinct P2 validation error.
- [x] Inspect visible graph records to check `order_status` fact present in 000 and missing in 001.
- [x] Inspect same-case repetition controls, including 000 graph 2 P3 repetition 1 failing for another reason.
- [x] Independent data-level check of the P3 eligibility rule: the contract rule reproduces the reference exclusions exactly; the proxy changes one 2017-11 exclusion reason and no included unit or metric value (see Independent validation).
- [x] Confirmed from the preserved `scored-results.json`: the five P3 error lists contain only the two 2017-11 exclusion-reason counts ([error check](../evaluation/followup/paired-discordance-artifact-error-check.md)).
- [ ] Optional: run the combined validator with `--artifact-dir` in CI or a checkout, so one committed JSON covers context, data and artifact checks together.
- [ ] Confirm exact source-code/prompt hashes and complete per-request invariants using frozen manifests; this reading checked counts and stages, not an independent cryptographic reconstruction of every payload.
- [ ] Ask a skeptical reviewer whether narrowed implementation-specific case-study novelty justifies workshop submission. No additional paid calls or case selection without a prespecified rationale.

**Decision:** Retain the narrower implementation-specific case-study/report path provisionally. Do not assert established graph-method superiority, universal evidence-deletion causality, or full independent ground-truth verification.
