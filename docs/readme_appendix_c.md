# Appendix C — Indicators

**File:** `data/appendix_c_indicators.csv`  
**Dictionary:** `dictionaries/appendix_c_indicators_dictionary.csv`

## Purpose
Metadata for series/indicators used to contextualize outcomes.

## Columns
- `indicator` — Short name of the indicator/series.
- `definition` — What the indicator measures.
- `unit` — Unit of measure (%, index, USD, count, etc.).
- `source_id` — Key to `provenance/sources.*`.
- `frequency` — One of: `annual`, `quarterly`, `monthly`, `weekly`, `daily`, `ad hoc`.
- `notes` — Coverage/caveats/transformations.
- `indicator_id` *(optional)* — Stable ID `C-###`.

## Notes
- If a series is irregular or event-driven, set `frequency = ad hoc`.
- Keep `source_id` consistent with the provenance table/worksheet.
