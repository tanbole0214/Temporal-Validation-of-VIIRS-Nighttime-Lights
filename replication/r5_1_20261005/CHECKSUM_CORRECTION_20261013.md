# R5.1 package correction on 13 October 2026

The previously cited a3e8fa710f9545c5fdd91b1d95fb088d07958283 snapshot had 25 mismatches in its 26-entry package manifest. Twenty-one came from CRLF/LF byte differences, and four documentation files had changed without regenerating the manifest. The check stopped before summary reproduction. This was a packaging failure, not evidence that the numerical estimates changed.

This correction stores package text as UTF-8 with LF line endings and includes a local .gitattributes rule for Git checkouts. PACKAGE_SHA256.csv is regenerated from the actual delivered bytes, excluding itself. The integrity check remains enabled and unchanged. Statistical .py files, reference CSV cells and Table 3 values are preserved. No restricted input is added. ENVIRONMENT.json now correctly requires Python 3.11 or later for the pinned dependencies.

The current manuscript title and direct workbook provider are disclosed. DATA_ACCESS.md distinguishes a provider-access enquiry from permission to supply data. Verification access remains subject to actual provider agreement; successful summary replay does not settle that condition.

Validation covers a newly extracted public archive and clean Git checkouts with both core.autocrlf=true and false, using the pinned dependencies. Public-only execution checks 64 metric rows, 704 numeric values and 48 Table 3 data cells. It does not refit city-level estimates or bootstrap intervals. The final published commit and downloadable asset must be read back and tested before they are cited as verified. Earlier immutable tags remain unchanged.
