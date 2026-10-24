# Frozen paired planner run 40120563599 — preliminary evidence review

**Status:** completed, scoring reproduced in workflow logs; artifact-level manual failure adjudication **pending**. This is a descriptive, implementation-specific case study, not a general graph-retrieval performance claim.

## Provenance
- Workflow: https://github.com/hollylessthan/context-graph-analytics-study/actions/runs/40120563599/job/120950986817
- Head: `a27b4a148fb1baec77922fcd757203f9a4ecda4` (`main`)
- Artifact: [paired-packing-40120563599-1](https://github.com/hollylessthan/context-graph-analytics-study/actions/runs/40120563599/artifacts/12571928596), artifact ID 12571928596, ZIP SHA-256 `09881cf265b6b9c5e3da28f170d3d08d0f4acfaf709e395c283097596a85cf43`.
- All workflow steps succeeded; 264/264 planned calls, 132/132 paired comparisons.
- Original (000) and altered-selection (001) are both fresh calls; 3 repetitions per 44 cases; common presentation-order policy. This does **not** isolate order effects perfectly.

## Preregistered outcome: executable numerical correctness
| Outcome (000,001) | Paired repetitions |
| --- | ---: |
| Pass, pass (11) | 92 |
| Fail, fail (00) | 34 |
| Pass, fail (10) | 6 |
| Fail, pass (01) | 0 |
| **Total** | **132** |

- Original: 98/132 correct (74.24%); altered: 92/132 (69.70%); descriptive difference altered minus original = **-4.55 percentage points**.
- Differences concentrated in three of 44 selected cases: `canonical|schema_llm|1|P3` (3/3 pass→fail), `canonical|schema_llm|2|P3` (2/3), `canonical|simple_llm|1|P2` (1/3). The other 41 cases had no change in binary numerical correctness across repetitions.
- Strata: edge lost (4 cases / 12 pairs) original 11/12 vs altered 6/12; edge gained (1 / 3) 3/3 both; edge missing set changed (7 / 21) original 3/21 vs altered 2/21; no edge support change (32 / 96) 81/96 in both arms.
- Per-task: P1 18/18 both, P2 9/39 vs 8/39, P3 29/33 vs 24/33, P4 42/42 both.
- These repeated responses are dependent within case; do **not** run an IID test on 132 paired repetitions, or report a population effect from three changed cases.

## Interpretation / decision
The frozen prospective experiment establishes that in this implementation, selected evidence can alter the planner's numerical outcomes under standardized presentation. The effect is concentrated, not broadly replicated across all tasks or methods. The source-pinned external component probes in PR #61 did **not** independently reproduce the implementation's label-to-ID packing mechanism, so do not claim that GraphRAG, LightRAG, or graph construction methods generally suffer from this effect.

**Recommendation:** continue a **narrow technical case-study/report manuscript**, conditional on manual adjudication of the six discordant paired observations, transport completeness, SQL semantics, evaluator correctness, and matched-input checks. Do not spend on more calls, expand corpus, or promise broad paper novelty. A workshop submission depends on a skeptical read of the full report and concrete venue fit, not merely on a favorable aggregate count.

## Required artifact-level skeptical review before manuscript lock
- [ ] Verify 264 unique planned operation fingerprints and 264 preserved response/transport entries; confirm no substitution, retries, or missing/truncated outputs.
- [ ] Reconcile artifact manifest, input/code hashes, actual token usage/cost, and the 132 comparison scores against the logged summary.
- [ ] For **all six discordant pairs**, inspect original/altered selected facts, required join/column availability, SQL text, execution/error classification, numeric gold, and whether a different correct query exists.
- [ ] Include same-case concordant repetitions as controls; inspect the 3/3, 2/3, 1/3 pattern rather than implying six independent examples.
- [ ] Check whether the 001 failures are caused by removal of genuinely required evidence, ordering/prompt effects, stochastic model variation, or evaluator/SQL ambiguities. If unresolved, downgrade the causal wording.
- [ ] Preserve the negative external probes, incomplete notebook-coverage checks, method comparison confounds, and known limitations in the paper.
- [ ] Reconcile final reviewer decision: case study vs reproducible technical report; select venue only after this audit.

**Research question remains fixed:** when and why graph construction/selection methods affect evidence available to an analytical planner, and the cost and correctness consequences. This follow-up diagnoses a confound in our saved comparison; it does not silently replace the original question with a generic prompt-order study.
