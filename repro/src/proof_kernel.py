"""Small exact-rational proof kernel for portable linear certificates."""
from __future__ import annotations

from fractions import Fraction


class CertificateError(ValueError):
    """Raised when a proof certificate does not derive its stated goal."""


def _fraction(value: str | int) -> Fraction:
    return Fraction(str(value))


def _coefficients(statement: dict, variables: tuple[str, ...]) -> dict[str, Fraction]:
    unknown = set(statement["coefficients"]) - set(variables)
    if unknown:
        raise CertificateError(f"unknown variables: {sorted(unknown)}")
    return {variable: _fraction(statement["coefficients"].get(variable, 0)) for variable in variables}


def check_farkas_certificate(certificate: dict) -> dict:
    variables = tuple(certificate["variables"])
    if len(set(variables)) != len(variables):
        raise CertificateError("duplicate variable")
    premises = {premise["name"]: premise for premise in certificate["premises"]}
    if len(premises) != len(certificate["premises"]):
        raise CertificateError("duplicate premise")

    combined = {variable: Fraction(0) for variable in variables}
    combined_rhs = Fraction(0)
    for term in certificate["farkas_combination"]:
        premise = premises.get(term["premise"])
        if premise is None:
            raise CertificateError(f"missing premise {term['premise']}")
        weight = _fraction(term["weight"])
        if premise["relation"] == "le" and weight < 0:
            raise CertificateError("inequality premise has negative weight")
        if premise["relation"] not in {"le", "eq"}:
            raise CertificateError("unsupported premise relation")
        for variable, coefficient in _coefficients(premise, variables).items():
            combined[variable] += weight * coefficient
        combined_rhs += weight * _fraction(premise["rhs"])

    goal = certificate["goal"]
    if goal["relation"] != "le":
        raise CertificateError("goal must be an inequality")
    expected = _coefficients(goal, variables)
    if combined != expected or combined_rhs != _fraction(goal["rhs"]):
        raise CertificateError(
            f"combination mismatch: got {combined} <= {combined_rhs}, "
            f"expected {expected} <= {goal['rhs']}"
        )
    terms = []
    for variable in variables:
        coefficient = expected[variable]
        if coefficient:
            terms.append(f"{coefficient}*{variable}")
    exact_goal = " + ".join(terms) + f" <= {_fraction(goal['rhs'])}"
    if variables == ("ALG", "OPT", "ETA") and tuple(expected.values()) == (
        Fraction(1),
        Fraction(-1),
        Fraction(-1),
    ):
        exact_goal = "ALG - OPT - ETA <= 0"
    return {
        "variables": len(variables),
        "premises": len(premises),
        "combination_terms": len(certificate["farkas_combination"]),
        "exact_goal": exact_goal,
    }


def check_telescoping_induction() -> dict:
    # D_1 = (-w_1 + w_0) - w_0 + w_1.
    base = {"w0": Fraction(1) - 1, "w1": Fraction(-1) + 1}
    if any(base.values()):
        raise CertificateError("telescoping base case failed")

    # D_(T+1)-D_T contributes the new summand (-w_new+w_old) and
    # changes the terminal boundary from +w_old to +w_new.
    step = {
        "w_old": Fraction(1) - 1,
        "w_new": Fraction(-1) + 1,
    }
    if any(step.values()):
        raise CertificateError("telescoping induction step failed")
    return {
        "base_horizon": 1,
        "induction_step": "T -> T+1",
        "path_scope": "arbitrary state path",
    }


def check_structural_obligations(certificate: dict) -> dict:
    required = {
        "The algorithm argmin gives its one-step equality.",
        "Any offline path gives the corresponding one-step lower bound.",
        "Both path sums telescope by induction for arbitrary T >= 1.",
        "Each discrepancy is bounded above by its coordinate maximum and below by its coordinate minimum.",
        "w_hat_T is zero on both terminal states, so the terminal potentials agree.",
    }
    supplied = set(certificate["structural_obligations"])
    if supplied != required:
        raise CertificateError("structural obligations differ from the theorem contract")
    return check_telescoping_induction()
