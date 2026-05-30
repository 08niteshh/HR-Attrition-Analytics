# HR Attrition Analytics Dashboard

![Python](https://img.shields.io/badge/Python-Data%20Analysis-3776AB)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-336791)
![Tableau](https://img.shields.io/badge/Tableau-Dashboard-E97627)
![Status](https://img.shields.io/badge/Status-Portfolio%20Ready-0f9b58)

An end-to-end HR analytics portfolio project that identifies employee attrition drivers, segments high-risk profiles, and translates retention data into business-ready insights.

🔗 **[Live Tableau Dashboard](https://public.tableau.com/app/profile/nitesh.yadav7047/viz/HRAttritionAnalytics_17801406990900/HRAttritionAnalyticsDashboard)**

---

## Business Problem

Employee attrition affects recruiting cost, productivity, team stability, and institutional knowledge. This project analyzes the IBM HR Analytics dataset to answer practical retention questions:

- Which departments and job roles face the highest attrition risk?
- How strongly are salary, overtime, tenure, promotions, and satisfaction associated with departures?
- Which employee profiles should HR prioritize for proactive intervention?

---

## Key Findings

- Overall attrition is **16.12%**: 237 of 1,470 employees left the organization.
- Employees working overtime have **30.53% attrition**, versus **10.44%** without overtime: a **2.92x risk ratio**.
- Employees earning below 3,000 per month have **28.61% attrition**, versus **10.80%** for employees earning 7,000+: a **2.65x gap**.
- Sales Representatives have the highest role-level attrition rate at **39.76%**.
- Employees with under one year at the company show **36.36% attrition**, highlighting onboarding and early role-fit risk.
- A composite profile combining low salary, overtime, low satisfaction, and short tenure identifies **21 high-risk employees** with a **71.43% historical attrition rate**.

---

## Tech Stack

- **Python:** pandas, numpy, matplotlib, seaborn
- **SQL:** PostgreSQL, CTEs, conditional aggregations, window functions
- **Tableau:** Interactive dashboard published on Tableau Public
- **GitHub:** project documentation and portfolio presentation

---

## Dashboard Preview

🔗 **Live Dashboard:** [Click here to view](https://public.tableau.com/app/profile/nitesh.yadav7047/viz/HRAttritionAnalytics_17801406990900/HRAttritionAnalyticsDashboard)

The dashboard includes:
- Attrition rate by Job Role and Department
- Overtime impact analysis
- Salary band vs attrition breakdown
- Job satisfaction correlation
- Tenure group risk analysis

---

## Project Structure

```
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
├── reports/
│   ├── charts/
│   │   ├── 01_attrition_by_job_role.png
│   │   ├── 02_salary_boxplot.png
│   │   ├── 03_overtime_by_department.png
│   │   ├── 04_tenure_promotion_heatmap.png
│   │   ├── 05_satisfaction_attrition.png
│   │   └── 06_high_risk_radar.png
│   └── insights/
│       └── measured_findings.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

## How to Run

**1. Clone the repository:**
```bash
git clone https://github.com/08niteshh/HR-Attrition-Analytics.git
cd HR-Attrition-Analytics
```

**2. Install packages:**
```bash
pip install -r requirements.txt
```

**3. Download the IBM HR Analytics CSV from Kaggle and place it here:**
```
data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv
```

**4. Run the complete analysis:**
```bash
python3 notebooks/hr_attrition_analysis.py
```

**5. View outputs:**
- Charts → `reports/charts/`
- Insights → `reports/insights/`
- Cleaned data → `data/cleaned/`

---

## Dataset

IBM HR Analytics Employee Attrition & Performance dataset:
https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

The dataset is synthetic and is used for educational analytics projects.

---

## Skills Demonstrated

- Data cleaning and feature engineering
- Exploratory data analysis (EDA)
- HR and people analytics
- KPI design and risk segmentation
- PostgreSQL CTEs and window functions
- Tableau dashboard design and publishing
- Business communication and data storytelling

---

## Contact

**Nitesh Yadav**
- GitHub: [@08niteshh](https://github.com/08niteshh)
- Email: niteshyadav08042005@gmail.com

