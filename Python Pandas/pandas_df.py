import pandas as pd


def get_employees_df():
    return pd.read_csv(
        "https://gist.githubusercontent.com/kevin336/acbb2271e66c10a5b73aacf82"
        "ca82784/raw/e38afe62e088394d61ed30884dd50a6826eee0a8/employees.csv"
    )


def get_departments_df():
    dep_df = pd.read_csv(
        "https://gist.githubusercontent.com/kevin336/5ea0e96813aa88871c20d315b5"
        "bf445c/raw/d8fcf5c2630ba12dd8802a2cdd5480621b6a0ea6/departments.csv"
    )
    dep_df = dep_df.rename(columns={"DEPARTMENT_ID": "DEPARTMENT_IDENTIFIER"})
    return dep_df


employees = get_employees_df()
departments = get_departments_df()

# 1. Calculate the average, median, lower, and upper quartiles of employees' salaries.
print("General Salary Statistics:")
print(employees["SALARY"].describe())
print("*" * 50)

salary_avg = employees["SALARY"].mean()
salary_median = employees["SALARY"].median()
salary_lower_q = employees["SALARY"].quantile(0.25)
salary_upper_q = employees["SALARY"].quantile(0.75)

# Printing the results
print("Salary Statistics:")
print(f"Average salary: {salary_avg}")
print(f"Median salary: {salary_median}")
print(f"Lower quartile: {salary_lower_q}")
print(f"Upper quartile: {salary_upper_q}")
print("*" * 50)

# 2. Calculate the average salary per department, including department names.
avg_salary_per_department = employees.groupby("DEPARTMENT_ID")["SALARY"].mean().reset_index()
avg_salary_per_department = avg_salary_per_department.merge(
    departments, left_on="DEPARTMENT_ID", right_on="DEPARTMENT_IDENTIFIER"
)
# Rename the column salary to avg_salary and keep only department id, department name, and avg_salary
avg_salary_per_department = avg_salary_per_department.rename(columns={"SALARY": "AVG_SALARY"})[
    ["DEPARTMENT_ID", "DEPARTMENT_NAME", "AVG_SALARY"]
]
print("Average Salary Per Department:")
print(avg_salary_per_department)
print("*" * 50)

# 3. Add a `SALARY_CATEGORY` column with value "low" for salaries below average and "high" for others.
employees["SALARY_CATEGORY"] = employees["SALARY"].apply(lambda x: "low" if x < salary_avg else "high")

# 4. Add `SALARY_CATEGORY_AMONG_DEPARTMENT` based on the department's average salary.
# Merge the department avg_salary into employees DataFrame
employees = employees.merge(avg_salary_per_department[["DEPARTMENT_ID", "AVG_SALARY"]], on="DEPARTMENT_ID")
employees = employees.rename(columns={"AVG_SALARY": "DEPARTMENT_AVG_SALARY"})
employees["SALARY_CATEGORY_AMONG_DEPARTMENT"] = employees.apply(
    lambda x: "low" if x["SALARY"] < x["DEPARTMENT_AVG_SALARY"] else "high", axis=1
)

print("Employees DataFrame with new columns (first 5 rows):")
print(employees.head())
print("*" * 50)

# 5. Filter employees to include only rows where `DEPARTMENT_ID` equals 20 and store the result.
employees_dep_20 = employees[employees["DEPARTMENT_ID"] == 20].copy()
print("Employees in department 20 (first 5 rows) (few columns selected for printing):")
print(employees_dep_20[["EMPLOYEE_ID", "LAST_NAME", "SALARY", "SALARY_CATEGORY", "SALARY_CATEGORY_AMONG_DEPARTMENT"]].head())
print("*" * 50)

# 6. Increase the salary by 10% for all employees in department 20 in the filtered DataFrame.
employees_dep_20["SALARY"] = employees_dep_20["SALARY"] * 1.1

print("Employees in department 20 with 10% salary increase: here are the first 5 rows: (few columns selected for printing)")
print(employees_dep_20[["EMPLOYEE_ID", "LAST_NAME", "SALARY", "SALARY_CATEGORY", "SALARY_CATEGORY_AMONG_DEPARTMENT"]].head())
print("*" * 50)
# 6. Increase the salary by 10% for all employees in department 20 in the main DataFrame.

# Ensure SALARY column is float before multiplying, without this we will get a warning
# FutureWarning: Setting an item of incompatible dtype is deprecated and will raise in a future error of pandas
employees["SALARY"] = employees["SALARY"].astype(float)

employees.loc[employees["DEPARTMENT_ID"] == 20, "SALARY"] *= 1.1

# 7. Check if any values in the `PHONE_NUMBER` column are empty.
print("Checking if there are any empty values in the PHONE_NUMBER column:")
if employees["PHONE_NUMBER"].isna().any():
    print("There are empty values in the PHONE_NUMBER column.")
    print("these are the first 5 rows with empty PHONE_NUMBER:")
    print(employees[employees["PHONE_NUMBER"].isna()].head())
else:
    print("There are no empty values in the PHONE_NUMBER column.")
