# Appendix E — Timelines

**File:** `data/appendix_e_timelines.csv`  
**Dictionary:** `dictionaries/appendix_e_timelines_dictionary.csv`

## Purpose
Event timelines per subcase with ISO dates and optional precision.

## Columns
- `domain` — Domain/subcase label.
- `date` — ISO `YYYY`, `YYYY-MM`, or `YYYY-MM-DD`.
- `event` — Concise event description.
- `source_id` — Key to `provenance/sources.*`.
- `date_precision` *(optional)* — `day`, `month`, or `year`.
- `event_id` *(optional)* — Stable ID `E-###`.

## Notes
- If a source gives only month/year, use `YYYY-MM` and set `date_precision = month`.
- Validator checks date formats and will flag invalid months/days.
