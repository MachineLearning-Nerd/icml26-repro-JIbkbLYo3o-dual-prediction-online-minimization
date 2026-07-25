# C3 source audit

The theorem is `lem:stabilityresult`, `main.tex:461-464`; its proof is
`main.tex:976-986`. The primal counterfamily is `main.tex:763-770`.
The retrieved source SHA-256 is
`364d1b1dabc7c09bce0839e214580e1beb08d78c2de7bdf2edd61fada706077c`.

The main theorem correctly states `2 beta`. The appendix restatement at line
977 says `2 alpha` even though it immediately defines `beta`; `alpha` is not
defined in that lemma. The current contract treats this as a typographical
error and tests the main theorem's `2 beta` statement.

For the primal family, `X=U` has the unique universal-set optimum of cost
`N+1/2`, while `X'=U\{0}` has the unique `N`-singleton optimum. The solution
vectors differ in `N+1` coordinates for a symmetric difference of one.
