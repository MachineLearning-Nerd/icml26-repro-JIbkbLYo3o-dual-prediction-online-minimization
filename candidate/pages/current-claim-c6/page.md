# Claim 6 — general set-cover lower bound

**Candidate verdict: VERIFIED in the paper's deterministic/adaptive scope.**

The manuscript's printed phase order does **not** prove the claim: it yields
`H_m-1`, and its final increment is zero. The current verifier rejects it.
A corrected request-before-removal adversary forces
`1 + 1/m + ... + 1/2 = H_m`. The final surviving unit-cost set covers every
nested request, hence `OPT=1`. A perfect dual puts unit mass on the first
universal-support element and is identical for every elimination order.

| Check | Result |
|---|---|
| Parametric induction | Every integer `m>=1` |
| Exact regression rows | `m=1..64`, rational arithmetic |
| Independent checker | PASS |
| Printed-construction control | Rejected with exact gap 1 |
| Scope | Deterministic fractional algorithm; adaptive adversary |

[Contract](../../.openresearch/artifacts/C6/claim_contract.json) ·
[source audit](../../.openresearch/artifacts/C6/source_audit.md) ·
[method](../../.openresearch/artifacts/C6/method.md) ·
[expected raw result](../../.openresearch/artifacts/C6/raw/expected_result.json) ·
[verifier](../../repro/src/verify_remaining_theory.py) ·
[independent checker](../../repro/src/check_remaining_theory_independent.py) ·
[control](../../repro/src/run_remaining_theory_negative_controls.py)

No randomized-oblivious lower bound is claimed.
