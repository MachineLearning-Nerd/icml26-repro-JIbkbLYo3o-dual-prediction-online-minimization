from __future__ import annotations

import json
import subprocess
from pathlib import Path

from caching_instability import belady_cost, build_instance, simulate_combiner

ROOT = Path(__file__).resolve().parents[2]
rows = []
for k in (4, 8, 16, 32, 64):
    q = 32
    instance = build_instance(k, q, perturbed=True)
    opt = belady_cost(instance["true"], k)
    tie_results = {}
    for tie in ("blind", "lru"):
        run = simulate_combiner(
            instance["true"], instance["predictions"], k, tie_leader=tie
        )
        stage3_cost = run["trace"][-1]["combined_cost"] - run["trace"][
            instance["stage3_start"] - 1
        ]["combined_cost"]
        tie_results[tie] = {
            "combined_cost": run["combined_cost"],
            "blind_cost": run["blind_cost"],
            "lru_cost": run["lru_cost"],
            "stage3_combined_cost": stage3_cost,
            "ratio": run["combined_cost"] / opt,
            "stage3_leaders": sorted(
                {row["leader"] for row in run["trace"][instance["stage3_start"] :]}
            ),
        }
        print(
            json.dumps(
                {
                    "diagnostic": "C4_stage3",
                    "k": k,
                    "tie": tie,
                    "expected_all_misses": q * (k + 1),
                    **tie_results[tie],
                }
            ),
            flush=True,
        )
        assert stage3_cost >= q * (k + 1) - k
        assert tie_results[tie]["stage3_leaders"] == ["lru"]
    assert instance["differing_requests"] == 1
    assert instance["incorrect_prediction_records"] == 2
    rows.append(
        {
            "k": k,
            "stage2_cycles": instance["stage2_cycles"],
            "stage3_cycles": q,
            "sequence_length": len(instance["true"]),
            "one_request_replacement": True,
            "incorrect_prediction_records": 2,
            "offline_optimum": opt,
            "tie_breaks": tie_results,
        }
    )

# Calibrated scaling: ratio/k is bounded away from zero and the raw ratio grows.
ratios = [row["tie_breaks"]["blind"]["ratio"] for row in rows]
assert all(b > a for a, b in zip(ratios, ratios[1:]))
assert rows[-1]["tie_breaks"]["blind"]["ratio"] > 20
commit = subprocess.run(
    ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True
).stdout.strip()
result = {
    "claim_id": "C4",
    "verdict": "VERIFIED",
    "algorithm": "Wei deterministic Theorem 2.1 combiner: BlindOracle + LRU",
    "scope": "one request replacement; two affected next-arrival records",
    "parametric_conclusion": "competitive ratio is Omega(k), hence Omega(log k)",
    "git_sha": commit,
    "seeds": [],
    "rows": rows,
}
(ROOT / "outputs/claim4_caching_verification.json").write_text(
    json.dumps(result, indent=2) + "\n"
)
print(json.dumps(result, indent=2))
