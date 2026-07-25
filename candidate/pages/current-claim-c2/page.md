# Claim 2 — exact MTS Bellman proof

**Candidate verdict: VERIFIED.** This is a proof certificate for the universal
theorem, not a finite-instance extrapolation.

For every finite MTS horizon and every prediction sequence ending in
`w_hat_T=0`, Algorithm 3 satisfies

`ALG <= OPT + eta`,

where `eta` is the sum of span seminorms of the Bellman discrepancies. Therefore
`ALG/OPT <= 1+eta/OPT` when `OPT>0`. When `OPT=0`, only the additive statement is
asserted because the displayed ratio is undefined.

## Exact proof result

| Field | Result |
|---|---|
| Source | arXiv 2606.05380, `th:MTSBoundForBellmanError` |
| Source SHA-256 | `364d1b1dabc7c09bce0839e214580e1beb08d78c2de7bdf2edd61fada706077c` |
| Proof arithmetic | Exact rational |
| Horizon handling | Base `T=1` plus symbolic `T -> T+1` telescoping step |
| Derived inequality | `ALG - OPT - ETA <= 0` |
| Independent checker | PASS |
| Negative control | Mutated `ETA` coefficient rejected by both checkers |
| Seeds | None; deterministic proof |
| Fixed command | `uv run --frozen python repro/src/run_publication_gate.py` |
| Environment | CPython 3.12.11, dependency-free `uv.lock` |
| Run / Git | `637ce304-11c9-4478-8552-082978e4196f` / `cd2f6d3ca1a732ea8e9bcb867b97cf51a76015f1` |
| CPU / runtime | Local, estimated 1 core, 8 visible logical CPUs, 0.977 s |

Raw contract:
[`claim_contract.json`](../../evidence/C2/claim_contract.json).
Source audit and evaluation record:
[`source_audit.md`](../../evidence/C2/source_audit.md) and
[`EVAL.md`](../../evidence/C2/EVAL.md).
Method:
[`method.md`](../../evidence/C2/method.md).
Proof certificate:
[`proof_certificate.json`](../../evidence/C2/proof_certificate.json).
Expected machine-readable result:
[`C2-MTS-proof.json`](../../evidence/runs/C2-MTS-proof.json).
Primary verifier:
[`verify_claim2_proof.py`](../../repro/src/verify_claim2_proof.py).
Independent checker:
[`check_claim2_independent.py`](../../repro/src/check_claim2_independent.py).
Negative control:
[`run_claim2_negative_control.py`](../../repro/src/run_claim2_negative_control.py).

## Proof outline exposed to reviewers

The algorithm’s argmin makes its one-step cost equal to a Bellman value minus
the next predicted potential. Summing telescopes the potentials. Applying the
same Bellman minimum to the offline path yields a lower bound on `OPT`. The
difference between the per-step maximum used by `ALG` and minimum used by
`OPT` is exactly the span seminorm. The exact-rational certificate adds those
three normalized premises with weight one and obtains the target coefficient
vector.

## Limitations and deviations

This page verifies Theorem 3.1 only. It does not claim that the separate
learnability and robustness theorems are formalized. The former 80 finite traces
remain regression evidence but are not the basis of this verdict.
