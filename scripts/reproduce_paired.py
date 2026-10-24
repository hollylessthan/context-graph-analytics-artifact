"""Offline reproduction of paired planner results from the original saved archive."""
import collections
import hashlib
import io
import json
import sys
from pathlib import Path
from zipfile import ZipFile

def check(archive):
    with ZipFile(archive) as z:
        def read(name):
            return json.loads(z.read("paired-results/"+name))
        scores=read("scored-results.json")
        summary=read("paired-summary.json")
        collection=read("collection-summary.json")
        assert collection["completed_operations"]==264
        assert abs(collection["ledger"]["estimated_usd"]-3.6223495)<0.005
        assert len(scores)==264
        assert summary["observed_calls"]==264
        by=collections.defaultdict(dict)
        ids=set()
        for row in scores:
            op=row["operation_id"]
            assert op not in ids
            ids.add(op)
            arm=row["arm"]
            assert arm in ("000","001")
            key=(row["pair_id"],row["repetition"])
            assert arm not in by[key]
            by[key][arm]=bool(row["numerical_contract_pass"])
        assert len(by)==132 and all(len(v)==2 for v in by.values())
        plan=read("plan.json")
        members={m["pair_id"]:m["support_stratum"] for m in plan["members"]}
        assert len(members)==44
        stratum_map={"edge_lost":"Edge lost","edge_gained":"Edge gained","edge_missing_set_changed":"Missing set changed","no_edge_support_change":"No support change"}
        by_stratum=collections.defaultdict(list)
        for (pair_id,rep),arms in by.items():
            by_stratum[stratum_map[members[pair_id]]].append(arms)
        expected_strata={"Edge lost":(4,12,11,6,5,0),"Edge gained":(1,3,3,3,0,0),"Missing set changed":(7,21,3,2,1,0),"No support change":(32,96,81,81,0,0)}
        for stratum,(cases,n,orig,altered,orig_only,altered_only) in expected_strata.items():
            group=by_stratum[stratum]
            assert len(group)==n and sum(x["000"] for x in group)==orig and sum(x["001"] for x in group)==altered
            assert sum(x["000"] and not x["001"] for x in group)==orig_only
            assert sum(x["001"] and not x["000"] for x in group)==altered_only
            assert sum(1 for m in members.values() if stratum_map[m]==stratum)==cases
        changed_p3={"canonical|schema_llm|1|P3","canonical|schema_llm|2|P3"}
        p3_discordant=[x for x in scores if x["pair_id"] in changed_p3 and x["arm"]=="001" and x["repetition"] in (1,2,3) and x["failure_stage"]=="numerical_scoring" and by[x["pair_id"],x["repetition"]]["000"]]
        expected_errors={"exclusions.2017-11.not_eligible_delivered: count_mismatch","exclusions.2017-11.missing_lifecycle_timestamp: count_mismatch"}
        assert len(p3_discordant)==5
        assert all(set(x["answer"]["errors"])==expected_errors for x in p3_discordant)
        p2=[x for x in scores if x["pair_id"]=="canonical|simple_llm|1|P2" and x["arm"]=="001" and x["failure_stage"]=="sql_validation" and "COLUMNS" in str(x["failure_detail"])]
        assert len(p2)==1
        counts=collections.Counter(
            "".join("1" if pair[arm] else "0" for arm in ("000","001"))
            for pair in by.values()
        )
        assert dict(counts)=={"11":92,"00":34,"10":6}, counts
        assert summary["paired_pass_table_000_then_001"]==dict(counts)
        passes={arm:sum(pair[arm] for pair in by.values()) for arm in ("000","001")}
        assert passes=={"000":98,"001":92}
        cases={key[0] for key in by}
        assert len(cases)==44
        assert all(len({k[1] for k in by if k[0]==c})==3 for c in cases)
        changed={key[0] for key,v in by.items() if v["000"]!=v["001"]}
        assert len(changed)==3
        if "SHA256_MANIFEST.json" in z.namelist():
            manifest=json.loads(z.read("SHA256_MANIFEST.json"))
            for name,record in manifest["files"].items():
                blob=z.read(name)
                assert hashlib.sha256(blob).hexdigest()==record["sha256"]
                assert len(blob)==record["bytes"]
        print("PASS paired experiment: 264 unique operations, 132 balanced pairs, 44 cases")
        print("PASS outcome counts: 92 both-pass, 34 both-fail, 6 original-only-pass")
        print("PASS original=98/132, changed=92/132, discordances in 3 cases")
        print("SCOPE: offline replay of saved scored results, not new model inference")
if __name__=="__main__":
    if len(sys.argv)!=2:
        sys.exit("Usage: python scripts/reproduce_paired.py <paired-evidence.zip>")
    check(sys.argv[1])
