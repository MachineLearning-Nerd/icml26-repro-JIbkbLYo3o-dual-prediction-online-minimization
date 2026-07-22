from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
subprocess.run([sys.executable, "repro/src/verify_dual_predictions.py", "--output", "outputs/verification.json"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "repro/tests", "-v"], cwd=ROOT, check=True)
v = json.loads((ROOT / "outputs/verification.json").read_text())
assert v["verified_claims"] == 5 and v["falsified_claims"] == 0
gate = {"paper": "JIbkbLYo3o", "gate": "passed", "tests_passed": True, "publication_gate_passed": True, "verified_claims": 5, "scope": v["scope"]}
(ROOT / "outputs/publication_gate.json").write_text(json.dumps(gate, indent=2) + "\n")
print(json.dumps(gate, indent=2))
