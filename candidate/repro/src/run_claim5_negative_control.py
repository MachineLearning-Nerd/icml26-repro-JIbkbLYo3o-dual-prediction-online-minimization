from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
raw = json.loads((ROOT / "outputs/claim5_four_route_audit.json").read_text())

# Deliberately attempt the invalid promotion used by the historical baseline:
# source figures plus public data availability are not a rerun.
promotion_requirements = {
    "author_algorithm_revision": False,
    "processed_input_hashes": False,
    "exact_initial_states": False,
    "exact_random_seeds": False,
    "raw_regenerated_metrics": False,
}
promoted = all(promotion_requirements.values()) and raw["verdict"] == "VERIFIED"
assert not promoted
result = {
    "status": "REJECTED_AS_INTENDED",
    "mutation": "promote source/data audit to VERIFIED",
    "promotion_requirements": promotion_requirements,
    "reason": "availability and figure consistency are not empirical reproduction",
}
(ROOT / "outputs/claim5_negative_control.json").write_text(
    json.dumps(result, indent=2) + "\n"
)
print(json.dumps(result, indent=2))
