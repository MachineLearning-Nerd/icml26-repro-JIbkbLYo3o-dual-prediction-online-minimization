- Previous live judged score: `5/12`
- Conservative projected score range after the proposed change: `8/12–10/12`
- Best-supported possible new score: **`10/12` forecast, not a judge result**

# Final release report

The current total score remains `5/12`. The existing Space was updated at
[`1d96f24`](https://huggingface.co/spaces/DineshAI/JIbkbLYo3o/commit/1d96f24b04bbe79b280f608b350e0f6e01d984c2)
and is awaiting the live evaluator. Nothing in this report is a new judge
result.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| C1 | 1 | 2 | HIGH | VERIFIED | Exact laminar charging and epsilon-substitution certificate; rounding lemma remains source-stated |
| C2 | 1 | 2 | HIGH | VERIFIED | Exact-rational Farkas certificate and independent arbitrary-horizon reconstruction |
| C3 | 1 | 2 | MEDIUM | VERIFIED | Stability induction and unbounded primal family; appendix alpha/beta typo is disclosed |
| C4 | 1 | 2 | HIGH | VERIFIED | Exact deterministic Wei combiner reaches ratio 61.152 at k=64; no-change control ratio 1 |
| C5 | 0 | 0 | LOW | BLOCKED | Four routes complete; author code, processed inputs, initial states, ties, and seeds remain unavailable |
| C6 | 1 | 2 | HIGH | VERIFIED | Corrected request-before-removal H_m adversary; printed H_m-1 construction is rejected |

## Release identity

| Field | Value |
|---|---|
| Baseline score | `5/12` |
| Judged HF Head | `ca024e6adeaf755dd21a0b28b642d5a85d6df733` |
| Judge Head | `ca024e6adeaf755dd21a0b28b642d5a85d6df733` |
| Winning scientific candidate | `orx/evaluator-visible-release-candidate@7f93a23595d1513eccc727c9a611a5d489734988` |
| Winning release-hardening branch | `orx/post-publication-snapshot-traversal-hardening@6e1657a0c6c4d756f59922dbcef943fc0680a80b` |
| Formal release run | `1880f3fc-b0b9-4b2a-a701-43204adcca9d` |
| Published Space | `DineshAI/JIbkbLYo3o@1d96f24b04bbe79b280f608b350e0f6e01d984c2` |
| GitHub `main` checked SHA | `6e1657a0c6c4d756f59922dbcef943fc0680a80b` |

C1, C2, C3, C4, and C6 changed from finite toy evidence to current exact or
parametric verification. C5 changed from unattempted to a four-route audit but
remains `BLOCKED`: a proxy pipeline cannot test the exact reported experiment.

## Experiment tree

The tree is a single descending research line with small corrective steps:
historical baseline → C2 proof → C1/C3/C6 proofs → exact C4 combiner → C5
four-route audit → corrected GHCN units → evaluator-visible release → published
snapshot hardening. The exact node and run IDs are in
[`experiment-tree.json`](../../candidate/evidence/runs/experiment-tree.json)
and the final two node descriptions in OpenResearch.

The final cumulative run reported C1/C2/C3/C4/C6 `VERIFIED`, C5 `BLOCKED`,
11/11 tests, every independent checker `PASS`, and every negative control
`REJECTED_AS_INTENDED`. It used HF `cpu-upgrade`, estimated 2 cores, detected
64 logical CPUs, and completed the Python gate in 4.584 seconds.

## Evidence and visibility

- Canonical Space entrypoint: `README.md`.
- Reachable from that entrypoint: 67 files; zero broken links.
- Judged file subset: 22/22 old paths remain present.
- Protected historical hashes: 19/19 unchanged. Only `README.md`,
  `logbook.json`, and `pages/index.md` changed to put current evidence first.
- Current claim pages: all six expose the contract, exact source scope,
  executable verifier, raw JSON, checker, control, command, environment,
  run/Git identity, seeds, CPU/runtime, and limitations.
- Evaluator-blind review: one repair pass followed by a clean pass.
- Secret scan: zero hits.
- Upload: exactly 88 UTF-8 text files; no new binary upload.
- Manifest: 87 payload hashes plus the manifest itself, payload-tree SHA-256
  `a4be79aa99e289ffdf1ebce0f44ea9cbed5572cd53cd7e91786dc17eaf11a7ea`.

The exact [upload allowlist](../../candidate/release/upload-allowlist.txt) and
[SHA-256 manifest](../../candidate/release/sha256-manifest.json) are committed.
A fresh download of the published revision reproduced the full visibility
audit and all 87 manifest-listed hashes.

## Commands

The formal command was fixed once and inherited unchanged:

```text
uv run --frozen python repro/src/run_publication_gate.py
```

Research and release orchestration used:

```text
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx runs b3c87edd-c8c3-4f7d-9496-3debcdf11e9c
orx exp run <local-node> --backend local
orx exp run <hf-node> --backend hf --flavor cpu-upgrade --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim
orx exp wait <experiment-id> --timeout 480
orx logs <run-id>
uv run --frozen python repro/src/verify_release_candidate.py
marimo check --strict notebooks/dual_prediction_reproduction.py
hf download DineshAI/JIbkbLYo3o --repo-type space --revision 1d96f24b04bbe79b280f608b350e0f6e01d984c2
git push origin HEAD:main
git ls-remote origin refs/heads/main
```

Publication used one Hugging Face `create_commit` HTTP API call over the exact
text staging directory. It targeted only the existing
`DineshAI/JIbkbLYo3o` Space; no Space was created and no delete operation was
issued.

## Compute and cost

All local formal jobs used at most one CPU core and had 5-second orchestrator
durations; incremental local cost was `$0`. Seven HF `cpu-upgrade` jobs
totaled 151 seconds of recorded job duration, including three environment or
packaging diagnostics. The official rate is
[$0.0005/minute ($0.03/hour)](https://huggingface.co/docs/hub/jobs-pricing).
That is about `$0.00126` if prorated by recorded seconds, or at most `$0.0035`
if each sub-minute job is billed as a full minute. No GPU was used.

## Final assessment

The conservative projected total is `8/12–10/12`; the best-supported possible
total is `10/12`. C5 remains the only `BLOCKED` claim. It requires the author
experiment revision, processed PPP and daily Citi Bike instances with hashes,
initial configurations, tie rules, and seeds. The exact publication action has
already been performed; the campaign is now awaiting the live judge, and the
live score remains `5/12`.
