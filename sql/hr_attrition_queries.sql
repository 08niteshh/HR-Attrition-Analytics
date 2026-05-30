-- HR Attrition Analytics: PostgreSQL Queries
-- Source table: hr_data with IBM CSV column names preserved.

-- QUERY 1: Attrition rate by department and job role, ranked highest to lowest.
-- Expected columns: department, job_role, employees, attrition_count, attrition_rate_pct, risk_rank
WITH role_attrition AS (
    SELECT
        "Department" AS department,
        "JobRole" AS job_role,
        COUNT(*) AS employees,
        COUNT(*) FILTER (WHERE "Attrition" = 'Yes') AS attrition_count
    FROM hr_data
    GROUP BY "Department", "JobRole"
)
SELECT
    department,
    job_role,
    employees,
    attrition_count,
    ROUND(attrition_count::numeric * 100 / NULLIF(employees, 0), 2) AS attrition_rate_pct,
    RANK() OVER (
        ORDER BY attrition_count::numeric / NULLIF(employees, 0) DESC
    ) AS risk_rank
FROM role_attrition
ORDER BY risk_rank, department, job_role;

-- QUERY 2: Average salary, age, and tenure for attrition versus non-attrition employees.
-- Expected columns: attrition_status, employees, avg_monthly_income, avg_age, avg_years_at_company, avg_total_working_years
SELECT
    "Attrition" AS attrition_status,
    COUNT(*) AS employees,
    ROUND(AVG("MonthlyIncome"), 2) AS avg_monthly_income,
    ROUND(AVG("Age"), 2) AS avg_age,
    ROUND(AVG("YearsAtCompany"), 2) AS avg_years_at_company,
    ROUND(AVG("TotalWorkingYears"), 2) AS avg_total_working_years
FROM hr_data
GROUP BY "Attrition"
ORDER BY attrition_status DESC;

-- QUERY 3: High-risk list: overtime, low job satisfaction, and below-average income.
-- Expected columns: employee_number, department, job_role, monthly_income, company_avg_income, job_satisfaction, years_at_company, attrition
WITH company_income AS (
    SELECT AVG("MonthlyIncome") AS avg_income
    FROM hr_data
)
SELECT
    h."EmployeeNumber" AS employee_number,
    h."Department" AS department,
    h."JobRole" AS job_role,
    h."MonthlyIncome" AS monthly_income,
    ROUND(c.avg_income, 2) AS company_avg_income,
    h."JobSatisfaction" AS job_satisfaction,
    h."YearsAtCompany" AS years_at_company,
    h."Attrition" AS attrition
FROM hr_data h
CROSS JOIN company_income c
WHERE h."OverTime" = 'Yes'
  AND h."JobSatisfaction" <= 2
  AND h."MonthlyIncome" < c.avg_income
ORDER BY h."MonthlyIncome" ASC, h."YearsAtCompany" ASC;

-- QUERY 4: Department-wise attrition trend by tenure group with window functions.
-- Expected columns: department, tenure_group, employees, attrition_count, attrition_rate_pct, department_attrition_share_pct, risk_rank_in_department
WITH grouped AS (
    SELECT
        "Department" AS department,
        CASE
            WHEN "YearsAtCompany" <= 2 THEN 'New: 0-2 yrs'
            WHEN "YearsAtCompany" <= 5 THEN 'Mid: 3-5 yrs'
            WHEN "YearsAtCompany" <= 10 THEN 'Senior: 6-10 yrs'
            ELSE 'Veteran: 10+ yrs'
        END AS tenure_group,
        COUNT(*) AS employees,
        COUNT(*) FILTER (WHERE "Attrition" = 'Yes') AS attrition_count
    FROM hr_data
    GROUP BY "Department", tenure_group
)
SELECT
    department,
    tenure_group,
    employees,
    attrition_count,
    ROUND(attrition_count::numeric * 100 / NULLIF(employees, 0), 2) AS attrition_rate_pct,
    ROUND(
        attrition_count::numeric * 100
        / NULLIF(SUM(attrition_count) OVER (PARTITION BY department), 0),
        2
    ) AS department_attrition_share_pct,
    RANK() OVER (
        PARTITION BY department
        ORDER BY attrition_count::numeric / NULLIF(employees, 0) DESC
    ) AS risk_rank_in_department
FROM grouped
ORDER BY department, risk_rank_in_department;

-- QUERY 5: Top 5 job roles with the highest attrition and average satisfaction scores.
-- Expected columns: job_role, employees, attrition_count, attrition_rate_pct, avg_job_satisfaction, avg_environment_satisfaction, avg_work_life_balance
WITH role_summary AS (
    SELECT
        "JobRole" AS job_role,
        COUNT(*) AS employees,
        COUNT(*) FILTER (WHERE "Attrition" = 'Yes') AS attrition_count,
        AVG("JobSatisfaction") AS avg_job_satisfaction,
        AVG("EnvironmentSatisfaction") AS avg_environment_satisfaction,
        AVG("WorkLifeBalance") AS avg_work_life_balance
    FROM hr_data
    GROUP BY "JobRole"
)
SELECT
    job_role,
    employees,
    attrition_count,
    ROUND(attrition_count::numeric * 100 / NULLIF(employees, 0), 2) AS attrition_rate_pct,
    ROUND(avg_job_satisfaction, 2) AS avg_job_satisfaction,
    ROUND(avg_environment_satisfaction, 2) AS avg_environment_satisfaction,
    ROUND(avg_work_life_balance, 2) AS avg_work_life_balance
FROM role_summary
ORDER BY attrition_count::numeric / NULLIF(employees, 0) DESC
LIMIT 5;

-- QUERY 6: Employees with no promotion in the last 5 years, grouped by department and attrition status.
-- Expected columns: department, attrition_status, employees, avg_years_since_last_promotion, avg_tenure, department_total, group_share_pct
WITH promotion_gap AS (
    SELECT
        "Department" AS department,
        "Attrition" AS attrition_status,
        COUNT(*) AS employees,
        AVG("YearsSinceLastPromotion") AS avg_years_since_last_promotion,
        AVG("YearsAtCompany") AS avg_tenure
    FROM hr_data
    WHERE "YearsSinceLastPromotion" >= 5
    GROUP BY "Department", "Attrition"
)
SELECT
    department,
    attrition_status,
    employees,
    ROUND(avg_years_since_last_promotion, 2) AS avg_years_since_last_promotion,
    ROUND(avg_tenure, 2) AS avg_tenure,
    SUM(employees) OVER (PARTITION BY department) AS department_total,
    ROUND(
        employees::numeric * 100
        / NULLIF(SUM(employees) OVER (PARTITION BY department), 0),
        2
    ) AS group_share_pct
FROM promotion_gap
ORDER BY department, attrition_status;

