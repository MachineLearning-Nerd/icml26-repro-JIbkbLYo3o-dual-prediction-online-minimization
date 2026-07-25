# Claim 3 — dual stability and primal instability

**Candidate verdict: VERIFIED** for Algorithm 2's fixed DFS dual and the
main-text `2 beta` statement.

The single-change proof cone telescopes to
`||y(X)-y(X+e)||_1 <= 2 beta`; triangle inequality over exactly
`|X delta X'|` insertions/deletions gives the universal theorem. An independent
checker exhausts the normalized cone and recovers the sharp factor two.

The primal counterfamily is parametric: for every positive integer `N`, one
changed element makes the unique optimal vector change in `N+1` coordinates.

The appendix restates the factor as `2 alpha`, although only `beta` is defined.
That typo is explicitly rejected and is not treated as evidence.

[Contract](../../.openresearch/artifacts/C3/claim_contract.json) ·
[source audit](../../.openresearch/artifacts/C3/source_audit.md) ·
[method](../../.openresearch/artifacts/C3/method.md) ·
[expected raw result](../../.openresearch/artifacts/C3/raw/expected_result.json) ·
[verifier](../../repro/src/verify_remaining_theory.py) ·
[independent checker](../../repro/src/check_remaining_theory_independent.py) ·
[control](../../repro/src/run_remaining_theory_negative_controls.py)

Command: `uv run --frozen python repro/src/run_publication_gate.py`. Seeds:
none. Expected compute: one core, under five minutes.
