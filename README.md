# Applicant Data Cleaning (Week 1)

## Objective
Practice real-world data cleaning and exploration with Python and Pandas on a
mock applicant dataset (Week 1 task, NextGenLearners internship). The raw file
contains deliberately messy data: missing values, duplicates, inconsistent
text, and wrong data types.

## Files
| File | Description |
|---|---|
| `Week1_Data_Cleaning_Maryam Fatima.ipynb` | Fully documented notebook (code + written explanations) |
| `applicants.csv` | Raw, messy input data (86 rows, 7 columns) |
| `applicants_cleaned.csv` | Final cleaned dataset (71 rows, 7 columns) |

## Cleaning steps
1. **Explored first:** `shape`, `head`, `info`, `isnull().sum()`, `duplicated()`, `describe()`
2. **Missing values (column by column):**
   - Applicant Name and Email: dropped rows (can't identify or contact the applicant)
   - University: filled with "Not Specified"
   - Status: filled with "Under Review"
3. **Duplicates:** removed 3 exact duplicates, then 3 near-duplicates by matching
   Email (after lowercasing and stripping spaces)
4. **Text standardization:** Domain Applied (18 variants mapped to 5 domains),
   Status (8 variants to 3 values), names in Title Case
5. **Data types:** Application Date converted to `datetime64` with
   `pd.to_datetime(errors="coerce")`; Phone kept as text with dashes and spaces
   removed so leading zeros are preserved

## Results
| | Before | After |
|---|---|---|
| Rows | 86 | 71 |
| Domain Applied variants | 18 | 5 |
| Status variants | 8 | 3 |
| Duplicate rows | 3 exact + 3 near | 0 |
| Application Date type | text | datetime64 |

Two dates were unreadable ("not sure"); they were kept as missing values (`NaT`)
instead of inventing a date.

## Tools
Python · Pandas · Jupyter Notebook (VS Code) · Git/GitHub

## How to run
```bash
pip install pandas jupyter
```
Open the notebook, keep `applicants.csv` in the same folder, and click **Run All**.
All cleaning is done in code, with no manual edits to the CSV.