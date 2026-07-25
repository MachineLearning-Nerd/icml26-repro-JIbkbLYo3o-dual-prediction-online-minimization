from __future__ import annotations
import json, os, platform, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
started = time.perf_counter()
subprocess.run([sys.executable, "repro/src/verify_dual_predictions.py", "--output", "outputs/verification.json"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/verify_claim2_proof.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/check_claim2_independent.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/run_claim2_negative_control.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/verify_remaining_theory.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/check_remaining_theory_independent.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/run_remaining_theory_negative_controls.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "repro/tests", "-v"], cwd=ROOT, check=True)
v = json.loads((ROOT / "outputs/verification.json").read_text())
c2 = json.loads((ROOT / "outputs/claim2_proof_verification.json").read_text())
c2_independent = json.loads((ROOT / "outputs/claim2_independent_checker.json").read_text())
c2_control = json.loads((ROOT / "outputs/claim2_negative_control.json").read_text())
remaining = json.loads((ROOT / "outputs/remaining_theory_verification.json").read_text())
remaining_independent = json.loads((ROOT / "outputs/remaining_theory_independent.json").read_text())
remaining_controls = json.loads((ROOT / "outputs/remaining_theory_negative_controls.json").read_text())
assert v["verified_claims"] == 5 and v["falsified_claims"] == 0
assert c2["verdict"] == "VERIFIED"
assert c2_independent["status"] == "PASS"
assert c2_control["status"] == "REJECTED_AS_INTENDED"
assert all(remaining[c]["verdict"] == "VERIFIED" for c in ("C1", "C3", "C6"))
assert remaining_independent["status"] == "PASS"
assert remaining_controls["status"] == "REJECTED_AS_INTENDED"
gate = {
    "paper": "JIbkbLYo3o",
    "gate": "passed",
    "tests_passed": True,
    "publication_gate_passed": True,
    "verified_claims": 5,
    "current_claims": {
        "C1": "VERIFIED",
        "C2": "VERIFIED",
        "C3": "VERIFIED",
        "C6": "VERIFIED",
    },
    "historical_regression": "PASS",
    "scope": v["scope"],
    "compute": {
        "estimated_cores": 1,
        "selected_flavor": "local (no flavor)",
        "allocation": "shared local machine; no dedicated CPU allocation",
        "visible_logical_cpus": os.cpu_count(),
        "python": platform.python_version(),
        "runtime_seconds": time.perf_counter() - started,
    },
}
(ROOT / "outputs/publication_gate.json").write_text(json.dumps(gate, indent=2) + "\n")
print(json.dumps(gate, indent=2))
