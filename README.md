# Temporal Validation of VIIRS Nighttime Lights

## Current manuscript status

**Current Scientific Reports manuscript title**

> Forward validation reveals temporal and processing-product dependence of VIIRS nighttime lights for prefecture GDP growth in China

The current manuscript is the **R5.1 consolidated submission version**. Its main empirical hierarchy is:

1. strong spatial alignment does not establish forward annual-growth validity;
2. forward validity is not automatically portable across time;
3. under common geographic and GDP support, measured incremental value can depend materially on the VIIRS processing product;
4. outcome-source validity is audited separately from geographic support.

The 2022–2024 extension uses the fixed 296-prefecture universe. The mixed-source GDP layer was independently audited and classified **GDP-B: usable with bounded qualifications**. In the verified audit, 98 of 105 predeclared workbook-only observations were resolved; seven remained unresolved. Reasonable GDP source substitutions did not remove the pooled EOG-versus-Black-Marble processing-product disagreement.

## Important replication-status note

The existing public GitHub release:

- [viirs-2024-20260930](https://github.com/tanbole0214/Temporal-Validation-of-VIIRS-Nighttime-Lights/releases/tag/viirs-2024-20260930)

is a **verified earlier temporal-extension package** prepared on 30 September 2026. It is retained for provenance and historical reproducibility, but **it does not reproduce the final R5/R5.1 manuscript in full**. In particular, it predates the later 296-prefecture mixed-source extension, GDP-source audit, source-panel sensitivity, paired EOG-versus-Black-Marble loss contrasts, and R5 extension uncertainty.

Do not cite that earlier release as the complete replication package for the R5.1 manuscript.

## R5.1 public-replication status

The R5/R5.1 project contains a public/private separation because some third-party source material and row-level files have unresolved redistribution rights.

A rights-cleared public package is being prepared for submission. It is expected to contain only materials cleared for public redistribution, such as:

- analysis and verification code;
- derived summary tables where redistribution is permitted;
- table/figure source files where permitted;
- source manifests and hashes;
- public source URLs and reconstruction instructions;
- environment/package specifications;
- numerical and document QA reports;
- reproducibility/check scripts.

Restricted third-party workbooks, acquired source publications, and restricted row-level material will not be uploaded unless redistribution rights are established.

The final Scientific Reports submission should use the exact release/commit identifier of the R5.1 public package once that package has been deposited.

## Historical package

The tracked repository files below primarily document the earlier 2013–2021 / September-2026 replication state. They remain available for provenance:

- `run_replication.py`
- `verify_package.py`
- `DATA_DICTIONARY.csv`
- `RESULTS_INDEX.csv`
- `PACKAGE_SHA256.csv`
- `EXTERNAL_DATA.md`
- `REPRODUCTION_QA.md`
- `CODE_ADAPTATIONS.md`

These files should be interpreted as historical replication materials unless explicitly superseded by the forthcoming R5.1 package.

## Data and code availability

See `DATA_AVAILABILITY_FOR_SUBMISSION.md` and `SCIENTIFIC_REPORTS_R5_1_SUBMISSION_STATUS.md`.

The project does not infer a redistribution licence merely because a source is publicly accessible. Public and restricted materials are separated accordingly.
