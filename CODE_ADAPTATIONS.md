# Portable-code adaptation log

The calculations and fixed statistical choices come from the frozen source scripts. The archive changes only file access and delivery mechanics:

1. Removed references to a private prompt and earlier local manuscript files from the Round 4 input inventory. The archive instead binds the current anonymized Round 16 documents by SHA-256 in `provenance/manuscript_binding.json`.
2. Redirected the Round 14 source-document hash check to that binding record. The original document files themselves are not copied into the data archive.
3. Added a minimal `forward_transfer_geography_extension/code/config.py` with the frozen B0–B3 and Moran constants needed by the included geographic and hotspot routines; the earlier workspace-wide configuration referenced unrelated project files and private paths.
4. Made the Round 4 raw-error **map rendering** conditional on third-party GeoJSON being present. Its correlations, Moran statistics, tabular outputs and bootstrap still run from the included accepted centroids and spatial-weight edges. The bound manuscript map SVGs remain available in `figures/manuscript_embedded/`.
5. Omitted the original Node/workbook wrapper and its absolute runtime locations. `run_replication.py` executes the Python statistical stages directly, in documented order, with the current interpreter. No research coefficient, sample, seed, comparison, or threshold was changed in this portability pass.

This is an offline *analysis-ready-data-to-results* replication archive. It does not assert that a reader can recreate certified GDP cells or pixel aggregates from raw third-party files without separately obtaining and checking those files.
