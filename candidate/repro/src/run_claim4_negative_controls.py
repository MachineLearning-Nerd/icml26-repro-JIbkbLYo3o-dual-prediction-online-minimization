from __future__ import annotations

import json
from pathlib import Path

from caching_instability import belady_cost, build_instance, simulate_combiner

ROOT = Path(__file__).resolve().parents[2]
k, q = 32, 32
instance = build_instance(k, q, perturbed=False)
run = simulate_combiner(
    instance["true"], instance["predictions"], k, tie_leader="blind"
)
opt = belady_cost(instance["true"], k)
ratio = run["combined_cost"] / opt

# With no replacement, the stale page is absent and the intended collapse
# disappears. A control that still had the >10 collapse would be invalid.
assert instance["differing_requests"] == 0
assert instance["incorrect_prediction_records"] == 0
assert ratio < 3
result = {
    "status": "REJECTED_AS_INTENDED",
    "control": "anticipated sequence equals true sequence",
    "differing_requests": 0,
    "incorrect_prediction_records": 0,
    "combined_cost": run["combined_cost"],
    "offline_optimum": opt,
    "ratio": ratio,
    "rejection_threshold": 3,
}
(ROOT / "outputs/claim4_negative_control.json").write_text(
    json.dumps(result, indent=2) + "\n"
)
print(json.dumps(result, indent=2))
