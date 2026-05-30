"""IBM HR Employee Attrition portfolio analysis.

Run from the project root:
    python3 notebooks/hr_attrition_analysis.py
"""

from pathlib import Path
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
CLEAN_DIR = PROJECT_ROOT / "data" / "cleaned"
CHART_DIR = PROJECT_ROOT / "reports" / "charts"
INSIGHT_DIR = PROJECT_ROOT / "reports" / "insights"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)
INSIGHT_DIR.mkdir(parents=True, exist_ok=True)

PRIMARY = "#1a1a2e"
ACCENT = "#e94560"
SUCCESS = "#0f9b58"
WARNING = "#f5a623"
BACKGROUND = "#f8f9fa"


def load_data(csv_path=RAW_PATH):
    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded dataset: {csv_path}")
        return df
    except FileNotFoundError:
        print(f"ERROR: CSV not found at {csv_path}")
        print("Download the Kaggle CSV and place it inside data/raw/.")
        raise
    except pd.errors.EmptyDataError:
        print("ERROR: The CSV exists but is empty.")
        raise
    except pd.errors.ParserError as error:
        print(f"ERROR: CSV parsing failed: {error}")
        raise


def inspect_data(df):
    print("\n" + "=" * 70)
    print("RAW DATA INSPECTION")
    print("=" * 70)
    print(f"Shape: {df.shape}")
    print("\nData types:")
    print(df.dtypes.to_string())
    print("\nNull counts:")
    print(df.isna().sum().to_string())


def tenure_group(years):
    if years <= 2:
        return "New: 0-2 yrs"
    if years <= 5:
        return "Mid: 3-5 yrs"
    if years <= 10:
        return "Senior: 6-10 yrs"
    return "Veteran: 10+ yrs"


def clean_data(df):
    cleaned = df.copy()
    useless_columns = ["EmployeeCount", "Over18", "StandardHours"]
    cleaned.drop(columns=useless_columns, inplace=True)

    cleaned["attrition_flag"] = cleaned["Attrition"].map({"Yes": 1, "No": 0}).astype(int)
    cleaned["salary_band"] = pd.cut(
        cleaned["MonthlyIncome"],
        bins=[-np.inf, 2999, 6999, np.inf],
        labels=["Low", "Mid", "High"],
        ordered=True,
    )
    cleaned["tenure_group"] = cleaned["YearsAtCompany"].apply(tenure_group)
    cleaned["overtime_flag"] = cleaned["OverTime"].map({"Yes": 1, "No": 0}).astype(int)

    categorical_columns = cleaned.select_dtypes(include=["object", "category"]).columns.tolist()
    encoded = pd.get_dummies(cleaned, columns=categorical_columns, drop_first=False, dtype=int)

    cleaned.to_csv(CLEAN_DIR / "hr_clean.csv", index=False)
    encoded.to_csv(CLEAN_DIR / "hr_encoded.csv", index=False)

    print("\n" + "=" * 70)
    print("DATA CLEANING")
    print("=" * 70)
    print(f"Dropped constant-value columns: {useless_columns}")
    print("Null handling: no missing values exist in the IBM source CSV; no imputation was required.")
    print("Categorical encoding: one-hot encoding was applied in hr_encoded.csv.")
    print("Why: one-hot encoding avoids inventing numeric order for categories such as Department or JobRole.")
    print("hr_clean.csv keeps readable labels for EDA and Power BI.")

    print("\n" + "=" * 70)
    print("CLEANED DATA SUMMARY")
    print("=" * 70)
    print(f"Total employees: {cleaned['EmployeeNumber'].nunique():,}")
    print(f"Attrition rate: {cleaned['attrition_flag'].mean() * 100:.2f}%")
    print(f"Departments: {cleaned['Department'].nunique()}")
    print(f"Average age: {cleaned['Age'].mean():.2f}")
    print(f"Average monthly salary: {cleaned['MonthlyIncome'].mean():,.2f}")
    return cleaned, encoded


def save_plot(filename):
    plt.tight_layout()
    plt.savefig(CHART_DIR / filename, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()


def analysis_1_department_job_role(df):
    department = (
        df.groupby("Department")
        .agg(employees=("EmployeeNumber", "count"), attrition_count=("attrition_flag", "sum"), attrition_rate=("attrition_flag", "mean"))
        .reset_index()
    )
    department["attrition_rate"] = (department["attrition_rate"] * 100).round(2)

    role = (
        df.groupby(["Department", "JobRole"])
        .agg(employees=("EmployeeNumber", "count"), attrition_count=("attrition_flag", "sum"), attrition_rate=("attrition_flag", "mean"))
        .reset_index()
        .sort_values("attrition_rate", ascending=False)
    )
    role["attrition_rate"] = (role["attrition_rate"] * 100).round(2)

    print("\nANALYSIS 1 — ATTRITION BY DEPARTMENT & JOB ROLE")
    print(role.head(10).to_string(index=False))

    chart = role.sort_values("attrition_rate")
    colors = chart["attrition_rate"].apply(lambda x: ACCENT if x >= 20 else WARNING if x >= 12 else SUCCESS)
    plt.figure(figsize=(12, 7))
    plt.barh(chart["JobRole"], chart["attrition_rate"], color=colors)
    plt.title("Attrition Rate by Job Role", fontsize=16, fontweight="bold")
    plt.xlabel("Attrition Rate (%)")
    plt.ylabel("Job Role")
    save_plot("01_attrition_by_job_role.png")

    print("Insights:")
    print(f"- Highest-risk role: {role.iloc[0]['JobRole']} at {role.iloc[0]['attrition_rate']:.2f}%.")
    print(f"- Highest-risk department: {department.sort_values('attrition_rate', ascending=False).iloc[0]['Department']}.")
    print("- Role-level analysis is more actionable than company-wide averages for targeted retention plans.")
    return department, role


def analysis_2_salary_vs_attrition(df):
    salary = (
        df.groupby(["salary_band", "Attrition"], observed=True)
        .agg(employees=("EmployeeNumber", "count"), avg_income=("MonthlyIncome", "mean"))
        .reset_index()
    )
    salary_band = (
        df.groupby("salary_band", observed=True)
        .agg(employees=("EmployeeNumber", "count"), attrition_count=("attrition_flag", "sum"), attrition_rate=("attrition_flag", "mean"), avg_income=("MonthlyIncome", "mean"))
        .reset_index()
    )
    salary_band["attrition_rate"] = (salary_band["attrition_rate"] * 100).round(2)
    salary_band["avg_income"] = salary_band["avg_income"].round(2)

    print("\nANALYSIS 2 — SALARY VS ATTRITION")
    print(salary_band.to_string(index=False))

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="Attrition", y="MonthlyIncome", palette={"No": SUCCESS, "Yes": ACCENT})
    plt.title("Monthly Income Distribution by Attrition Status", fontsize=16, fontweight="bold")
    plt.xlabel("Attrition Status")
    plt.ylabel("Monthly Income")
    save_plot("02_salary_boxplot.png")

    plt.figure(figsize=(9, 6))
    sns.barplot(data=salary_band, x="salary_band", y="attrition_rate", palette=[ACCENT, WARNING, SUCCESS])
    plt.title("Attrition Rate by Salary Band", fontsize=16, fontweight="bold")
    plt.xlabel("Salary Band")
    plt.ylabel("Attrition Rate (%)")
    save_plot("02_attrition_by_salary_band.png")

    low = salary_band.loc[salary_band["salary_band"] == "Low", "attrition_rate"].iloc[0]
    high = salary_band.loc[salary_band["salary_band"] == "High", "attrition_rate"].iloc[0]
    print("Insights:")
    print(f"- Low-salary employees leave at {low:.2f}%, versus {high:.2f}% for high-salary employees.")
    print("- Income distribution for leavers is concentrated lower than for retained employees.")
    print("- Compensation review should be prioritized for lower-income, high-demand roles.")
    return salary, salary_band


def analysis_3_overtime_impact(df):
    overtime = (
        df.groupby("OverTime")
        .agg(employees=("EmployeeNumber", "count"), attrition_count=("attrition_flag", "sum"), attrition_rate=("attrition_flag", "mean"))
        .reset_index()
    )
    overtime["attrition_rate"] = (overtime["attrition_rate"] * 100).round(2)

    dept = (
        df.groupby(["Department", "OverTime"])
        .agg(employees=("EmployeeNumber", "count"), attrition_rate=("attrition_flag", "mean"))
        .reset_index()
    )
    dept["attrition_rate"] = (dept["attrition_rate"] * 100).round(2)

    role = (
        df.groupby(["JobRole", "OverTime"])
        .agg(employees=("EmployeeNumber", "count"), attrition_rate=("attrition_flag", "mean"))
        .reset_index()
        .sort_values("attrition_rate", ascending=False)
    )
    role["attrition_rate"] = (role["attrition_rate"] * 100).round(2)

    print("\nANALYSIS 3 — OVERTIME IMPACT")
    print(overtime.to_string(index=False))
    print("\nTop overtime role risks:")
    print(role[role["OverTime"] == "Yes"].head(10).to_string(index=False))

    plt.figure(figsize=(11, 6))
    sns.barplot(data=dept, x="Department", y="attrition_rate", hue="OverTime", palette={"No": SUCCESS, "Yes": ACCENT})
    plt.title("Overtime vs Non-Overtime Attrition by Department", fontsize=16, fontweight="bold")
    plt.xlabel("Department")
    plt.ylabel("Attrition Rate (%)")
    plt.legend(title="Overtime")
    save_plot("03_overtime_by_department.png")

    yes_rate = overtime.loc[overtime["OverTime"] == "Yes", "attrition_rate"].iloc[0]
    no_rate = overtime.loc[overtime["OverTime"] == "No", "attrition_rate"].iloc[0]
    print("Insights:")
    print(f"- Overtime employees leave at {yes_rate:.2f}%, compared with {no_rate:.2f}% without overtime.")
    print(f"- Overtime attrition risk is {yes_rate / no_rate:.2f}x higher.")
    print("- Workload interventions should focus on departments where overtime and attrition rise together.")
    return overtime, dept, role


def analysis_4_tenure_promotion(df):
    tenure = (
        df.groupby("YearsAtCompany")
        .agg(employees=("EmployeeNumber", "count"), attrition_rate=("attrition_flag", "mean"))
        .reset_index()
    )
    tenure["attrition_rate"] = (tenure["attrition_rate"] * 100).round(2)

    promotion = (
        df.groupby("YearsSinceLastPromotion")
        .agg(employees=("EmployeeNumber", "count"), attrition_rate=("attrition_flag", "mean"))
        .reset_index()
    )
    promotion["attrition_rate"] = (promotion["attrition_rate"] * 100).round(2)

    heat = df.pivot_table(index="YearsAtCompany", columns="YearsSinceLastPromotion", values="attrition_flag", aggfunc="mean") * 100

    print("\nANALYSIS 4 — TENURE & PROMOTION")
    print("Highest tenure danger zones:")
    print(tenure.sort_values("attrition_rate", ascending=False).head(10).to_string(index=False))
    print("\nHighest promotion-gap danger zones:")
    print(promotion.sort_values("attrition_rate", ascending=False).head(10).to_string(index=False))

    plt.figure(figsize=(14, 8))
    sns.heatmap(heat, cmap="YlOrRd", linewidths=0.3, linecolor="white")
    plt.title("Attrition Rate Heatmap: Tenure vs Years Since Last Promotion", fontsize=16, fontweight="bold")
    plt.xlabel("Years Since Last Promotion")
    plt.ylabel("Years at Company")
    save_plot("04_tenure_promotion_heatmap.png")

    danger = tenure[tenure["employees"] >= 10].sort_values("attrition_rate", ascending=False).iloc[0]
    print("Insights:")
    print(f"- Among tenure groups with at least 10 people, year {int(danger['YearsAtCompany'])} is the largest exit danger zone at {danger['attrition_rate']:.2f}%.")
    print("- Early-tenure exits indicate onboarding and role-fit issues.")
    print("- Promotion-gap heatmaps help HR prioritize career-path conversations.")
    return tenure, promotion, heat


def analysis_5_satisfaction(df):
    metrics = ["JobSatisfaction", "EnvironmentSatisfaction", "WorkLifeBalance"]
    frames = []
    for metric in metrics:
        grouped = df.groupby(metric).agg(employees=("EmployeeNumber", "count"), attrition_rate=("attrition_flag", "mean")).reset_index()
        grouped["attrition_rate"] = (grouped["attrition_rate"] * 100).round(2)
        grouped.rename(columns={metric: "score"}, inplace=True)
        grouped["metric"] = metric
        frames.append(grouped)
    combined = pd.concat(frames, ignore_index=True)

    metric_gap = (
        combined.groupby("metric")
        .apply(lambda x: x.loc[x["score"] == x["score"].min(), "attrition_rate"].iloc[0] - x.loc[x["score"] == x["score"].max(), "attrition_rate"].iloc[0])
        .sort_values(ascending=False)
    )

    print("\nANALYSIS 5 — SATISFACTION SCORE IMPACT")
    print(combined.to_string(index=False))
    print("\nLow-vs-high score attrition gap:")
    print(metric_gap.to_string())

    plt.figure(figsize=(12, 7))
    sns.barplot(data=combined, x="score", y="attrition_rate", hue="metric", palette=[ACCENT, WARNING, PRIMARY])
    plt.title("Attrition Rate by Satisfaction and Work-Life Scores", fontsize=16, fontweight="bold")
    plt.xlabel("Score (1 = Low, 4 = High)")
    plt.ylabel("Attrition Rate (%)")
    plt.legend(title="Metric")
    save_plot("05_satisfaction_attrition.png")

    print("Insights:")
    print(f"- Strongest low-vs-high attrition gap: {metric_gap.index[0]} at {metric_gap.iloc[0]:.2f} percentage points.")
    print("- Low satisfaction consistently signals higher retention risk.")
    print("- Satisfaction surveys become more useful when joined with overtime and salary data.")
    return combined, metric_gap


def analysis_6_high_risk_profile(df):
    profile = df.copy()
    profile["high_risk_flag"] = np.where(
        (profile["MonthlyIncome"] < 3000)
        & (profile["OverTime"] == "Yes")
        & (profile["JobSatisfaction"] <= 2)
        & (profile["YearsAtCompany"] <= 2),
        1,
        0,
    )

    high_risk = profile[profile["high_risk_flag"] == 1]
    low_risk = profile[profile["high_risk_flag"] == 0]
    summary = pd.DataFrame({
        "profile": ["High Risk", "Lower Risk"],
        "employees": [len(high_risk), len(low_risk)],
        "attrition_rate": [high_risk["attrition_flag"].mean() * 100, low_risk["attrition_flag"].mean() * 100],
        "avg_income": [high_risk["MonthlyIncome"].mean(), low_risk["MonthlyIncome"].mean()],
        "avg_tenure": [high_risk["YearsAtCompany"].mean(), low_risk["YearsAtCompany"].mean()],
        "avg_job_satisfaction": [high_risk["JobSatisfaction"].mean(), low_risk["JobSatisfaction"].mean()],
        "avg_work_life_balance": [high_risk["WorkLifeBalance"].mean(), low_risk["WorkLifeBalance"].mean()],
    }).round(2)

    print("\nANALYSIS 6 — HIGH RISK EMPLOYEE PROFILE")
    print(summary.to_string(index=False))
    print("\nSample high-risk employees:")
    print(high_risk[["EmployeeNumber", "Department", "JobRole", "MonthlyIncome", "OverTime", "JobSatisfaction", "YearsAtCompany", "Attrition"]].head(10).to_string(index=False))

    radar_metrics = ["Income", "Tenure", "Job Satisfaction", "Work-Life Balance", "No Overtime"]
    high_values = [
        high_risk["MonthlyIncome"].mean() / df["MonthlyIncome"].max(),
        high_risk["YearsAtCompany"].mean() / max(df["YearsAtCompany"].max(), 1),
        high_risk["JobSatisfaction"].mean() / 4,
        high_risk["WorkLifeBalance"].mean() / 4,
        1 - high_risk["overtime_flag"].mean(),
    ]
    low_values = [
        low_risk["MonthlyIncome"].mean() / df["MonthlyIncome"].max(),
        low_risk["YearsAtCompany"].mean() / max(df["YearsAtCompany"].max(), 1),
        low_risk["JobSatisfaction"].mean() / 4,
        low_risk["WorkLifeBalance"].mean() / 4,
        1 - low_risk["overtime_flag"].mean(),
    ]

    angles = np.linspace(0, 2 * np.pi, len(radar_metrics), endpoint=False).tolist()
    high_values += high_values[:1]
    low_values += low_values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"polar": True})
    ax.plot(angles, high_values, color=ACCENT, linewidth=2, label="High Risk")
    ax.fill(angles, high_values, color=ACCENT, alpha=0.20)
    ax.plot(angles, low_values, color=SUCCESS, linewidth=2, label="Lower Risk")
    ax.fill(angles, low_values, color=SUCCESS, alpha=0.15)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(radar_metrics)
    ax.set_yticklabels([])
    ax.set_title("High-Risk vs Lower-Risk Employee Profile", fontsize=16, fontweight="bold", pad=24)
    ax.legend(loc="upper right", bbox_to_anchor=(1.20, 1.10))
    save_plot("06_high_risk_radar.png")

    print("Insights:")
    print(f"- Composite high-risk profile contains {len(high_risk)} employees.")
    print(f"- High-risk attrition is {summary.iloc[0]['attrition_rate']:.2f}%, versus {summary.iloc[1]['attrition_rate']:.2f}% for other employees.")
    print("- A combined risk rule is more useful for intervention lists than any single KPI.")
    return summary, high_risk


def write_measured_insights(df, role, salary_band, overtime, high_risk):
    low = salary_band.loc[salary_band["salary_band"] == "Low", "attrition_rate"].iloc[0]
    high = salary_band.loc[salary_band["salary_band"] == "High", "attrition_rate"].iloc[0]
    overtime_yes = overtime.loc[overtime["OverTime"] == "Yes", "attrition_rate"].iloc[0]
    overtime_no = overtime.loc[overtime["OverTime"] == "No", "attrition_rate"].iloc[0]
    high_risk_rate = high_risk["attrition_flag"].mean() * 100 if len(high_risk) else 0
    top_role = role.iloc[0]
    text = f"""# Measured Insights

- Overall attrition rate: {df['attrition_flag'].mean() * 100:.2f}% ({df['attrition_flag'].sum()} of {len(df)} employees).
- Overtime employees have {overtime_yes:.2f}% attrition versus {overtime_no:.2f}% without overtime, a {overtime_yes / overtime_no:.2f}x risk ratio.
- Low-salary employees have {low:.2f}% attrition versus {high:.2f}% for high-salary employees, a {low / high:.2f}x difference.
- Highest-risk job role: {top_role['JobRole']} at {top_role['attrition_rate']:.2f}% attrition.
- Composite high-risk segment size: {len(high_risk)} employees with {high_risk_rate:.2f}% attrition.
- Average monthly income: {df['MonthlyIncome'].mean():,.2f}; average age: {df['Age'].mean():.2f}.
"""
    (INSIGHT_DIR / "measured_findings.md").write_text(text)


def main():
    raw = load_data()
    inspect_data(raw)
    cleaned, _encoded = clean_data(raw)
    _department, role = analysis_1_department_job_role(cleaned)
    _salary, salary_band = analysis_2_salary_vs_attrition(cleaned)
    overtime, _dept_overtime, _role_overtime = analysis_3_overtime_impact(cleaned)
    analysis_4_tenure_promotion(cleaned)
    analysis_5_satisfaction(cleaned)
    _risk_summary, high_risk = analysis_6_high_risk_profile(cleaned)
    write_measured_insights(cleaned, role, salary_band, overtime, high_risk)
    print("\nAnalysis complete. Review data/cleaned, reports/charts, and reports/insights.")


if __name__ == "__main__":
    main()

