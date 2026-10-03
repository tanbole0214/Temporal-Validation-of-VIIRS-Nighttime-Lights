# Scientific Reports data and code availability status

## Current status

This repository currently contains the earlier public replication materials and the verified 30 September 2026 temporal-extension release. The final **R5.1 Scientific Reports** public-replication package has **not yet been deposited** in this repository.

Accordingly, the manuscript should not yet state that all R5/R5.1 code and derived outputs are publicly archived here.

## Submission-day wording after the R5.1 public package is deposited

The exact wording should be updated with the final release tag, commit SHA, and/or DOI. A suitable structure is:

### Code availability

> Custom analysis and verification code, derived summary outputs, source manifests, reconstruction instructions, environment specifications, figure/table source files cleared for redistribution, and reproducibility checks for this study are publicly archived at the project repository: https://github.com/tanbole0214/Temporal-Validation-of-VIIRS-Nighttime-Lights [insert final R5.1 release tag/commit or DOI]. Restricted third-party inputs are excluded from the public package.

### Data availability

> The analysis uses public Earth-observation products, official statistical sources, derived prefecture-level analysis files, and a third-party compiled GDP workbook. Materials that can be redistributed are included in the public replication package at https://github.com/tanbole0214/Temporal-Validation-of-VIIRS-Nighttime-Lights [insert final R5.1 release tag/commit or DOI]. The compiled GDP workbook, acquired source documents, and certain row-level materials are not publicly redistributed because redistribution rights have not been established. Public source URLs, hashes, page/table locators, retrieval status, and reconstruction information are provided in the source manifests. Restricted materials can be made available to editors and peer reviewers within the applicable legal and data-use constraints; post-publication access to third-party sources depends on the original providers and their terms.

Only retain the reviewer-access sentence if the authors can in fact provide that access under the relevant rights/terms.

## What the public R5.1 package should contain

At minimum:

- current analysis/verification code;
- a public-share manifest;
- a private/restricted manifest that identifies but does not redistribute restricted material;
- public source manifest;
- source hashes and retrieval metadata;
- derived summary outputs cleared for redistribution;
- table/figure source files cleared for redistribution;
- exact environment/package versions;
- numerical QA;
- document/source binding or equivalent version record;
- SHA-256 inventory;
- README with one-command or clearly ordered reproduction instructions.

## What must not be uploaded without rights clearance

- the author-provided third-party GDP workbook if redistribution permission is unresolved;
- acquired official/statistical publications whose redistribution terms do not permit republication;
- restricted row-level data;
- third-party boundary or raster files when redistribution is not permitted.

Public accessibility is not treated as evidence of a redistribution licence.

## Historical release

The release `viirs-2024-20260930` remains a valid historical replication record for the earlier temporal extension, but it does not reproduce the final R5/R5.1 manuscript in full.
