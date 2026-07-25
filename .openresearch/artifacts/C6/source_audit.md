# C6 source audit

The claim and proof are `main.tex:811-901`, source SHA-256
`364d1b1dabc7c09bce0839e214580e1beb08d78c2de7bdf2edd61fada706077c`.
Its explicit scope fixes a deterministic online fractional algorithm and uses
an adaptive adversary. It does not establish a randomized-oblivious lower
bound.

There is a real arithmetic/order defect in the printed proof. It removes a
maximum-weight set before the first request, so its forced increments are
`sum_{j=2}^m 1/j = H_m-1`. The final singleton increment is then explicitly
zero. The statement “H_m-1+1” has no supporting unit increment.

The corrected classical construction requests the element supported on the
current alive set before removing a maximum-weight set. Its first request
forces unit cost; subsequent nested supports force `1/m,...,1/2`, totaling
`H_m`. The final survivor covers every request, so OPT is one. Unit dual mass
on the initial universal-support element is feasible, optimal, and identical
for every adaptive elimination order.
