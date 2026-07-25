# Claim 1 — laminar bound, exact derivation

**Candidate verdict: VERIFIED.** For every finite fractional laminar set-cover
instance, prediction, optimal dual, and `0<alpha<1`, the reconstructed charging
proof derives

`E[ALG] <= OPT/alpha + over/alpha + R*under/(1-alpha)`.

With `alpha=1/(1+epsilon)`, this is exactly
`(1+epsilon)OPT + (1+epsilon)over + R(1+epsilon)under/epsilon`, implying the
paper's fixed-epsilon big-O statement.

| Evidence | Result |
|---|---|
| Exact source | `lem:lemdualboundlaminar`, source SHA `364d...077c` |
| Laminar charging | Maximal purchased sets proved pairwise disjoint |
| Type-2 charging | Nested redundancy removed from the optimal cover |
| Independent checker | PASS, five exact rational epsilon values |
| Negative control | Missing `1/(1-alpha)` factor rejected |
| Command | `uv run --frozen python repro/src/run_publication_gate.py` |
| Seeds | None; deterministic proof |
| Run / Git | `f4893104-c0c9-4e01-bb31-1699b469f795` / `2ea21d42e6c25dcf2866c7e056254f3c8d4b49f7` |
| CPU / runtime | Local, estimated 1 core, 8 visible logical CPUs, 0.616 s |

[Contract](../../evidence/C1/claim_contract.json) ·
[source audit](../../evidence/C1/source_audit.md) ·
[method](../../evidence/C1/method.md) ·
[evaluation record](../../evidence/C1/EVAL.md) ·
[raw result](../../evidence/runs/C1-C3-C6-theory.json) ·
[verifier](../../repro/src/verify_remaining_theory.py) ·
[independent checker](../../repro/src/check_remaining_theory_independent.py) ·
[control](../../repro/src/run_remaining_theory_negative_controls.py)

Limitation: the separate randomized rounding lemma is not re-formalized.
Historical finite bound cells are regression evidence only.
