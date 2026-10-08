# External data products and original statistical sources

Raw external data are not redistributed or downloaded by this package.

EOG lineage: the frozen 2013-2021 observations use Annual VIIRS Nighttime Lights VNL V2.1 (https://eogdata.mines.edu/products/vnl/). The 2022-2024 continuation is the annual VNL-derived Cloud-Optimized GeoTIFF series in OpenGeoHub Zenodo record 17294744, version v0.4 (https://doi.org/10.5281/zenodo.17294744). Only observed VIIRS years are used; backward-extrapolated 2000-2011 values are excluded. Extension growth uses adjacent years within the extension source, including its own 2021 for 2022 growth. The overlap bridge yields a net EOG factor of 1.0 on extracted aggregates. Consult manuscript Methods and Supplementary Information for support and bridge qualifications; numerical scale matching does not establish exact physical radiance equivalence.

NASA Black Marble VNP46A4 Collection 2: https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A4/ . Earthdata registration/authentication may be required. The extension uses AllAngle_Composite_Snow_Free; finite non-negative radiance; quality code 0; more than three observations; land/water codes 0/1/2/5; and a 0.50 nW cm^-2 sr^-1 background threshold. Fixed support and all_touched=True are disclosed separately from GDP timing restrictions. Raw-raster reconstruction is not part of the public summary-replay command.

GDP statistical sources: the *China City Statistical Yearbook* (中国城市统计年鉴; relevant editions through 2025), compiled by the Urban Socio-Economic Survey Department of the National Bureau of Statistics, and municipal/provincial statistical-bureau publications. The National Bureau of Statistics portal is https://www.stats.gov.cn/ . Study-specific publication titles, table/page locators, vintages and verification evidence are retained in the author record.

For part of the 2022-2024 extension, an intermediary compiled workbook derived from these statistical sources was used for extraction and harmonization. The workbook is not treated as an original statistical source and is not included in the public archive. Official-source observations independently retrieved from the upstream publications take precedence whenever available.

Third-party geographic boundary resources are likewise not bundled. No raw-source file, account credential, acquired provider PDF/HTML or third-party boundary geometry is included in the public archive.
