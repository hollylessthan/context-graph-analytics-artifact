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
