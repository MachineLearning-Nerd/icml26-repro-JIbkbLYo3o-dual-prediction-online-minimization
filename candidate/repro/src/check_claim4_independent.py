"""Independent trace invariants; imports only the raw verifier output."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
raw = json.loads((ROOT / "outputs/claim4_caching_verification.json").read_text())
for row in raw["rows"]:
    k = row["k"]
    q = row["stage3_cycles"]
    assert row["one_request_replacement"]
    assert row["incorrect_prediction_records"] == 2
    for result in row["tie_breaks"].values():
        assert result["stage3_combined_cost"] >= q * (k + 1) - k
        assert result["stage3_leaders"] == ["lru"]
        assert abs(result["ratio"] - result["combined_cost"] / row["offline_optimum"]) < 1e-12

normalized = [
    row["tie_breaks"]["blind"]["ratio"] / row["k"] for row in raw["rows"]
]
assert min(normalized[-3:]) > 0.30
result = {
    "status": "PASS",
    "imports_simulator": False,
    "checked_rows": len(raw["rows"]),
    "minimum_ratio_over_k_last_three": min(normalized[-3:]),
}
(ROOT / "outputs/claim4_independent_checker.json").write_text(
    json.dumps(result, indent=2) + "\n"
)
print(json.dumps(result, indent=2))
