# HR Attrition Analytics Dashboard

![Python](https://img.shields.io/badge/Python-Data%20Analysis-3776AB)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-336791)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811)
![Status](https://img.shields.io/badge/Status-Portfolio%20Ready-0f9b58)

An end-to-end HR analytics portfolio project that identifies employee attrition drivers, segments high-risk profiles, and translates retention data into business-ready insights.

## Business Problem

Employee attrition affects recruiting cost, productivity, team stability, and institutional knowledge. This project analyzes the IBM HR Analytics dataset to answer practical retention questions:

- Which departments and job roles face the highest attrition risk?
- How strongly are salary, overtime, tenure, promotions, and satisfaction associated with departures?
- Which employee profiles should HR prioritize for proactive intervention?

## Key Findings

- Overall attrition is **16.12%**: 237 of 1,470 employees left the organization.
- Employees working overtime have **30.53% attrition**, versus **10.44%** without overtime: a **2.92x** risk ratio.
- Employees earning below 3,000 per month have **28.61% attrition**, versus **10.80%** for employees earning 7,000+: a **2.65x** gap.
- Sales Representatives have the highest role-level attrition rate at **39.76%**.
- Employees with under one year at the company show **36.36% attrition**, highlighting onboarding and early role-fit risk.
- A composite profile combining low salary, overtime, low satisfaction, and short tenure identifies **21 high-risk employees** with a **71.43%** historical attrition rate.

## Tech Stack

- Python: pandas, numpy, matplotlib, seaborn
- SQL: PostgreSQL, CTEs, conditional aggregations, window functions
- Power BI: Power Query, DAX, dashboard planning
- GitHub: project documentation and portfolio presentation

## Project Structure

```txt
HR-Attrition-Analytics/
├── data/
│   ├── raw/
│   │   └── WA_Fn-UseC_-HR-Employee-Attrition.csv
│   └── cleaned/
│       ├── hr_clean.csv
│       └── hr_encoded.csv
├── notebooks/
│   └── hr_attrition_analysis.py
├── sql/
│   └── hr_attrition_queries.sql
├── powerbi/
│   ├── dashboard_plan.md
│   └── hr_attrition_theme.json
├── reports/
│   ├── charts/
│   ├── insights/
│   │   └── measured_findings.md
│   ├── screenshots/
│   └── resume_linkedin_interview.md
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/08niteshh/HR-Attrition-Analytics.git
cd HR-Attrition-Analytics
```

2. Create and activate a Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install packages:

```bash
pip install -r requirements.txt
```

4. Download the IBM HR Analytics CSV from Kaggle and place it here:

```txt
data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv
```

5. Run the complete analysis:

```bash
python3 notebooks/hr_attrition_analysis.py
```

6. Review outputs:

```txt
data/cleaned/
reports/charts/
reports/insights/
```

7. Open Power BI Desktop and follow:

```txt
powerbi/dashboard_plan.md
```

## Dashboard Preview

Add Power BI screenshots after building the dashboard:

```txt
reports/screenshots/overview.png
reports/screenshots/risk_analysis.png
reports/screenshots/employee_profile.png
```

## Dataset

IBM HR Analytics Employee Attrition & Performance dataset:

https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

The dataset is synthetic and is used for educational analytics projects. The raw CSV is ignored by Git by default; download it locally before running the pipeline.

## Skills Demonstrated

- Data cleaning and preprocessing
- Categorical feature encoding
- Exploratory data analysis
- HR and people analytics
- KPI design and segmentation
- PostgreSQL CTEs and window functions
- Power BI modeling and DAX
- Business communication and data storytelling

## GitHub Upload Checklist

- Run `python3 notebooks/hr_attrition_analysis.py`.
- Confirm `data/cleaned/hr_clean.csv` and `data/cleaned/hr_encoded.csv` exist locally.
- Confirm 7 chart PNG files exist in `reports/charts/`.
- Build the `.pbix` file using `powerbi/dashboard_plan.md`.
- Add Power BI screenshots to `reports/screenshots/`.
- Update your GitHub username in the clone command.
- Check `git status`.
- Ensure the raw CSV and cleaned CSV files are not committed.
- Commit and push the portfolio repository.

