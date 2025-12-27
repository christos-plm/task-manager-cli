# pandas_manipulation.py - Advanced pandas data manipulation
import pandas as pd
import numpy as np

print("=" * 70)
print("PANDAS DATA MANIPULATION - TRANSFORMING DATA")
print("=" * 70)

# Load the data
df = pd.read_csv('employees.csv')
df['hire_date'] = pd.to_datetime(df['hire_date'])

# PART 1: CREATING NEW COLUMNS
print("\n1. ADDING A NEW COLUMN - Annual Bonus (10% of salary):")
print("-" * 70)

# Create a new column based on calculation
df['bonus'] = df['salary'] * 0.10

print(df[['name', 'salary', 'bonus']].head())

print("\n2. ADDING COLUMN WITH CONDITIONAL LOGIC:")
print("-" * 70)

# Create performance level based on rating
# Using np.where (like SQL CASE WHEN)
df['performance'] = np.where(df['rating'] >= 4.5, 'Excellent',
                     np.where(df['rating'] >= 4.0, 'Good', 'Needs Improvement'))

print(df[['name', 'rating', 'performance']])

print("\n3. ADDING COLUMN - Years of Service:")
print("-" * 70)

# Calculate years from hire_date to today
from datetime import datetime
today = datetime.now()
df['years_of_service'] = (today - df['hire_date']).dt.days / 365.25

print(df[['name', 'hire_date', 'years_of_service']].head())

print("\n4. ADDING COLUMN - Salary Category:")
print("-" * 70)

# Using pd.cut to create bins/categories
df['salary_category'] = pd.cut(df['salary'],
                                bins=[0, 70000, 85000, 100000],
                                labels=['Low', 'Medium', 'High'])

print(df[['name', 'salary', 'salary_category']])

# PART 2: MODIFYING EXISTING COLUMNS
print("\n5. MODIFYING - Give everyone a 5% raise:")
print("-" * 70)

print("Before raise:")
print(df[['name', 'salary']].head(3))

df['salary'] = df['salary'] * 1.05

print("\nAfter raise:")
print(df[['name', 'salary']].head(3))

print("\n6. MODIFYING - Standardize department names:")
print("-" * 70)

# Convert to uppercase
df['department'] = df['department'].str.upper()
print(df[['name', 'department']].head())

# PART 3: APPLYING FUNCTIONS
print("\n7. APPLYING CUSTOM FUNCTION - Calculate tax bracket:")
print("-" * 70)

def calculate_tax_rate(salary):
    """Calculate tax rate based on salary"""
    if salary < 75000:
        return 0.15
    elif salary < 90000:
        return 0.20
    else:
        return 0.25

df['tax_rate'] = df['salary'].apply(calculate_tax_rate)
df['estimated_tax'] = df['salary'] * df['tax_rate']

print(df[['name', 'salary', 'tax_rate', 'estimated_tax']].head())

print("\n8. APPLYING LAMBDA FUNCTION - Extract first name:")
print("-" * 70)

df['first_name'] = df['name'].apply(lambda x: x.split()[0])
print(df[['name', 'first_name']].head())

# PART 4: WORKING WITH STRINGS
print("\n9. STRING OPERATIONS - Email addresses:")
print("-" * 70)

# Create email addresses from names
df['email'] = (df['first_name'].str.lower() + '.' +
               df['name'].str.split().str[-1].str.lower() +
               '@company.com')

print(df[['name', 'email']].head())

print("\n10. STRING FILTERING - Names starting with 'A':")
print("-" * 70)

names_with_a = df[df['name'].str.startswith('A')]
print(names_with_a[['name', 'department']])

# PART 5: HANDLING MISSING DATA
print("\n11. INTRODUCING MISSING DATA (for practice):")
print("-" * 70)

# Artificially create some missing values
df_with_missing = df.copy()
df_with_missing.loc[2, 'rating'] = np.nan
df_with_missing.loc[5, 'salary'] = np.nan
df_with_missing.loc[7, 'department'] = np.nan

print("Missing values per column:")
print(df_with_missing.isnull().sum())

print("\n12. HANDLING MISSING - Fill with mean:")
print("-" * 70)

# Fill missing salary with mean salary
mean_salary = df_with_missing['salary'].mean()
df_with_missing['salary'].fillna(mean_salary, inplace=True)
print(f"Filled missing salary with mean: ${mean_salary:,.2f}")

print("\n13. HANDLING MISSING - Fill with default value:")
print("-" * 70)

# Fill missing department with 'Unknown'
df_with_missing['department'].fillna('UNKNOWN', inplace=True)
print(df_with_missing[['name', 'department']].tail())

print("\n14. HANDLING MISSING - Drop rows with missing values:")
print("-" * 70)

print(f"Rows before dropping: {len(df_with_missing)}")
df_cleaned = df_with_missing.dropna()
print(f"Rows after dropping: {len(df_cleaned)}")

# PART 6: RENAMING AND REORDERING
print("\n15. RENAMING COLUMNS:")
print("-" * 70)

df_renamed = df.rename(columns={
    'employee_id': 'id',
    'name': 'full_name',
    'hire_date': 'start_date'
})
print("New column names:", df_renamed.columns.tolist())

print("\n16. SELECTING AND REORDERING COLUMNS:")
print("-" * 70)

# Select specific columns in a specific order
df_reordered = df[['employee_id', 'first_name', 'department',
                    'salary', 'rating', 'performance']]
print(df_reordered.head())

# PART 7: AGGREGATING BY GROUPS
print("\n17. ADVANCED GROUPBY - Multiple aggregations:")
print("-" * 70)

dept_summary = df.groupby('department').agg({
    'salary': ['mean', 'min', 'max', 'count'],
    'rating': 'mean',
    'years_of_service': 'mean'
}).round(2)

print(dept_summary)

print("\n18. GROUPBY WITH CUSTOM AGGREGATION:")
print("-" * 70)

# Create a custom aggregation function
def salary_range(x):
    return x.max() - x.min()

dept_analysis = df.groupby('department').agg({
    'salary': ['mean', salary_range],
    'employee_id': 'count'
}).round(2)

print(dept_analysis)

print("\nEXERCISE 1: FLAG SENIOR EMPLOYEES:")
print("-" * 70)

# Create a column 'is_senior' that is True if years_of_service >= 4
df['is_senior'] = df['years_of_service'] >= 4

print(df[['name', 'years_of_service', 'is_senior']])

# Alternative - using np.where for more control
df['seniority_level'] = np.where(df['years_of_service'] >= 4, 'Senior', 'Junior')

print("\nWith seniority level:")
print(df[['name', 'years_of_service', 'is_senior', 'seniority_level']])

# Count senior vs junior
print(f"\nSenior employees: {df['is_senior'].sum()}")
print(f"Junior employees: {(~df['is_senior']).sum()}")

print("\nEXERCISE 2: TOTAL COMPENSATION:")
print("-" * 70)

# Calculate total compensation (salary + bonus)
df['total_comp'] = df['salary'] + df['bonus']

# Show all employees with total comp
print("All employees with total compensation:")
print(df[['name', 'salary', 'bonus', 'total_comp']].sort_values('total_comp', ascending=False))

# Show top 3 earners
print("\nTop 3 highest total compensation:")
top_3 = df.nlargest(3, 'total_comp')
print(top_3[['name', 'department', 'salary', 'bonus', 'total_comp']])

# Alternative - using sort and head
print("\nAlternative approach:")
top_3_alt = df.sort_values('total_comp', ascending=False).head(3)
print(top_3_alt[['name', 'total_comp']])

print("\nEXERCISE 3: RANK EMPLOYEES WITHIN DEPARTMENT BY SALARY:")
print("-" * 70)

# Rank by salary within each department (1 = highest)
df['dept_salary_rank'] = df.groupby('department')['salary'].rank(ascending=False, method='min')

# Show employees ranked within their department
result = df[['name', 'department', 'salary', 'dept_salary_rank']].sort_values(['department', 'dept_salary_rank'])
print(result)

print("\n#1 earners in each department:")
top_per_dept = df[df['dept_salary_rank'] == 1]
print(top_per_dept[['name', 'department', 'salary', 'dept_salary_rank']])

# Alternative - show rank as integer
df['dept_salary_rank'] = df['dept_salary_rank'].astype(int)
print("\nWith integer ranks:")
print(df[['name', 'department', 'salary', 'dept_salary_rank']].sort_values(['department', 'dept_salary_rank']))

print("\nEXERCISE 4: DATA CLEANING:")
print("-" * 70)

# 1. Remove the 'bonus' column
print("Step 1: Removing bonus column")
df = df.drop('bonus', axis=1)
print(f"Columns after dropping bonus: {df.columns.tolist()}")

# Alternative way to drop multiple columns
# df = df.drop(['bonus', 'other_col'], axis=1)

# 2. Reset department names to title case
print("\nStep 2: Fixing department names to Title Case")
print("Before:", df['department'].unique())
df['department'] = df['department'].str.title()
print("After:", df['department'].unique())

# 3. Round salary to nearest 100
print("\nStep 3: Rounding salaries to nearest 100")
print("Before:")
print(df[['name', 'salary']].head(3))

df['salary'] = (df['salary'] / 100).round() * 100

print("\nAfter:")
print(df[['name', 'salary']].head(3))

# Show cleaned data summary
print("\nCleaned dataset summary:")
print(df.info())

# Show sample of cleaned data
print("\nSample of cleaned data:")
print(df[['name', 'department', 'salary', 'rating']].head())

# PART 8: MERGING DATAFRAMES (like SQL JOIN)
print("\n19. CREATING A SECOND DATASET - Projects:")
print("-" * 70)

# Create a projects DataFrame
projects_data = {
    'employee_id': [1, 1, 3, 5, 7, 9, 2, 4],
    'project_name': ['Web Redesign', 'Mobile App', 'Marketing Campaign',
                     'Sales Dashboard', 'API Development', 'Database Migration',
                     'Mobile App', 'Content Strategy'],
    'project_budget': [50000, 75000, 30000, 40000, 60000, 45000, 75000, 25000]
}

projects = pd.DataFrame(projects_data)
print(projects)

print("\n20. INNER JOIN - Employees with their projects:")
print("-" * 70)

# Merge employees with projects (like SQL INNER JOIN)
merged = df.merge(projects, on='employee_id', how='inner')
print(merged[['first_name', 'department', 'project_name', 'project_budget']].head(10))

print("\n21. LEFT JOIN - All employees (even without projects):")
print("-" * 70)

# Left join keeps all employees
all_employees = df.merge(projects, on='employee_id', how='left')
print(f"Total rows: {len(all_employees)}")
print("\nEmployees without projects:")
no_projects = all_employees[all_employees['project_name'].isnull()]
print(no_projects[['first_name', 'department']])

print("\n22. AGGREGATING AFTER MERGE - Total budget per employee:")
print("-" * 70)

budget_summary = merged.groupby('first_name')['project_budget'].sum().reset_index()
budget_summary.columns = ['first_name', 'total_project_budget']
budget_summary = budget_summary.sort_values('total_project_budget', ascending=False)
print(budget_summary)

print("\n" + "=" * 70)
print("DATA MANIPULATION COMPLETE!")
print("=" * 70)

