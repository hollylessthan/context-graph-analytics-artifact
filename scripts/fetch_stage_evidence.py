"""Fetch exact published frozen stage-local records without paid calls."""
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
record = json.loads((ROOT/"evidence/label-stage-summary.json").read_text())
expected = record["output_sha256"]
commit = "c6c886cecfe389e1c3906342ac466e25955989ca"
base = "https://raw.githubusercontent.com/hollylessthan/context-graph-analytics-study/" + commit + "/evaluation/followup/label-stage-audit/"
with zipfile.ZipFile(ROOT/"stage-local-evidence.zip", "w", compression=zipfile.ZIP_STORED) as bundle:
    for name, digest in expected.items():
        with urllib.request.urlopen(base + name, timeout=45) as response:
            data = response.read()
        observed = hashlib.sha256(data).hexdigest()
        if observed != digest:
            raise SystemExit(f"Frozen source hash mismatch for {name}: {observed} != {digest}")
        bundle.writestr("stage-local/" + name, data)
        print(f"VERIFIED {name}: {len(data)} bytes, sha256={digest}")
print("PASS: all 4 compressed stage-local frozen evidence files match summary-record SHA256")
print("SCOPE: integrity and collection verified, not independent recomputation of factorial rows")
