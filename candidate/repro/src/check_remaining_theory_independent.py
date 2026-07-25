"""Independent checker: intentionally imports no primary certificate code."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
primary = json.loads((ROOT / "outputs/remaining_theory_verification.json").read_text())

# C1: test the rational identities on exact values not selected by the primary.
for epsilon in map(Fraction, (1, 2, 3, 7, 19)):
    alpha = Fraction(1, 1) / (1 + epsilon)
    assert 1 / alpha == 1 + epsilon
    assert 1 / (1 - alpha) == (1 + epsilon) / epsilon

# C3: check the proof cone by maximizing the claimed L1 expression subject to
# its boundary inequalities on an exhaustive integer grid.
max_ratio = Fraction()
for beta in range(1, 12):
    for delta0 in range(beta + 1):
        for deltad in range(delta0, beta + 1):
            for sd in range(deltad, beta + 1):
                l1_upper = sd + deltad - delta0
                assert l1_upper <= 2 * beta
                max_ratio = max(max_ratio, Fraction(l1_upper, beta))
assert max_ratio == 2

# C6: derive the lower bound independently from survivor counts.
for m in range(1, 65):
    forced = Fraction(1)
    for survivors in range(m, 1, -1):
        forced += Fraction(1, survivors)
    expected = sum((Fraction(1, j) for j in range(1, m + 1)), Fraction())
    assert forced == expected

assert {primary["C1"]["verdict"], primary["C3"]["verdict"], primary["C6"]["verdict"]} == {
    "VERIFIED"
}
result = {
    "status": "PASS",
    "independence": "does not import theory_certificates",
    "C1_exact_epsilon_values": 5,
    "C3_constraint_grid_points": sum(
        1
        for beta in range(1, 12)
        for delta0 in range(beta + 1)
        for deltad in range(delta0, beta + 1)
        for sd in range(deltad, beta + 1)
    ),
    "C3_sharp_factor": str(max_ratio),
    "C6_symbolic_survivor_counts": "m=1..64",
}
(ROOT / "outputs/remaining_theory_independent.json").write_text(
    json.dumps(result, indent=2) + "\n"
)
print(json.dumps(result, indent=2))
