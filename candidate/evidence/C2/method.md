# Claim 2 method

The proof is checked in two layers.

1. A structural checker validates the one-step argmin/competitor obligations
   and a two-case induction certificate (base horizon one; generic extension)
   for telescoping the predicted potentials along any path.
2. An exact-rational linear kernel verifies that the algorithm upper bound, the
   offline-optimum lower bound, and the definition of `eta` combine with
   nonnegative weights to the target inequality `ALG-OPT-ETA<=0`.

The independent checker does not import the primary kernel. It reconstructs the
coefficient sum with `fractions.Fraction` and separately checks the induction
step. The negative control changes the `ETA` coefficient in the goal from `-1`
to `-1/2`; both checkers must reject that mutation.

No sample size, horizon, tolerance, or random family is selected from the
theorem formula. All arithmetic is exact.
