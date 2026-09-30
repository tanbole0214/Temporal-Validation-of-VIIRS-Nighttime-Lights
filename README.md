# VIIRS temporal validation: extension through 2024

The Scientific Reports temporal extension, prepared on 30 September 2026, is distributed as a versioned [GitHub release](https://github.com/tanbole0214/Temporal-Validation-of-VIIRS-Nighttime-Lights/releases/tag/viirs-2024-20260930). Download its PUBLIC_UPLOAD_READY ZIP; the automatic Source code archives contain only the repository tree, not the statistical package.

After extraction, enter `extensions/viirs_2013_2024_20260930/` and follow `README_TEMPORAL_EXTENSION.md`: install the pinned requirements, then run `python run_extension.py --check` and `python run_extension.py --reproduce`. The package includes derived inputs, the 2014–2024 panel, predictions, table-source CSVs, eight SVGs, provenance and SHA-256 manifests. Independent reproduction matched 38 CSVs numerically and eight SVGs byte for byte. Raw external imagery/documents and manuscript DOCX files are not redistributed.

New-year official GDP coverage is 148/148/156 of 296 cities in 2022/2023/2024; no missing GDP is imputed, and no verified common 2025 analysis is included. This extends the temporal evidence only; it does not claim to rerun all historical spatial/ranking/moderator tests.

**Historical scope:** The unchanged text below describes the earlier IJDE archive. Some directories it references were not deposited in the original tracked tree. Its former GDP gate, Figure 1 caveat and deposit wording are historical, not statements about the new release. Use the new release's own runner and manifests for the 2024 extension.

---

# Replication archive for the IJDE manuscript


**Manuscript:** *From Spatial Fit to Temporal Transfer: Task-Matched Validation of VIIRS Nighttime Lights for Prefecture-Level GDP Growth in China*. This archive is bound by SHA-256 to the Round 16 main and supplementary manuscripts identified in `provenance/manuscript_binding.json`. It contains analysis-ready prefecture-year data, source registries, executable statistical code, archived output tables, and the exact artwork embedded in those documents. It has not been deposited in a public repository and has no assigned DOI.


## What can be reproduced without downloading raw products


The included panel and light aggregates let a reviewer rerun the rolling temporal validation, B0–B3 benchmarks, conditional M0/M1 comparisons, province-block bootstrap, Moran tests on frozen spatial weights, Conley sensitivity, growth-extreme recovery, model-form checks, AR(1) benchmark, exploratory heterogeneity, forward-calibration coefficients, strict balanced-sample analysis, and the 2017 evaluation-fold influence analysis. The primary continuous pre-COVID target years are 2015–2019; conditional tests begin in 2016. The 2020–2021 outcomes are separate temporal stress tests, not primary folds. The analysis universe is 296 harmonized prefectures across 31 mainland provinces; Sansha is excluded for missing certifiable GDP growth.


The raw annual EOG and NASA rasters, official statistical yearbook pages, and third-party GeoJSON boundaries are **not** bundled. The archive includes their product/file/source registries, exact file names, URLs where recorded, source tiers, and hashes of source files where available. See `EXTERNAL_DATA.md`. Frozen geometry metadata and Queen/4NN edge lists are included, so statistical spatial diagnostics run without boundary GeoJSON. Re-rendering choropleth maps from scratch requires the boundary files; the exact final map artwork is included under `figures/manuscript_embedded/`. The original raw-raster extraction was audited in the study but is not rerun by this package.


## Run


Use Python 3.11 or newer. Install `requirements.txt` into a clean virtual environment and from the archive root run:


```bash
python run_replication.py --check
python run_replication.py --full
```


`--check` verifies packaged input fingerprints, frozen output tables, counts, and key numeric invariants without changing research files. `--full` executes the extended forward and geographic analyses, nine identification-closure stages, exploratory heterogeneity, and Round 14 sensitivity analysis. It stops on the first failed stage, then compares regenerated numeric outputs with the immutable copies in `reference_results/`; run time depends especially on 9,999-draw bootstrap/permutation steps. Generated output files inside the working copy are overwritten. Run on a copy of the archive if preservation of the original byte-for-byte files is important. `--full` never downloads external data.


## Key file groups


- `temporal_extension_2013_2021/07_panel/`: 2014–2021 analysis panel; certified GDP and common-product flags.
- `temporal_extension_2013_2021/05_ntl_processed/`: 2013–2021 EOG V2.1 and Black Marble VNP46A4 Collection 2 prefecture aggregates.
- `temporal_extension_2013_2021/08_analysis/`: frozen rolling predictions and primary descriptive/spatial outputs.
- `round4_ijde_identification_closure/`: nested conditional prediction code, tests, output tables, and audit rows.
- `round10b_ijde/branch_b/`: exploratory applicability moderators and estimates. Do not interpret these as identified thresholds or causal effects.
- `round14_ijde/`: forward calibration, 272-prefecture strict balanced sample, and 2017 evaluation influence outputs.
- `reference_results/`: immutable reference copies used by the packaged numerical comparator.
- `figures/manuscript_embedded/`: verbatim media extracted from the two bound Word files; `provenance/manuscript_binding.json` records each embedded media checksum and all table-cell transcriptions.
- `RESULTS_INDEX.csv`: every main and supplementary figure/table linked to data and code.


### Figure 1 version caveat


The Round 16 Word file still embeds the prior Figure 1 raster and its prior caption. The later clarified, editable Figure 1 is supplied under `figures/updated_figure1_not_yet_in_manuscript/`, **not** represented as already embedded or caption-synchronized. Before submission, replace the manuscript image and update the caption/text to match the new diagram. Other manuscript-embedded media are copied verbatim, not redrawn in this archive.


## Statistical contract


Annual real-GDP growth is the official reported percentage transformed as `ln(1 + g/100)`. Annual light change is the log change in a fixed-support city radiance sum. The target-year GDP outcome is excluded from calibration and historical benchmarks; target-year light is observed. Stand-alone light mappings are fitted using only prior GDP years. The conditional incremental test compares an intercept-recalibrated historical M0 with that same benchmark plus light M1; comparison with the unrecalibrated raw historical benchmark answers a different question. Random seeds and 9,999 repetitions are fixed in the original code. The 2022–2024 extension did not clear its GDP certification gate and is not included as evidence or silently appended here.


`DATA_AVAILABILITY_FOR_SUBMISSION.md` contains a statement for the manuscript, with repository location deliberately left unspecified until an actual deposit or journal upload is made.


For a record of path-only code changes and independently rerun checks, see `CODE_ADAPTATIONS.md` and `REPRODUCTION_QA.md`. The included candidate Figure 1 PPTX has anonymized author metadata; its editable slide objects are unchanged from the working original.

