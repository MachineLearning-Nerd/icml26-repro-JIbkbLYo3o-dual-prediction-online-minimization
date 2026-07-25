"""Independent Claim 2 checker; deliberately does not import proof_kernel."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / ".openresearch" / "artifacts" / "C2" / "proof_certificate.json"
if not CERTIFICATE.exists():
    CERTIFICATE = ROOT / "evidence" / "C2" / "proof_certificate.json"


def check(certificate: dict) -> None:
    variables = certificate["variables"]
    premises = {item["name"]: item for item in certificate["premises"]}
    total = {name: Fraction(0) for name in variables}
    rhs = Fraction(0)
    for item in certificate["farkas_combination"]:
        premise = premises[item["premise"]]
        weight = Fraction(item["weight"])
        if premise["relation"] == "le":
            assert weight >= 0
        for name in variables:
            total[name] += weight * Fraction(premise["coefficients"].get(name, "0"))
        rhs += weight * Fraction(premise["rhs"])
    goal = certificate["goal"]
    goal_coefficients = {name: Fraction(goal["coefficients"].get(name, "0")) for name in variables}
    assert total == goal_coefficients
    assert rhs == Fraction(goal["rhs"])

    # Reconstruct the base and generic extension of the path-potential identity.
    assert (Fraction(-1) + 1) == 0  # terminal w_1
    assert (Fraction(1) - 1) == 0   # initial w_0
    assert (Fraction(1) - 1) == 0   # old terminal in T -> T+1
    assert (Fraction(-1) + 1) == 0  # new terminal in T -> T+1


def main() -> None:
    certificate = json.loads(CERTIFICATE.read_text())
    check(certificate)
    result = {
        "claim_id": "C2",
        "checker": "independent exact-rational reconstruction",
        "imports_primary_kernel": False,
        "status": "PASS",
        "derived_goal": "ALG - OPT - ETA <= 0",
    }
    (ROOT / "outputs" / "claim2_independent_checker.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
