# Abbreviations

**File:** `data/abbreviations.csv`  
**Dictionary:** `dictionaries/abbreviations_dictionary.csv`

## Purpose
Map common abbreviations/acronyms to their full expansions and a coarse `scope` to help readers interpret context.

## Columns
- `term` — Abbreviation/acronym (unique).
- `expansion` — Full expansion.
- `scope` — Category tag. Recommended set:
  `Law`, `Agency`, `Oversight`, `Index/Metric`, `NGO`, `Think Tank/NGO`,
  `Intl. Org`, `Non-state actor`, `Policy`, `Program`, `Law/Authority`,
  `Company`, `Court`, `General`, `Tech`, `Admin/NEPA`.

## Notes
- `term` should be unique; duplicates are warned by the validator.
- You may use additional `scope` values; they will appear as warnings unless added to the recommended list in `run_all.py`.
