# Evaluator-blind review — pass 1

Scope: a fresh copy of the candidate artifact, opened only from `README.md`
with the evaluator rubric. Repository knowledge was not used to locate files.

## Files opened

- `README.md`
- `pages/current-claim-c1/page.md` through
  `pages/current-claim-c6/page.md`
- the contract, source-audit, method, raw-run, verifier, checker, and control
  links exposed by those six pages
- `report.md`
- `logbook.json`

## Missing conclusions:

- The fixed command named `repro/src/run_publication_gate.py`, but the first
  package draft exposed code under `code/src`.
- The source hash was visible, but the exact source payload was not available
  through the text-only candidate.
- Several current pages did not directly link their `EVAL.md` records.
- The illustrated report was not linked from the canonical README.

## Fixes applied

The executable tree now uses `repro/`; the exact source tar is included as
base64 text with a hash-checked loader; every claim links its evaluation record;
and the report, notebook, environment, release audit, and historical baseline
are linked directly from `README.md`.
