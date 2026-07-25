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
| Fixed command | `uv run --frozen python repro/src/run_publication_gate.py` |

[Contract](../../evidence/C6/claim_contract.json) ·
[source audit](../../evidence/C6/source_audit.md) ·
[method](../../evidence/C6/method.md) ·
[evaluation record](../../evidence/C6/EVAL.md) ·
[raw result](../../evidence/runs/C1-C3-C6-theory.json) ·
[verifier](../../repro/src/verify_remaining_theory.py) ·
[independent checker](../../repro/src/check_remaining_theory_independent.py) ·
[control](../../repro/src/run_remaining_theory_negative_controls.py)

No randomized-oblivious lower bound is claimed.

Run `f4893104-c0c9-4e01-bb31-1699b469f795`, Git
`2ea21d42e6c25dcf2866c7e056254f3c8d4b49f7`, local estimated one core,
runtime 0.616 seconds. Exact rational regression rows cover `m=1..64`; the induction
covers every integer `m>=1`. Seeds: none; the adversary and proof are
deterministic.

Limitation: the verdict is restricted to the paper's deterministic algorithm
and adaptive-adversary scope.
