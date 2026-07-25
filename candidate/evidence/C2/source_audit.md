# Claim 2 source audit

Source archive: arXiv `2606.05380`, SHA-256
`364d1b1dabc7c09bce0839e214580e1beb08d78c2de7bdf2edd61fada706077c`,
retrieved 2026-07-25 with the browser User-Agent recorded in the startup
snapshot.

The exact anchor is `main.tex` label `th:MTSBoundForBellmanError` in the
“Algorithm with Dual Predictions” subsection. The algorithm receives `c_t` and
`w_hat_t`, then chooses any minimizer of
`d(s_{t-1},s)+c_t(s)+w_hat_t(s)`. The paper explicitly assumes
`w_hat_T=0`. It defines `eta_t` as the span seminorm of
`B^{c_t}(w_hat_t)-w_hat_{t-1}` and `eta` as their sum.

The theorem is written as a `(1+eta/OPT)` competitive ratio. Division requires
`OPT>0`; the proof establishes the stronger boundary-safe statement
`ALG<=OPT+eta`, which is the contract checked here. No Lipschitz assumption on
the predictions is used by this theorem.

The quantifier is universal over finite MTS instances and prediction sequences.
Finite traces are therefore corroboration only and are not used as the proof.
