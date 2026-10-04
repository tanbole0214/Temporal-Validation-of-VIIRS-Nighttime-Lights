# Temporal Validation of VIIRS Nighttime Lights

## Current Scientific Reports R5.1 materials

Manuscript: Forward validation reveals temporal and processing-product dependence of VIIRS nighttime lights for prefecture GDP growth in China.

The R5.1 public code and aggregate-results snapshot is in [replication/r5_1_20261005/](replication/r5_1_20261005/). Its designated release is [sr-r5.1-20261005](https://github.com/tanbole0214/Temporal-Validation-of-VIIRS-Nighttime-Lights/releases/tag/sr-r5.1-20261005); the release page is the publication record, and the exact commit is recorded there. The downloadable author-assembled archive is `Scientific_Reports_R5_1_Public_Code_and_Summary_Replication_20261005.zip` with SHA-256 `2b947309a2b157fd9cd1ffdb12c49bebf78753c79792dbcdffe6eda09d897081`.

This is a public statistical-code and summary-reproduction deposit, not a complete microdata or raw-source release. In a clean extracted archive and a fresh virtual environment, the public runner reproduces 64 metric rows (704 arithmetic checks) and all 48 data cells in the submitted Table 3. Separately, the same runner with retained, hash-bound inputs passed 338 model/invariance checks and 108 bootstrap point/interval checks. Public-only use does not refit restricted city-level models or re-estimate intervals.

The extension retains 296 prefectures. Independent verification resolved 98 of 105 predeclared observations; seven remain unresolved. The verified-enhanced panel contains 590 official outcomes and 298 compiled outcomes. The 108 newly inspected official outcomes are not the sampled verification completion count. The qualified GDP-B classification and fragile most-recent-history EOG result remain unchanged.

## Data access boundary

The compiled workbook provider is Markdata (马克集数; macrodatas.cn). Workbook redistribution and restricted derivative access require provider permissions; none are inferred here. Row-level panels, predictions/losses, raw publications, detailed verification records, raw rasters and boundary geometries are not public. Contact Zhong Li at lizhong@caas.cn for author-controlled documentation and lawful input access enquiries; a request channel is not an unconditional reviewer-access guarantee.

## Historical materials

Root-level scripts and the [viirs-2024-20260930 release](https://github.com/tanbole0214/Temporal-Validation-of-VIIRS-Nighttime-Lights/releases/tag/viirs-2024-20260930) document the earlier temporal-extension state. They are retained without alteration and must not be cited as complete R5.1 replication. Use the versioned subdirectory above for R5.1 summary reproduction.

See DATA_AVAILABILITY_FOR_SUBMISSION.md and SCIENTIFIC_REPORTS_R5_1_SUBMISSION_STATUS.md. No new blanket code or third-party data licence is assigned by this deposit.
