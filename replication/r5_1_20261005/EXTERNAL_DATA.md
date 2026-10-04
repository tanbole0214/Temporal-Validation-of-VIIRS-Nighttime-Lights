# External data products and providers

Raw external data are not redistributed or downloaded by this package.

EOG lineage: the frozen 2013-2021 observations use Annual VIIRS Nighttime Lights VNL V2.1 (https://eogdata.mines.edu/products/vnl/). The 2022-2024 continuation is the annual VNL-derived Cloud-Optimized GeoTIFF series in OpenGeoHub Zenodo record 17294744, version v0.4 (https://doi.org/10.5281/zenodo.17294744), not an assertion that the original VNL V2.1 files were used through 2024. Only observed VIIRS years are used; backward-extrapolated 2000-2011 values are excluded. Extension growth uses adjacent years within the extension source, including its own 2021 for 2022 growth. The overlap bridge yields a net EOG factor of 1.0 on extracted aggregates. Consult manuscript Methods and Supplementary Information for support and bridge qualifications; numerical scale matching does not establish exact physical radiance equivalence.

NASA Black Marble VNP46A4 Collection 2: https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A4/ . Earthdata registration/authentication may be required. The extension uses AllAngle_Composite_Snow_Free; finite non-negative radiance; quality code 0; more than three observations; land/water codes 0/1/2/5; and a 0.50 nW cm^-2 sr^-1 background threshold. Fixed support and all_touched=True are disclosed separately from GDP timing restrictions. Raw-raster reconstruction is not part of the public summary-replay command.

Official GDP sources: national, provincial and municipal statistical publishing bodies; https://www.stats.gov.cn/ is the national portal, not an exact substitute for all study-specific publications. Detailed publication locators, vintages and verification evidence are retained in the author record and available through the access enquiry described in DATA_ACCESS.md, where lawful. No claim is made that provider portals alone reconstruct the mixed-source panel exactly.

Compiled GDP workbook: Markdata (马克集数), https://www.macrodatas.cn/ . Access conditions, purchase/login requirements and permissions are determined by the provider. The authors do not grant redistribution rights to this workbook.

Third-party geographic boundary resources are likewise not bundled. No raw-source file, account credential, provider PDF/HTML or third-party boundary geometry is included in the public archive.
