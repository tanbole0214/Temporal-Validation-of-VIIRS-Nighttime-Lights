# Temporal Validation of VIIRS Nighttime Lights

## Current Scientific Reports R5.1 materials

Manuscript: Assessing the incremental value of VIIRS nighttime lights for prefecture-level GDP growth in China.

The R5.1 public code and aggregate-results snapshot is in [replication/r5_1_20261005/](replication/r5_1_20261005/). The 2026-10-13 correction normalizes text files to LF and regenerates the checksum manifest after documentation edits. Statistical code and aggregate estimates are unchanged. The earlier release `sr-r5.1-20261005` remains a historical snapshot, not the corrected deposit.

This is a public statistical-code and summary-reproduction deposit, not a complete microdata or raw-source release. In a clean extracted archive and a fresh virtual environment, the public runner reproduces 64 metric rows (704 arithmetic checks) and all 48 data cells in the submitted Table 3. Separately, the same runner with retained, hash-bound inputs passed 338 model/invariance checks and 108 bootstrap point/interval checks. Public-only use does not refit restricted city-level models or re-estimate intervals.

The extension retains 296 prefectures. Independent verification resolved 98 of 105 predeclared observations; seven remain unresolved. The verified-enhanced panel contains 590 official outcomes and 298 compiled outcomes. The 108 newly inspected official outcomes are not the sampled verification completion count. The qualified GDP-B classification and fragile most-recent-history EOG result remain unchanged.

## GDP source provenance and access boundary

The underlying prefecture GDP source data are the *China City Statistical Yearbook* (中国城市统计年鉴; relevant editions through 2025) and municipal/provincial statistical-bureau publications. A compiled workbook was used only as an intermediary extraction and harmonization layer for part of the 2022-2024 extension and is not treated as an original statistical source. Official observations independently retrieved from the upstream statistical publications take precedence whenever available.

The direct provider of the compiled workbook is Markdata, https://www.macrodatas.cn/. Its GDP-growth product is https://s.macrodatas.cn/article/indicator/city-e895d581e72b4d-gdpzengsu-b52ac5 (indicator 108252). This intermediary provider is distinct from the underlying official statistical producers. A later portal download is not guaranteed to match the retained workbook.

The R5.1 public layer excludes the intermediary workbook, city-year GDP panels, predictions/losses, acquired publications, detailed verification records, raw rasters and boundary geometries. The provider's membership terms (https://s.macrodatas.cn/membership-agreement; inspected 2026-10-13) restrict third-party provision and require written permission for overseas use or provision. No permission for journal-review or post-publication redistribution has been established by this deposit. Contact Zhong Li at lizhong@caas.cn for author-controlled documentation. A subscription or request to the authors does not by itself authorize sharing restricted files. See the versioned DATA_ACCESS.md for the access boundary.

## Historical materials

Root-level scripts and the [viirs-2024-20260930 release](https://github.com/tanbole0214/Temporal-Validation-of-VIIRS-Nighttime-Lights/releases/tag/viirs-2024-20260930) document the earlier temporal-extension state. They are retained without alteration and must not be cited as complete R5.1 replication. Use the versioned subdirectory above for R5.1 summary reproduction.

See DATA_AVAILABILITY_FOR_SUBMISSION.md and SCIENTIFIC_REPORTS_R5_1_SUBMISSION_STATUS.md. No new blanket code or third-party data licence is assigned by this deposit.

## Environment

Use Python 3.11 or later; tests used Python 3.12.14. Statistical code and empirical results are unchanged by the source-provenance documentation correction.
