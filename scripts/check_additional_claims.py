"""Check cross-study claims against exported frozen records. No API calls."""
import collections,gzip,json,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
read=lambda n:json.loads((R/"evidence"/n).read_text())
p3=read("paired-discordance-validation.json")["p3_data_checks"]
assert [p3[m]["contract_rule_counts"]["included"] for m in ("2017-11","2018-04")]==[7288,6798]
assert all(p3[m]["included_sets_identical"] for m in ("2017-11","2018-04"))
assert sum(len(p3[m]["units_with_different_reason"]) for m in ("2017-11","2018-04"))==1
g=read("invariance-gate-phase-a.json")
assert g["followup_violations"]==0 and g["contexts_checked"]==168
assert sum(t["perturbations"] for x in g["graphs"] for t in x["tasks"])==3696
assert sum(len(t["followup_violations"]) for x in g["graphs"] for t in x["tasks"])==0
o=read("offline-analysis.json")["summary"]
assert (o["simple_llm|8000"]["document_frozen_complete"],o["schema_llm|8000"]["document_frozen_complete"])==(22,13)
assert (o["simple_llm|8000"]["reverse_document_frozen_complete"],o["schema_llm|8000"]["reverse_document_frozen_complete"])==(12,15)
f=read("review-followups.json")
assert f["permutations_per_graph"]==100
ranges={x["method"]:(min(x["permuted_complete_counts"]),max(x["permuted_complete_counts"])) for x in f["permutation_summary"]}
assert ranges=={"simple_llm":(14,27),"schema_llm":(14,22)}
primary=read("primary-results.json")
rows={(x["task_id"],x["condition"]):x["passes"] for x in primary["E2_task_pass"]}
for task,vals in {"P1":(9,9),"P2":(5,1),"P3":(8,6),"P4":(8,9)}.items():
 assert (rows[task,"simple_llm"],rows[task,"schema_llm"])==vals
assert all(rows[t,c]==9 for t in ("P1","P2","P3","P4") for c in ("deterministic_schema","lexical_source","identical_facts_flat"))
assert all(x["recall"]["mean"]==1 and abs(x["precision"]["mean"]-48/49)<1e-12 for x in primary["E6_construction_variation"])
ext=read("external-selection-summary.json")
for x in ext["results"]:
 assert x["baseline_cases"]==72
 assert x["cases_with_active_bound"]==(0 if x["implementation"]=="graphrag" else 72)
 for intervention in x["interventions"]:
  if intervention["intervention"] in ("label_derived_ids","permuted_existing_ids"):
   assert intervention["analytical_set_changed"]==0
  if intervention["intervention"]=="input_shuffle" and x["implementation"]=="lightrag":
   assert intervention["analytical_set_changed"]==72
with zipfile.ZipFile(R/"evidence/stage-local-evidence.zip") as z:
 support=json.loads(gzip.decompress(z.read("stage-local/support.json.gz")))
 pairs=json.loads(gzip.decompress(z.read("stage-local/pairs.json.gz")))
gap=collections.Counter()
association=collections.Counter()
for row in support:
 association[(row["outcome_category"],row["edge_complete"])]+=1
 for item in row["items"]:
  if item["strict_credited"]:continue
  gap["all"]+=1
  if item["item"].startswith("relationship:"):gap["relationship"]+=1
  elif item["edge_credited"]:gap["join_endpoint"]+=1
  elif item["identifier_availability_upper"]:gap["other_visible"]+=1
  else:gap["not_visible"]+=1
assert (gap["all"],gap["relationship"],gap["join_endpoint"],gap["other_visible"],gap["not_visible"])==(84,3,36,8,37),gap
assert sum(n for (outcome,complete),n in association.items() if outcome=="pass" and complete)==50
assert association[("pass",False)]==5
assert association[("table_name_rejection",True)]==4
assert all(not c for (outcome,c),n in association.items() if outcome in ("wrong_answer","explicit_refusal_in_sql") and n)
print("PASS supplementary: 3696 invariance checks, 22/13 vs 12/15, permutation ranges, task table, support gaps, external probes")
print("Outcome/completeness association:",dict((str(k),v) for k,v in association.items()))
