from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
raw = json.loads((ROOT / "outputs/claim5_four_route_audit.json").read_text())
assert raw["verdict"] == "BLOCKED"
assert raw["confidence"] == "LOW"
assert raw["routes_completed"] == 4
assert len({route["route"] for route in raw["routes"]}) == 4
ghcn = raw["routes"][1]["data"]
assert ghcn["target_years"] == 153
assert ghcn["station_ids"] == ["USW00094728"]
assert len(ghcn["unresolved_source_choices"]) >= 5
bike = raw["routes"][2]["data"]
assert bike["compressed_bytes"] > 0
assert bike["downloaded_for_this_audit"] is False
assert len(bike["unresolved_source_choices"]) >= 8
assert raw["routes"][3]["result"] == "NO_VALID_COUNTEREXAMPLE"
result = {
    "status": "PASS",
    "checked_verdict": "BLOCKED",
    "distinct_routes": 4,
    "promotion_allowed": False,
    "reason": "exact experiment semantics and processed artifacts are unavailable",
}
(ROOT / "outputs/claim5_independent_checker.json").write_text(
    json.dumps(result, indent=2) + "\n"
)
print(json.dumps(result, indent=2))
