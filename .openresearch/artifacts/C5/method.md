# C5 four-route method

1. **Source-artifact route.** Hash all four embedded PNGs and compare the
   numerical prose with the visible plots. This tests internal consistency but
   is circular and cannot verify an experiment.
2. **Full GHCN-input route.** Download the official Central Park station CSV
   with an explicit User-Agent; hash it; reconstruct all 153 named calendar
   years; audit 365-day completeness, missing precipitation, and rain-threshold
   sensitivity at raw thresholds 0/10/25 tenths of a millimeter. This
   reconstructs inputs but cannot select an unreleased PPP
   policy.
3. **Citi Bike route.** Resolve the official S3 object manifest for all named
   years and audit every decision needed before the dual/WFA/DC computation.
   The trip archives are not downloaded because their size cannot resolve the
   missing algorithm semantics; a guessed implementation would be a proxy.
4. **Mandatory falsification route.** Restate the exact joint claim and seek a
   contradiction using source figures, all named GHCN inputs, and the complete
   official Citi Bike manifest. Alternative choices are not valid
   counterexamples because they violate the unreleased exact contract.

Fixed command: `uv run --frozen python repro/src/run_publication_gate.py`.
Compute plan: estimated two cores and uncertain network runtime; Hugging Face
`cpu-upgrade`, CPU only. Seeds: none.
