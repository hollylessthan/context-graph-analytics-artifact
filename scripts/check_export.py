"""Provider-free validation of exported frozen summaries, not complete experiment replay."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def read(name):
    return json.loads((root/"evidence"/name).read_text())
original=read("primary-results.json")
means={r["condition"]:r["mean_task_proportion"] for r in original["E4_condition_summary"]}
assert (round(means["simple_llm"]*36),round(means["schema_llm"]*36))==(30,25)
assert all(round(means[x]*36)==36 for x in ("deterministic_schema","identical_facts_flat","lexical_source"))
arms=read("label-stage-summary.json")["summary"]["arms"]
by={(r["method"],r["mask"]):r for r in arms}
expected={"000":((19,26),(18,28)),"001":((15,27),(17,24)),"010":((21,29),(18,28)),"011":((16,29),(17,24)),"100":((19,26),(17,28)),"101":((15,28),(17,24)),"110":((21,28),(17,28)),"111":((16,29),(17,24))}
for mask, pair in expected.items():
    for method, (strict,edge) in zip(("simple_llm","schema_llm"),pair):
        record=by[method,mask]
        assert (record["contexts"],record["strict_complete"],record["edge_complete"])==(36,strict,edge)
assert sum(by[x,"001"]["visible_set_changes_from_original"] for x in ("simple_llm","schema_llm"))==44
assert read("paired-discordance-validation.json")["run_id"]==40120563599
external=read("external-selection-summary.json")
assert external["provider_calls"]==0 and len(external["results"])==2
print("PASS: frozen original comparisons, 16 factorial summary rows, 44 packing changes, paired audit provenance, external summaries.")
print("SCOPE: checks frozen summary records; companion scripts independently re-aggregate paired and stage-local traces.")
