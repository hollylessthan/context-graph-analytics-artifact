# External component probes: stronger mechanism not independently reproduced

## Decision

The fixed two-implementation check does **not** establish broader novelty for
our label-to-ID packing defect. LightRAG's tested final-selection component is
invariant to the two ID interventions on all 72 saved cases while its reference
budget is active. GraphRAG's tested source branch is also ID-invariant, but its
budget does not bind on these inputs, making that result inconclusive about
packing under pressure.

These are source-pinned **component probes with controlled reference costs**,
not full framework replications or native-tokenizer experiments. They provide
no positive external reproduction of the stronger mechanism. Do not generalize
the PR #60 finding to GraphRAG systems generally, and do not expand the sample
to find a favorable implementation after seeing this result.

Claude's review is addressed in [the review response](pr60-review-response.md).
A later paid, paired planner study could measure impact within our own pipeline;
it would not by itself demonstrate that the mechanism is new or widespread.
No such run was started or enabled here.

## Prospective scope and source selection

The [two-repository protocol](external-selection-validation-plan.md) and review
response were committed at `5aa8807d61d75c4e1998fdd0be111ad2db5af0d6` before
inspecting the selected query code. After that inspection, the exact selected
functions, whole-source digests and adapters were frozen at
`f7af4f54c50d0e0125f155d8390334fd9821cd88` before runtime probes.

The fixed source commits are:

- [Microsoft GraphRAG, c600ff8](https://github.com/microsoft/graphrag/tree/c600ff80b77b9b62c47d539a3ac9569e95d8949b).
- [HKUDS LightRAG, aaebfe1](https://github.com/HKUDS/LightRAG/tree/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a).

All nine cached source/license files match their pinned Git blob identities.
The inspected local/hybrid context paths do not show our incidental-ID sorting
mechanism at their inspected selection boundaries. This is not an exhaustive
audit of either repository, backend or version history. Upstream embedding
search and vector-store tie resolution are outside the executed scope.

Under the frozen selection rule, we therefore tested the final eligible source
selectors as negative controls rather than replacing either implementation.
The source register is `config/external-selection-source-manifest.json`.

## Native functions actually executed

For GraphRAG, the unmodified
[`LocalSearchMixedContext._build_text_unit_context`](https://github.com/microsoft/graphrag/blob/c600ff80b77b9b62c47d539a3ac9569e95d8949b/packages/graphrag/graphrag/query/structured_search/local_search/mixed_context.py)
orders source units by selected-entity position and relationship count, then
calls native
[`build_text_unit_context` and `count_relationships`](https://github.com/microsoft/graphrag/blob/c600ff80b77b9b62c47d539a3ac9569e95d8949b/packages/graphrag/graphrag/query/context_builder/source_context.py).
The local-search call sets `shuffle_data=False`. Incidental text-unit and
relationship IDs are used as consistently rewired references; stable short
display IDs are used for rendering. Neither identifier intervention changes
the native semantic priorities or input order.

For LightRAG, native
[`process_chunks_unified`](https://github.com/HKUDS/LightRAG/blob/aaebfe1bb8d55deb6a4304d357a3bf4c92fcd40a/lightrag/utils.py)
calls its reference-aware `_truncate_chunks_for_unified_context`, native
whole-item prefix limiter and native reference/rendering functions. The chosen
supported configuration disables reranking and the separate top-k limit, so
the final reference budget is the tested bound. Chunk IDs remain metadata;
rendered references depend on fixed file paths and content. Native output
display IDs are assigned by position.

Definitions are loaded directly from verified source ASTs. Function bodies and
signatures are not rewritten. Dependency isolation supplies installed pandas,
standard-library helpers, duck-typed data carriers and an inline async executor
for the native tokenizer work. No full framework package, model, remote storage
or application is initialized. This does not validate the frameworks' complete
dependency environments or concurrency behavior.

## Data, costs and controls

All 18 saved graphs and all four fixed task queries are used: 72 cases per
component. Each compact saved fact is projected to one source/text chunk. This
is not graph construction performed by either external framework. The frozen
BM25 values determine a fixed input order; occurrence ordinal breaks score ties
independently of IDs. No new embeddings or relevance scores are computed.

GraphRAG receives ten selected entity carriers, ordered by maximum incident
frozen BM25 score and then stable endpoint occurrence. All semantic endpoint
strings are preserved. Text-unit and relationship references are updated
bijectively when IDs change; dangling references fail the probe instead of
counting as a finding. Its upstream entity ranking is supplied, not executed.

Neither native tokenizer is available in this runtime. Both components use their
tokenizer injection point with a reference counter of **one unit per UTF-8
byte**, at a fixed 8,000 reference-unit budget. This explicitly differs from
BPE token counting, a full prompt budget and the native query's allocation
between context sections. The budget and adapter were fixed before execution;
no smaller cap was chosen after observing GraphRAG's inactive bound.

Each case has six arms: baseline, label-derived IDs, permutation of existing
same-length IDs, held-ID label change, restored-original-ID round trip, and
input-order shuffle. Input shuffle is a distinct intervention; it does not count
as evidence of metadata sensitivity. All 864 case/arm component calls completed.

## Results

Every numerator below counts changed **analytical record sets**, not returned
IDs, incidental metadata or serialized hashes.

| Component | Cases with active reference bound | Label-derived IDs | Existing-ID permutation | Held-ID label change | ID round trip | Input shuffle |
|---|---:|---:|---:|---:|---:|---:|
| GraphRAG source branch | 0/72 | 0/72 | 0/72 | 0/72 | 0/72 | 0/72 |
| LightRAG final chunk selector | 72/72 | 0/72 | 0/72 | 0/72 | 0/72 | 72/72 |

GraphRAG selects 19–33 records, all of its eligible source candidates in each
case. Input shuffling changes their presentation order in 72/72 cases while
preserving their sets. The identity-invariance result is valid for these cases,
but **there is no saved-data test of its binding packing cutoff**. This remains
unknown; it is not a second strong negative about bounded selection.

LightRAG selects 28–36 records. Its active bound and input-shuffle changes show
that the harness can observe analytical selection changes in these cases.
Relabelled/permuted IDs and held-ID labels change returned raw metadata hashes
in 72/72 cases while leaving selected facts, multiplicities and analytical
ordering unchanged. Counting those raw hashes as evidence changes would give
a false positive. The ID round trip restores the raw output too.

Both implementations retain the supplied/semantic ordering in the tested
components rather than introducing our fact-ID packing order. There is no
observed ID-induced exchange to classify as equal-score or unequal-score.
Changes from deliberately shuffling input are not a replication of our
treatment-label effect, even when the reordered records have different BM25
scores. No native reranker or vector-store tie behavior was exercised.

## Validation and limitations

Eight focused harness tests pass. They cover source-body pin rejection,
consistent reference rewiring, broken-reference failure, ID-independent score
ties, ID round trips, metadata-versus-content comparison, Unicode-safe reference
costs and blocked out-of-scope callbacks.

Four native conformance calls use oversized-first and small-first fixtures at
the same fixed reference budget. Both native prefix builders return the expected
zero/one records. These were implementation-verification fixtures, not additional
saved-data evidence or a post-result cap sweep; they do not remedy GraphRAG's
inactive bound in the 72 actual cases.

Every native function body is verified against its frozen AST digest before
execution. Outputs reproduce byte-for-byte under a second Python hash
seed. The recorded runtime is Python 3.12.14 and pandas 2.2.3; it is a component
harness environment, not either framework's complete pinned installation.

The existing four tasks and graphs are reused and not independent new datasets.
There are no significance tests, accuracy measurements or prevalence estimates.
All full-pipeline behavior, actual native-tokenizer budgets and unexecuted
retrieval paths remain unmeasured. The original study and stage-audit results
are unchanged.

## Reproduce

```bash
python scripts/check_external_selection.py \
  --source-cache <pinned-source-cache> \
  --output-dir evaluation/followup/external-selection
python -m unittest discover -s tests -p 'test_external_selection.py' -v
```

An empty source cache can be populated with the optional `--fetch-sources` flag.
That setup downloads only the nine pinned public GitHub source/license files
and checks their hashes; it does not call model APIs. The committed source
manifest gives every exact repository path, commit, digest and selected function.
The native code itself is not vendored into this repository. Both pinned roots
include MIT license notices, retained in the private source cache on download.

`evaluation/followup/external-selection/summary.json` contains the environment,
source/function freeze, full control table and exclusions. `cases.json.gz`
contains all 864 cases/arms, candidate orders, selected occurrence indices,
reference costs and separate raw/analytical comparisons. Its indices refer to
the existing stage-audit catalog; that catalog's bytes are pinned in the source
manifest. No paid calls, notebook expansion, SQL execution or workflow dispatch
occurred.
