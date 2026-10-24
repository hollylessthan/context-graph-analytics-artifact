# Label-to-ID stage audit: effects beyond lexical score ties

## Decision

The bounded analysis found a specific mechanism beyond ordinary equal-relevance
tie-breaking: the frozen final packing stage sorts by fact ID within priority
groups, including facts with unequal BM25 scores. Construction-method labels
enter those IDs. Holding seeds and graph lookups fixed, a label-derived packing
key alone changes which visible facts fit the context.

This strengthens the diagnosis of **this implementation's comparison confound**.
It does not establish a new general retrieval phenomenon, its prevalence in
other implementations, a superior constructor, or any changed SQL accuracy.
The next useful novelty gate is a separately bounded external-implementation
replication. Additional resampling of the original clean catalog is not justified
by this result. Corpus expansion and paid calls remain paused.

## Scope, freeze and reconciliation

The [analysis plan](existing-artifact-analysis-plan.md) was committed in PR #58.
The [support/intervention rubric](existing-artifact-support-rubric.md) and input
hashes were committed at `a1360dc6c1de4d04f0224135f7b0ffd4ba40ddb6` before the
new analysis. This is exploratory and unblinded after the primary, F1 and F2
results, not independent confirmatory preregistration.

We used all 18 saved LLM graphs, all four tasks and all three variants: 72
original contexts, eight interventions per context, 576 factorial contexts.
The cap stayed at 8,000 characters. The three switches independently change
lexical tie ordering, limited lookup ordering and final packing ordering to
keys obtained by swapping the method label and rehashing the original raw fact.
Occurrence identities, analytical content, priority rules and limits are fixed.

All gates passed before outputs were written:

- Original-label hashing reproduces every raw fact ID.
- All 72 instrumented original contexts match the saved contexts and the frozen
  retriever, including ordered records, sizes, call counts and attachment stats.
- All 72 all-swapped endpoints match an independent call to the frozen retriever
  on relabelled/rehash facts and the earlier review-follow-up measurements.
- Held-ID relabelling and input shuffling leave all 72 contexts unchanged.
- All 72 full per-occurrence BM25 score arrays are unchanged by label rehashing.

The final check matters because the frozen lexical index serializes IDs into
its corpus as well as using them as sorting keys. In these actual inputs, that
does not change scores. All lookup candidates, including zero-score candidates,
receive comparable scores from the same full attached-fact lexical corpus.
No replacement policy was introduced into the retriever.

## A. All eight interventions

Bits are ordered **lexical / lookup / packing**. A 1 uses the swapped-label key
at that site; 0 uses the original key. Every cell below has 36 graph/task
contexts. These are retrieval-completeness counts, not planner accuracies.

| Mask | Simple strict | Schema strict | Simple edge-credit | Schema edge-credit |
|---|---:|---:|---:|---:|
| 000: original | 19 | 18 | 26 | 28 |
| 001: packing only | 15 | 17 | 27 | 24 |
| 010: lookup only | 21 | 18 | 29 | 28 |
| 011: lookup and packing | 16 | 17 | 29 | 24 |
| 100: lexical ties only | 19 | 17 | 26 | 28 |
| 101: lexical ties and packing | 15 | 17 | 28 | 24 |
| 110: lexical ties and lookup | 21 | 17 | 28 | 28 |
| 111: all swapped | 16 | 17 | 29 | 24 |

Packing alone reverses the original strict completeness ordering. Under the
existing edge-credit definition, the original ordering points the other way,
and packing alone reverses that ordering too. Thus the issue is not eliminated
by crediting join endpoints. It also does not identify which method should win:
the outcome depends on the selector and the operational coverage definition.

For each stage there are 288 paired switch contrasts: 72 original graph/task
contexts times four settings of the other two switches. They are repeated
interventions on the same cases, not 288 independent tasks.

| Switched stage | Distinct visible fact set changes | Strict completeness changes | Edge-credit completeness changes |
|---|---:|---:|---:|
| Lexical equal-score ordering | 48/288 | 2/288 | 2/288 |
| ID-ordered limited lookups | 218/288 | 18/288 | 10/288 |
| Final packing order | 171/288 | 40/288 | 22/288 |

Effects interact because an upstream choice changes entities and candidate
pools downstream. These counts are not additive shares of causation. Exact
occurrence sets, visible-record sets, multisets and context hashes are measured
separately in the traces. Packing changes the context hash in all 288 paired
contrasts, but changes the distinct visible set in only 171; hash turnover is
not itself evidence loss.

### A concrete unequal-score packing effect

With the original lexical seeds and lookup results fixed (000 versus 001),
packing changes distinct visible sets in 44/72 contexts. In **41/72** there is
a same-priority unequal-score exchange for which replacing the selected lower-
scored fact by the excluded higher-scored fact still fits the 8k cap. The
original arm selects the lower-scored fact in **40/72** contexts (17 Simple,
23 Schema); the swapped arm does so in 39/72 (15 Simple, 24 Schema). These sets
overlap; neither ordering repairs the problem generally.

Across all four upstream settings, 164/288 packing contrasts have such a
feasible exchange. Infeasible replacements are counted separately in the trace;
the analysis does not confuse a larger record failing to fit with an available
same-budget opportunity.

Example: canonical SchemaLLM realization 1, P1. The original context includes
fact 44, a table row-count profile with BM25 score 0.0, while omitting fact 7,
the customers.customer_id membership record, with score 2.7916851292401046.
Both are non-seed, non-DECLARED_JOIN candidates in the same priority group.
Exchanging the profile for the membership record would produce a 7,902-character
context. Their ordering was determined by ID rather than that relevance gap.
The column is already named by a join in this particular context, so this
example illustrates selection and measurement, not a demonstrated SQL failure.

BM25 is not an oracle for analytical usefulness. The defensible finding is that
the label-dependent ID can override unequal lexical relevance within a group,
not that every higher-scored replacement would improve an answer.

## B. Support audit across every original context

All 846 required-item instances were enumerated. There are 84 strictly missing
instances: 81 columns and three relationships, across 35 contexts. All missing
items and their exact witnesses were reviewed under the frozen rubric, including
failures. No coding changes or manual semantic gold edits were made. The
unblinded review checklist is in `review.json` alongside the machine outputs.

Of the 81 missing column instances:

- 36 are endpoints of relationships accepted by the existing secondary scorer.
- Eight more have a visible identifier through profiles and/or internal
  translation mappings, with semantic scope left unresolved.
- 37 have no accepted normalized identifier witness in the selected context.

Categories can overlap at witness level. The three missing relationships do
not become credited merely because endpoint names are visible. The separate
HAS_COLUMN requirement is a legitimate structural annotation definition; it
must not be interpreted as a test of whether the physical name appears anywhere.

| Saved outcome | Contexts | Strict complete | Edge-credit complete | Identifier-availability upper complete |
|---|---:|---:|---:|---:|
| Numerical-contract pass | 55 | 37 | 50 | 50 |
| Refusal expressed in SQL | 12 | 0 | 0 | 0 |
| Table-name rejection | 4 | 0 | 4 | 4 |
| Wrong numerical answer | 1 | 0 | 0 | 0 |

The availability upper bound additionally credits visible profile/internal-
mapping/other column identifiers; it does not credit unasserted relationships.
It adds individual column visibility but no further fully complete contexts.
It is not a bound on analytical correctness or sufficient semantic support.

This reconciles the previously observed 18 passes with strict evidence gaps:
13 have every missing item available through accepted join endpoints; five
P2 Simple cases still lack review_id. The latter remain passes of the saved
numerical contracts, with semantic equivalence and necessity unproven.

All four table-name rejections have complete edge-credit coverage. Their saved
runtime rejection is distinct from identifier absence; increasing evidence
coverage does not itself repair unsupported table names. All 12 refusal contexts
and the single wrong-answer context retain gaps even under the availability
upper bound. That is a descriptive association, not proof that those gaps caused
the observed answers or that every listed item was necessary.

## What this changes for novelty

The result is more specific than “IDs break score ties”: treatment labels affect
ID-ordered access limits and relevance-overriding packing in this pipeline.
The effect persists under both frozen membership and existing edge-credit
completeness definitions. The support audit also prevents runtime rejections and
missing annotation forms from being described as one undifferentiated retrieval
failure. These are useful diagnostic findings.

However, this may still be a documented implementation defect plus known
evaluation limitations. The literature overlap in
[the novelty review](methodological-novelty-review.md) remains. No external
implementation has been tested, and no SQL was generated on any new context.
The original Simple 30/36 and Schema 25/36 numerical-pass totals are unchanged.
Do not claim a label-induced SQL-accuracy reversal or a general construction-
quality winner from the completeness reversals above.

Before calling this a broader methodological contribution, freeze a separate
external-replication design: select implementations before inspecting outcomes,
pin their versions, use their native ordering/packing behavior, hold analytical
content and queries fixed, and separate equal-score ties from unequal-score
selection and deliberate semantic priorities. A transplanted copy of our
selector is not an independent replication. If only ordinary tie effects recur,
retain that negative result and favor a transparent technical report. No external
experiment or paid pilot is authorized automatically by this audit.

## Artifacts and reproduction

`evaluation/followup/label-stage-audit/summary.json` contains input/output hashes,
all controls, all arm counts and outcome cross-tabs. The deterministic gzip
JSON files preserve complete traces without duplicating long fact text:

- `catalogs.json.gz`: graph-local fact indices, original/swapped IDs, compact
  records, source/chunk provenance, entity-name indices and all BM25 scores.
- `factorial.json.gz`: all 576 contexts, lexical ranks/seeds, every pre/post-limit
  lookup, frontiers, priority groups, packing decisions, sizes and missing items.
- `pairs.json.gz`: all 864 paired stage contrasts and scored packing witnesses.
- `support.json.gz`: all 72 original contexts and all 846 required-item instances
  with witness references and conservative adjudication.
- `review.json`: the manual missing-item review, bound to the support-file hash.

Indices in traces reference the corresponding graph's catalog; they are stable
occurrence identities, not new ranking keys. Exact witness field text is in the
referenced compact record. Catalogs are diagnostic extracts, not a substitute
for durably archiving the full raw artifacts needed to reproduce BM25 inputs.

```bash
python scripts/analyze_label_stage_audit.py \
  --phase-a-dir <A> --phase-b-dir <B> --variant-root <packages> \
  --output-dir evaluation/followup/label-stage-audit
python -m unittest discover -s tests -p 'test_label_stage_audit.py' -v
python -m unittest discover -s tests -p 'test_primary_retrieval_fairness.py' -v
```

Read a compressed trace with Python's standard library:

```python
import gzip, json
with gzip.open('evaluation/followup/label-stage-audit/factorial.json.gz', 'rt') as stream:
    contexts = json.load(stream)
assert len(contexts) == 576
```

Validation: 12 new audit tests and 12 existing retrieval-fairness tests pass.
All actual-artifact reconciliation gates pass. Full outputs reproduce
byte-for-byte under a second Python hash seed. Frozen primary/F1/F2 algorithms,
source packages and results are unchanged. No provider, embedding, planner,
judge or SQL-execution calls were made.
