# Cleaned Data

Run:

```bash
python3 notebooks/hr_attrition_analysis.py
```

The pipeline creates:

```txt
hr_clean.csv
hr_encoded.csv
```

- `hr_clean.csv` preserves readable labels for EDA and Power BI.
- `hr_encoded.csv` one-hot encodes categorical fields for model-ready analysis.

