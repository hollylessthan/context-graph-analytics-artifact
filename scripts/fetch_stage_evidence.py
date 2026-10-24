"""Fetch exact published frozen stage-local records without paid calls."""
import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
record = json.loads((ROOT/"evidence/label-stage-summary.json").read_text())
expected = record["output_sha256"]
commit = "c6c886cecfe389e1c3906342ac466e25955989ca"
source = "https://github.com/hollylessthan/context-graph-analytics-study.git"
with tempfile.TemporaryDirectory() as temp:
    work = Path(temp)/"source"
    subprocess.run(["git", "init", "-q", str(work)], check=True)
    subprocess.run(["git", "-C", str(work), "remote", "add", "origin", source], check=True)
    subprocess.run(["git", "-C", str(work), "fetch", "-q", "--depth", "1", "origin", commit], check=True)
    with zipfile.ZipFile(ROOT/"stage-local-evidence.zip", "w", compression=zipfile.ZIP_STORED) as bundle:
      for name, digest in expected.items():
        data = subprocess.check_output(["git", "-C", str(work), "show", commit + ":evaluation/followup/label-stage-audit/" + name])
        observed = hashlib.sha256(data).hexdigest()
        if observed != digest:
            raise SystemExit(f"Frozen source hash mismatch for {name}: {observed} != {digest}")
        bundle.writestr("stage-local/" + name, data)
        print(f"VERIFIED {name}: {len(data)} bytes, sha256={digest}")
print("PASS: all 4 compressed stage-local frozen evidence files match summary-record SHA256")
print("SCOPE: integrity and collection verified, not independent recomputation of factorial rows")
