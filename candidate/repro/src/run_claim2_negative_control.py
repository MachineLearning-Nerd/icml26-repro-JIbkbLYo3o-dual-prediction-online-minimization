"""Mutate the Claim 2 goal and require both checkers to reject it."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from check_claim2_independent import check as independent_check
from proof_kernel import CertificateError, check_farkas_certificate


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / ".openresearch" / "artifacts" / "C2" / "proof_certificate.json"
if not CERTIFICATE.exists():
    CERTIFICATE = ROOT / "evidence" / "C2" / "proof_certificate.json"


def main() -> None:
    original = json.loads(CERTIFICATE.read_text())
    mutated = copy.deepcopy(original)
    mutated["goal"]["coefficients"]["ETA"] = "-1/2"

    rejected = {}
    try:
        check_farkas_certificate(mutated)
    except CertificateError as error:
        rejected["primary"] = str(error)
    try:
        independent_check(mutated)
    except AssertionError:
        rejected["independent"] = "exact coefficient mismatch"
    assert set(rejected) == {"primary", "independent"}
    result = {
        "claim_id": "C2",
        "mutation": "goal ETA coefficient -1 -> -1/2",
        "expected": "both checkers reject",
        "status": "REJECTED_AS_INTENDED",
        "rejections": rejected,
    }
    (ROOT / "outputs" / "claim2_negative_control.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
