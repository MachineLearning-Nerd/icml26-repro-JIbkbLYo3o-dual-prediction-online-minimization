from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
controls = {}

# C1: omitting the 1/(1-alpha) amplification must not equal the theorem.
epsilon = Fraction(1, 3)
alpha = 1 / (1 + epsilon)
controls["C1_drop_miss_amplification"] = {
    "rejected": Fraction(1) != 1 / (1 - alpha),
    "reason": "underprediction coefficient changed",
}

# C3: the appendix's undefined alpha cannot certify a beta-bound.
controls["C3_alpha_beta_typo"] = {
    "rejected": True,
    "reason": "alpha is not defined in the stability lemma; theorem uses beta",
}

# C6: execute the phase order printed in the manuscript.  It gives H_m-1.
m = 16
printed = sum((Fraction(1, j) for j in range(2, m + 1)), Fraction())
hm = sum((Fraction(1, j) for j in range(1, m + 1)), Fraction())
controls["C6_printed_remove_before_request"] = {
    "rejected": printed != hm,
    "observed": str(printed),
    "required": str(hm),
    "gap": str(hm - printed),
}

assert all(control["rejected"] for control in controls.values())
result = {"status": "REJECTED_AS_INTENDED", "controls": controls}
(ROOT / "outputs/remaining_theory_negative_controls.json").write_text(
    json.dumps(result, indent=2) + "\n"
)
print(json.dumps(result, indent=2))
