# Reproducing Learning-Augmented Online Minimization with Dual Predictions

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-JIbkbLYo3o-dual-prediction-online-minimization/blob/main/notebooks/dual_prediction_reproduction.py)

This CPU-only campaign tests all six claims selected by the live evaluator for
[arXiv 2606.05380](https://arxiv.org/abs/2606.05380). Five finite spot checks
were replaced by exact symbolic certificates or a direct implementation of the
named caching algorithm. The unreleased parking-permit and bike-share
experiment remains `BLOCKED` after four distinct research routes.

The current live score is still **5/12**. The candidate forecast is
**8/12–10/12**, with **10/12** the best-supported possible score—not a judge
result.

| Evidence | Paper result | Observed result | Assessment |
|---|---|---|---|
| C1 laminar cover | `(1+epsilon) OPT + O(R eta/epsilon)` | exact charging and substitution certificate | VERIFIED candidate |
| C2 MTS | `ALG <= OPT + eta` | exact-rational arbitrary-horizon certificate | VERIFIED candidate |
| C3 stability | dual `O(symmetric difference)`; primal unbounded | induction certificate and unbounded parametric family | VERIFIED candidate |
| C4 caching | one event error can collapse the guarantee | ratio `61.152` at `k=64`; last-three minimum `ratio/k=0.955` | VERIFIED candidate |
| C5 real data | PPP `1.8x–4.4x` better at `K=9`; bike-share advantage | no faithful number: essential experiment semantics are absent | BLOCKED |
| C6 set cover | perfect predictions cannot beat `H_m` | corrected assumption-preserving `H_m` adversary; printed order gives `H_m-1` | VERIFIED candidate |

The C4 sweep uses `k=4,8,16,32,64` and the exact deterministic Wei combiner.
C5 does not substitute synthetic data: its audit reconstructs the named GHCN
input and official 19.20 GB Citi Bike archive manifest, then records why those
inputs do not identify the authors' algorithms, preprocessing, initial states,
tie rules, or seeds. All formal runs use Python 3.12, one repository `.venv`,
the committed `uv.lock`, and CPU only.

- [Illustrated technical report](reports/dual-prediction-reproduction/report.md)
- [Self-contained marimo tutorial](notebooks/dual_prediction_reproduction.py)
- Local notebook: `marimo edit notebooks/dual_prediction_reproduction.py`

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `main` | Public report and notebook | Not run as an experiment (publication surface) | Presentation only | None |
| [`orx/exact-theory-contracts-and-proof-certificates`](https://github.com/MachineLearning-Nerd/icml26-repro-JIbkbLYo3o-dual-prediction-online-minimization/tree/orx/exact-theory-contracts-and-proof-certificates) | Exact C2 proof | `uv run --frozen python repro/src/run_publication_gate.py` | PASS | local CPU, at most 1 core |
| [`orx/remaining-universal-theory-certificates`](https://github.com/MachineLearning-Nerd/icml26-repro-JIbkbLYo3o-dual-prediction-online-minimization/tree/orx/remaining-universal-theory-certificates) | C1, C3, and C6 certificates | `uv run --frozen python repro/src/run_publication_gate.py` | PASS | local CPU, at most 1 core |
| [`orx/exact-caching-combiner-instability`](https://github.com/MachineLearning-Nerd/icml26-repro-JIbkbLYo3o-dual-prediction-online-minimization/tree/orx/exact-caching-combiner-instability) | Direct C4 algorithm and controls | `uv run --frozen python repro/src/run_publication_gate.py` | PASS | local CPU, at most 1 core |
| [`orx/correct-ghcn-unit-sensitivity`](https://github.com/MachineLearning-Nerd/icml26-repro-JIbkbLYo3o-dual-prediction-online-minimization/tree/orx/correct-ghcn-unit-sensitivity) | Corrected four-route C5 audit | `uv run --frozen python repro/src/run_publication_gate.py` | BLOCKED claim, audit PASS | Hugging Face `cpu-upgrade`, 64 visible logical CPUs |

## Reproducibility contract

The fixed command for every experiment node is:

```text
uv run --frozen python repro/src/run_publication_gate.py
```

The pinned arXiv source SHA-256 is
`364d1b1dabc7c09bce0839e214580e1beb08d78c2de7bdf2edd61fada706077c`.
Every current verifier fails closed, has an independent checker, and runs a
negative control that must be rejected. Candidate verdicts are exactly
`VERIFIED` or `BLOCKED`; no toy check is presented as full-scale evidence.
