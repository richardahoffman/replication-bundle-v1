# Dataset: appendix_b_evidence_to_claim.csv

**Purpose**  
Claim-level evidence table that encodes the logic of support/contrast and records the **test type** used.

**File**  
`data/appendix_b_evidence_to_claim.csv`  (CSV, UTF-8)

**Row count**  
TBD — run `python code/run_all.py --summary`.

**Columns (required)**

| Column       | Description                                                                                                  |
|--------------|--------------------------------------------------------------------------------------------------------------|
| `domain`     | Domain/subcase (e.g., Education, Health/Medicine, Justice, etc.).                                           |
| `claim_id`   | Stable identifier for the claim (format `B-###`).                                                            |
| `claim_text` | One-sentence statement of the claim being tested.                                                            |
| `test_type`  | One of: `straw_in_the_wind`, `hoop`, `smoking_gun`, `doubly_decisive`.                                       |
| `method`     | Brief note on approach (design, comparison, instrument, model, heuristic).                                   |
| `sources`    | Citations for the specific evidence (semicolon-separated if multiple).                                       |
| `notes`      | Freeform remarks or qualifiers.                                                                              |

**Conventions & caveats**
- `claim_id` must be unique and match `^B-\d{3}$`.
- `test_type` is validated against the four allowed values.
- Prefer primary documents and nonpartisan government sources where available.

**Dictionary**  
See `dictionaries/appendix_b_evidence_to_claim_dictionary.csv`.
