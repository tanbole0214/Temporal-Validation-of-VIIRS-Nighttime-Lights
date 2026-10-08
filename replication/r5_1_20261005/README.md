# Scientific Reports R5.1 public replication materials

This archive supports the R5/R5.1 temporal validation and mixed-source sensitivity results for 296 Chinese prefectures. It contains readable statistical code, aggregate numerical results, the submitted Table 3 source, input fingerprints and access documentation. It deliberately does not contain restricted row-level observations or acquired source publications.

## Public reproduction

Install the pinned requirements in a clean Python environment, then run:

```
python -m pip install -r requirements.txt
python run_replication.py --check
python run_replication.py --reproduce-summaries --output generated
```

These commands verify package fingerprints, recompute 64 source-panel metric rows from archived annual summary statistics, and reconstruct the submitted Table 3. Confidence intervals are carried through from frozen aggregate results in public-only mode; bootstrap intervals are not estimated again without statistical inputs.

## Statistical refitting with separate inputs

```
python run_replication.py --refit --inputs /path/to/lawfully-obtained-inputs --bootstrap --output generated_private
```

This mode requires all four exact analysis-ready files listed in `RESTRICTED_INPUT_SHA256.csv`. It checks their hashes, refits the unchanged recursive estimators, treats P3 as an official-target subset of P1 fits, and reruns 9,999 whole-province-history bootstrap draws. It does not download or certify raw source publications. It stops when an input is missing or differs from the frozen version. The public files alone cannot perform this mode.

The absence of row-level inputs is an explicit access boundary, not a hidden code defect, scrambled specification or claimed complete public replication. No public-only command should be described as an independent row-level empirical refit. Historical non-temporal/spatial diagnostics are not rerun by this R5.1 runner.

## GDP source provenance

The underlying prefecture GDP source data are the *China City Statistical Yearbook* (中国城市统计年鉴; relevant editions through 2025) and municipal/provincial statistical-bureau publications. A compiled workbook was used only as an intermediary extraction/harmonization layer for part of the 2022-2024 extension and is not treated as an original statistical source. Official observations independently retrieved from the upstream statistical publications take precedence whenever available.

Contact the corresponding author, Zhong Li, at lizhong@caas.cn for additional author-controlled processing and verification documentation. See `DATA_ACCESS.md`, `EXTERNAL_DATA.md` and `PUBLIC_PRIVATE_BOUNDARY.md`.

The local statistical tests are described in `REPRODUCTION_QA.md`. `PACKAGE_SHA256.csv` inventories package files except itself and generated outputs.
