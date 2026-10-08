# Reproduction verification

Date: 5 October 2026.

Public summary replay: PASS in the local package. Recomputed 64 source-panel rows and 704 numeric summary cells; submitted Table 3 has 48 matched data cells. These checks derive summary arithmetic, not individual GDP measurements. Public-mode intervals are read from the frozen aggregate interval table.

Clean extracted-ZIP verification: PASS. A new directory containing only the public ZIP members reproduced the same summaries and submitted Table 3 using a fresh virtual environment with the pinned requirements installed separately. This is public-only summary reproduction, not an independent raw-data reconstruction. The final archive is tested again after this report is included; its outer hash is recorded outside the ZIP to avoid a circular fingerprint.

Separately supplied statistical-input refit: PASS locally. The public runner used the four hash-matched retained P1-P4 analysis files, verified 338 model-metric and historical-invariance checks, and matched 108 point/interval values from 9,999 complete-province-history refit draws (seed 20261002). These processed inputs are not bundled. Their successful local use does not establish public access or provider redistribution rights. No raw GDP source certification was rerun by this test.

The runner performs no download, raw-source certification or filling. It reports NOT_RUN_RESTRICTED_INPUTS_NOT_INCLUDED when only public files are used. Integrity-check failure and input absence are not converted into model success.
