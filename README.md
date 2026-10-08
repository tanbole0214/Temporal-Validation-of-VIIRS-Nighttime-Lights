# Temporal Validation of VIIRS Nighttime Lights

## Current Scientific Reports R5.1 materials

Manuscript: Forward validation reveals temporal and processing-product dependence of VIIRS nighttime lights for prefecture GDP growth in China.

The R5.1 public code and aggregate-results snapshot is in [replication/r5_1_20261005/](replication/r5_1_20261005/). The current submission should cite the exact repository commit containing the corrected source-provenance documentation. The earlier release `sr-r5.1-20261005` remains a historical snapshot of the same statistical code and aggregate results but predates the final source-provenance wording correction.

This is a public statistical-code and summary-reproduction deposit, not a complete microdata or raw-source release. In a clean extracted archive and a fresh virtual environment, the public runner reproduces 64 metric rows (704 arithmetic checks) and all 48 data cells in the submitted Table 3. Separately, the same runner with retained, hash-bound inputs passed 338 model/invariance checks and 108 bootstrap point/interval checks. Public-only use does not refit restricted city-level models or re-estimate intervals.

The extension retains 296 prefectures. Independent verification resolved 98 of 105 predeclared observations; seven remain unresolved. The verified-enhanced panel contains 590 official outcomes and 298 compiled outcomes. The 108 newly inspected official outcomes are not the sampled verification completion count. The qualified GDP-B classification and fragile most-recent-history EOG result remain unchanged.

## GDP source provenance and access boundary

The underlying prefecture GDP source data are the *China City Statistical Yearbook* (中国城市统计年鉴; relevant editions through 2025) and municipal/provincial statistical-bureau publications. A compiled workbook was used only as an intermediary extraction and harmonization layer for part of the 2022-2024 extension and is not treated as an original statistical source. Official observations independently retrieved from the upstream statistical publications take precedence whenever available.

The R5.1 public layer excludes the intermediary compiled workbook, city-year GDP panels, predictions/losses, acquired publications, detailed verification records, raw rasters and boundary geometries. Users seeking source-level reconstruction should consult the original yearbooks and statistical-bureau publications together with the source locators, hashes and verification documentation retained by the authors. Contact Zhong Li at lizhong@caas.cn for author-controlled processing and verification documentation.

## Historical materials

Root-level scripts and the [viirs-2024-20260930 release](https://github.com/tanbole0214/Temporal-Validation-of-VIIRS-Nighttime-Lights/releases/tag/viirs-2024-20260930) document the earlier temporal-extension state. They are retained without alteration and must not be cited as complete R5.1 replication. Use the versioned subdirectory above for R5.1 summary reproduction.

See DATA_AVAILABILITY_FOR_SUBMISSION.md and SCIENTIFIC_REPORTS_R5_1_SUBMISSION_STATUS.md. No new blanket code or third-party data licence is assigned by this deposit.

## Environment

Use Python 3.11 or later; tests used Python 3.12.14. Statistical code and empirical results are unchanged by the source-provenance documentation correction.
