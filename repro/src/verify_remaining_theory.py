from __future__ import annotations

import json
from pathlib import Path

from theory_certificates import check_claim1, check_claim3, check_claim6

ROOT = Path(__file__).resolve().parents[2]
result = {
    "C1": check_claim1(),
    "C3": check_claim3(),
    "C6": check_claim6(),
    "checker": "primary exact symbolic certificate",
}
out = ROOT / "outputs/remaining_theory_verification.json"
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
