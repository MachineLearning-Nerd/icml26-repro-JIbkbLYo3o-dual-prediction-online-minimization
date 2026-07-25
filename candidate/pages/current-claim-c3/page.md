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

The independent cone checker visited 1,364 normalized integer points and
recovered sharp factor `2`. Parametric primal ratios shown in the raw output
are `2,3,6,18,102` for `N=1,2,5,17,101`; the proof covers every positive
integer `N`. Run `f4893104-c0c9-4e01-bb31-1699b469f795`, Git
`2ea21d42e6c25dcf2866c7e056254f3c8d4b49f7`, local estimated one core,
runtime 0.616 seconds.

[Contract](../../evidence/C3/claim_contract.json) ·
[source audit](../../evidence/C3/source_audit.md) ·
[method](../../evidence/C3/method.md) ·
[evaluation record](../../evidence/C3/EVAL.md) ·
[raw result](../../evidence/runs/C1-C3-C6-theory.json) ·
[verifier](../../repro/src/verify_remaining_theory.py) ·
[independent checker](../../repro/src/check_remaining_theory_independent.py) ·
[control](../../repro/src/run_remaining_theory_negative_controls.py)

Command: `uv run --frozen python repro/src/run_publication_gate.py`. Seeds:
none. Expected compute: one core, under five minutes.

Limitation: the appendix's undefined `2 alpha` notation prevents treating that
restatement literally; this verdict uses Algorithm 2 and the main-text
`2 beta` quantifier.
