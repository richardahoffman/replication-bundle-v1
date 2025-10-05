Institutional Inversion — Case Study: Government (US)

Replication Materials (v1.0)

Author: Richard A. Hoffman
Paper (conceptual framework): Institutional inversion: Mechanisms of mission betrayal and systemic survival.
Data bundle DOI: https://doi.org/10.5281/zenodo.17205083

What’s here

This archive contains the structured data and documentation used to generate Table 1 and Appendices B–E for the case study.

Canonical format: all datasets and dictionaries are CSV (UTF-8, comma-delimited). Any .xlsx copies (if present) are convenience files only.

Quick start

# 0) From the repo/bundle root
cd .\replication_bundle_v1\

# 1) Summarize datasets
python .\code\run_all.py --summary     # prints row/column counts and headers

# 2) Validate (IDs, enums, dates, cross-file refs)
python .\code\run_all.py --validate
# add --strict to enforce provenance/link checks as hard errors:
python .\code\run_all.py --validate --strict

Windows helpers (same as above):

.\code\summary.bat
.\code\validate.bat          # add --strict like:  python .\code\run_all.py --validate --strict

Build manifest + checksums + zip in one step (Windows):

# Validates (strict), rebuilds manifest, refreshes checksums, writes ../replication_bundle_v1.zip
powershell -ExecutionPolicy Bypass -File .\code\zip_and_hash.ps1
# Options:
#   -NoStrict        -> skip strict provenance checks
#   -SkipManifest    -> don’t rebuild file manifest
#   -ZipName NAME.zip -> set the output zip filename

Datasets (high level)

data/table1_promises_vs_outcomes.csv — Cross-administration comparison of promises vs. realized outcomes by domain/section with citations.
Dictionary: dictionaries/table1_promises_vs_outcomes_dictionary.csv

data/appendix_b_evidence_to_claim.csv — Claim-level mapping per subcase, including mechanism test tag (test_type), method, outcome indicators, and sources.
Dictionary: dictionaries/appendix_b_evidence_to_claim_dictionary.csv

data/appendix_c_indicators.csv — Series/indicator metadata to contextualize outcomes (definition, unit, frequency, source_id, notes).
Dictionary: dictionaries/appendix_c_indicators_dictionary.csv

data/appendix_e_timelines.csv — Event timelines per subcase with ISO dates (YYYY-MM-DD / YYYY-MM / YYYY) and optional date_precision.
Dictionary: dictionaries/appendix_e_timelines_dictionary.csv

data/abbreviations.csv — Abbreviation → expansion mapping with a simple scope tag.
Dictionary: dictionaries/abbreviations_dictionary.csv

For per-dataset details (purpose, required columns, caveats), see the Data Guides in docs/readme_*.md.

Reproducibility notes

Encoding: UTF-8; values are comma-delimited; quotes only where needed.

Dates: ISO-8601 (YYYY, YYYY-MM, or YYYY-MM-DD) where applicable.

Missing values: empty string.

IDs: stable row IDs may appear as B-###, C-###, E-### etc., and are unique within their dataset.

Sources: nonpartisan government publications and primary documents where possible (CBO, JCT, CRS, GAO, PCLOB, IEA, IPCC, DOI, DoS, NCES, HRW, PRAC, etc.).

Mechanisms & test_type: follow the conventions described in the case-study paper’s Methods.

Directory layout (at release)

replication_bundle_v1/
├─ checksums/
│  └─ SHA256SUMS
├─ code/
│  ├─ build_manifest.py
│  ├─ run_all.py
│  ├─ environment.yml
│  ├─ requirements.txt
│  ├─ zip_and_hash.ps1
│  ├─ summary.bat
│  └─ validate.bat
├─ data/
│  ├─ table1_promises_vs_outcomes.csv
│  ├─ appendix_b_evidence_to_claim.csv
│  ├─ appendix_c_indicators.csv
│  ├─ appendix_e_timelines.csv
│  └─ abbreviations.csv
├─ dictionaries/
│  ├─ table1_promises_vs_outcomes_dictionary.csv
│  ├─ appendix_b_evidence_to_claim_dictionary.csv
│  ├─ appendix_c_indicators_dictionary.csv
│  ├─ appendix_e_timelines_dictionary.csv
│  └─ abbreviations_dictionary.csv
├─ docs/
│  ├─ readme_table1.md
│  ├─ readme_appendix_b.md
│  ├─ readme_appendix_c.md
│  ├─ readme_appendix_e.md
│  ├─ readme_abbreviations.md
│  ├─ FILE_MANIFEST.md
│  └─ CHANGELOG.md
├─ metadata/
│  ├─ zenodo.json
│  └─ file_manifest.csv
├─ provenance/
│  └─ sources.csv
├─ .gitattributes
├─ CITATION.cff
├─ LICENSE
├─ LICENSE_CODE.txt
├─ LICENSE_DATA.txt
└─ README.md

File manifest (per-file metadata)

The script below creates and refreshes a browsable manifest and a CSV you can edit:

python .\code\build_manifest.py
# writes:
#   - metadata/file_manifest.csv   (edit: Title / Description / Keywords [/ Author])
#   - docs/FILE_MANIFEST.md        (pretty table for users)

Checksums & integrity

Refresh checksums (ASCII file for cross-platform stability):

Get-FileHash -Algorithm SHA256 -Path `
  .\data\*.csv, `
  .\dictionaries\*.csv, `
  .\code\run_all.py, `
  .\code\build_manifest.py, `
  .\code\environment.yml, `
  .\code\requirements.txt, `
  .\metadata\zenodo.json, `
  .\metadata\file_manifest.csv, `
  .\docs\readme_*.md, `
  .\docs\FILE_MANIFEST.md, `
  .\provenance\* `
| ForEach-Object { "{0}  {1}" -f $_.Hash, (Resolve-Path $_.Path -Relative) } `
| Out-File -Encoding ascii .\checksums\SHA256SUMS

Verify after download/unzip (simple PowerShell loop):

Get-Content .\checksums\SHA256SUMS | ForEach-Object {
  $parts = $_ -split '  ', 2
  $expected = $parts[0]; $rel = $parts[1]
  $actual = (Get-FileHash -Algorithm SHA256 $rel).Hash
  if ($actual -ne $expected) { Write-Host "MISMATCH: $rel" -ForegroundColor Red }
}

How to cite

Data bundle:
Hoffman, R. A. (2025). Replication materials for “Institutional inversion: Case study—Government (US)” (v1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.17205083

Framework/paper:
Hoffman, R. A. (2025). Institutional inversion: Mechanisms of mission betrayal and systemic survival. Zenodo.

License

Data & metadata: see LICENSE_DATA.txt (recommended: CC BY 4.0).

Code: see LICENSE_CODE.txt.

Repository root license: LICENSE.

Release checklist (maintainers)

 CSVs in data/ and dictionaries in dictionaries/ finalized (UTF-8).

 python .\code\build_manifest.py (refresh manifest).

 python .\code\run_all.py --validate --strict (clean).

 Refresh checksums/SHA256SUMS (or run the helper below).

 Create release zip:

powershell -ExecutionPolicy Bypass -File .\code\zip_and_hash.ps1

 Upload zip + fill record metadata on Zenodo.

 Tag in Git (optional): git tag v1.0

Contact
Questions or corrections: open an issue on the Zenodo record or contact the author.




