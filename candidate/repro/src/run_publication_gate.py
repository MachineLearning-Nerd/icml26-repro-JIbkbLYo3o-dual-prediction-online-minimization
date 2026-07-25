from __future__ import annotations
import json, os, platform, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
(ROOT / "outputs").mkdir(exist_ok=True)
started = time.perf_counter()
subprocess.run([sys.executable, "repro/src/verify_dual_predictions.py", "--output", "outputs/verification.json"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/verify_claim2_proof.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/check_claim2_independent.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/run_claim2_negative_control.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/verify_remaining_theory.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/check_remaining_theory_independent.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/run_remaining_theory_negative_controls.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/verify_claim4_caching.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/check_claim4_independent.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/run_claim4_negative_controls.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/audit_claim5_real_data.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/check_claim5_independent.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/run_claim5_negative_control.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "repro/tests", "-v"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/verify_release_candidate.py"], cwd=ROOT, check=True)
v = json.loads((ROOT / "outputs/verification.json").read_text())
c2 = json.loads((ROOT / "outputs/claim2_proof_verification.json").read_text())
c2_independent = json.loads((ROOT / "outputs/claim2_independent_checker.json").read_text())
c2_control = json.loads((ROOT / "outputs/claim2_negative_control.json").read_text())
remaining = json.loads((ROOT / "outputs/remaining_theory_verification.json").read_text())
remaining_independent = json.loads((ROOT / "outputs/remaining_theory_independent.json").read_text())
remaining_controls = json.loads((ROOT / "outputs/remaining_theory_negative_controls.json").read_text())
c4 = json.loads((ROOT / "outputs/claim4_caching_verification.json").read_text())
c4_independent = json.loads((ROOT / "outputs/claim4_independent_checker.json").read_text())
c4_control = json.loads((ROOT / "outputs/claim4_negative_control.json").read_text())
c5 = json.loads((ROOT / "outputs/claim5_four_route_audit.json").read_text())
c5_independent = json.loads((ROOT / "outputs/claim5_independent_checker.json").read_text())
c5_control = json.loads((ROOT / "outputs/claim5_negative_control.json").read_text())
release = json.loads((ROOT / "outputs/release_candidate_verification.json").read_text())
assert v["verified_claims"] == 5 and v["falsified_claims"] == 0
assert c2["verdict"] == "VERIFIED"
assert c2_independent["status"] == "PASS"
assert c2_control["status"] == "REJECTED_AS_INTENDED"
assert all(remaining[c]["verdict"] == "VERIFIED" for c in ("C1", "C3", "C6"))
assert remaining_independent["status"] == "PASS"
assert remaining_controls["status"] == "REJECTED_AS_INTENDED"
assert c4["verdict"] == "VERIFIED"
assert c4_independent["status"] == "PASS"
assert c4_control["status"] == "REJECTED_AS_INTENDED"
assert c5["verdict"] == "BLOCKED" and c5["routes_completed"] == 4
assert c5_independent["status"] == "PASS"
assert c5_control["status"] == "REJECTED_AS_INTENDED"
assert release["status"] == "PASS"
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
        "C4": "VERIFIED",
        "C5": "BLOCKED",
        "C6": "VERIFIED",
    },
    "historical_regression": "PASS",
    "evaluator_visible_release": release,
    "scope": v["scope"],
    "compute": {
        "estimated_cores": 2,
        "selected_flavor": "hf cpu-upgrade",
        "allocation": "Hugging Face Jobs CPU allocation; detected at runtime",
        "visible_logical_cpus": os.cpu_count(),
        "python": platform.python_version(),
        "runtime_seconds": time.perf_counter() - started,
    },
}
(ROOT / "outputs/publication_gate.json").write_text(json.dumps(gate, indent=2) + "\n")
print(json.dumps(gate, indent=2))
