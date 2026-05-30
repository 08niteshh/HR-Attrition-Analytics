# Power BI Dashboard Plan

## Data Model

The IBM dataset is employee-level, so the model can start with one fact table:

- `hr_clean`

Optional dimension tables for a star schema:

- `DimDepartment[Department]` 1:* `hr_clean[Department]`
- `DimJobRole[JobRole]` 1:* `hr_clean[JobRole]`
- `DimEmployee[EmployeeNumber]` 1:1 `hr_clean[EmployeeNumber]`

## Power Query Setup

Import `data/cleaned/hr_clean.csv`.

Set data types:

- Whole Number: `Age`, `EmployeeNumber`, `DistanceFromHome`, `Education`, `EnvironmentSatisfaction`, `JobInvolvement`, `JobLevel`, `JobSatisfaction`, `MonthlyIncome`, `NumCompaniesWorked`, `PercentSalaryHike`, `PerformanceRating`, `RelationshipSatisfaction`, `StockOptionLevel`, `TotalWorkingYears`, `TrainingTimesLastYear`, `WorkLifeBalance`, `YearsAtCompany`, `YearsInCurrentRole`, `YearsSinceLastPromotion`, `YearsWithCurrManager`, `attrition_flag`, `overtime_flag`
- Text: `Attrition`, `BusinessTravel`, `Department`, `EducationField`, `Gender`, `JobRole`, `MaritalStatus`, `OverTime`, `salary_band`, `tenure_group`

Calculated columns already included by Python:

- `attrition_flag`
- `salary_band`
- `tenure_group`
- `overtime_flag`

Optional Power Query equivalent for risk segmentation:

```powerquery
High Risk Flag =
if [OverTime] = "Yes"
and [JobSatisfaction] < 2
and [MonthlyIncome] < 3000
then 1
else 0
```

## DAX Measures

```DAX
Total Employees =
DISTINCTCOUNT(hr_clean[EmployeeNumber])
```

```DAX
Attrition Employees =
CALCULATE(
    [Total Employees],
    hr_clean[Attrition] = "Yes"
)
```

```DAX
Attrition Rate % =
DIVIDE(
    [Attrition Employees],
    [Total Employees],
    0
)
```

```DAX
Active Employees =
[Total Employees] - [Attrition Employees]
```

```DAX
Avg Monthly Income =
AVERAGE(hr_clean[MonthlyIncome])
```

```DAX
Avg Tenure =
AVERAGE(hr_clean[YearsAtCompany])
```

```DAX
Overtime Employees =
CALCULATE(
    [Total Employees],
    hr_clean[OverTime] = "Yes"
)
```

```DAX
Overtime Rate % =
DIVIDE(
    [Overtime Employees],
    [Total Employees],
    0
)
```

```DAX
High Risk Employee Count =
CALCULATE(
    [Total Employees],
    FILTER(
        hr_clean,
        hr_clean[OverTime] = "Yes"
            && hr_clean[JobSatisfaction] < 2
            && hr_clean[MonthlyIncome] < 3000
    )
)
```

## Dashboard Pages

### Page 1 — Overview

- KPI cards: Total Employees, Active Employees, Attrition Rate %, Avg Monthly Income
- Gauge: Attrition Rate %
- Bar chart: Attrition Rate % by Department
- Donut chart: Employees by Department
- Slicers: Department, Gender, JobRole

### Page 2 — Risk Analysis

- Scatter: MonthlyIncome vs YearsAtCompany, legend by Attrition
- Grouped bar: Attrition Rate % by OverTime and Department
- Matrix heatmap: JobSatisfaction vs EnvironmentSatisfaction with Attrition Rate %
- Cards: Overtime Rate %, High Risk Employee Count
- Slicers: Salary Band, OverTime, Department

### Page 3 — Employee Profile

- Line chart: Attrition Rate % by YearsAtCompany
- Matrix: YearsAtCompany vs YearsSinceLastPromotion with Attrition Rate %
- Table: high-risk employees with EmployeeNumber, Department, JobRole, MonthlyIncome, OverTime, JobSatisfaction, YearsAtCompany
- Slicers: Tenure Group, Department, JobRole

## Theme

- Primary: `#1a1a2e`
- Accent: `#e94560`
- Success: `#0f9b58`
- Warning: `#f5a623`
- Background: `#f8f9fa`

Import `powerbi/hr_attrition_theme.json` from `View` → `Themes` → `Browse for themes`.

## Build Page 1 Step by Step

1. Open Power BI Desktop.
2. Select `Get Data` → `Text/CSV`.
3. Import `data/cleaned/hr_clean.csv`.
4. Confirm column data types in Power Query using the list above.
5. Click `Close & Apply`.
6. Create each DAX measure from the Modeling tab.
7. Rename the page to `Overview`.
8. Set the canvas background to `#f8f9fa`.
9. Add four Card visuals in one row:
   - Total Employees
   - Active Employees
   - Attrition Rate %
   - Avg Monthly Income
10. Add a Gauge visual:
   - Value: `Attrition Rate %`
   - Minimum: `0`
   - Maximum: `0.30`
11. Add a Clustered Bar Chart:
   - Y-axis: `Department`
   - X-axis: `Attrition Rate %`
12. Add a Donut Chart:
   - Legend: `Department`
   - Values: `Total Employees`
13. Add slicers:
   - `Department`
   - `Gender`
   - `JobRole`
14. Apply the provided JSON theme.
15. Add the title `HR Attrition Analytics Overview`.
16. Save the file as `powerbi/HR_Attrition_Dashboard.pbix`.

