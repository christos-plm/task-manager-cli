# pandas_basics.py - Learning pandas fundamentals
import pandas as pd

print("=" * 70)
print("PANDAS BASICS - LEARNING DATA ANALYSIS")
print("=" * 70)

# PART 1: Loading data
print("\n1. LOADING CSV FILE:")
print("-" * 70)

# Read CSV file into a DataFrame
df = pd.read_csv('employees.csv')
print("✓ Data loaded successfully!")
print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")

# PART 2: Viewing data
print("\n2. FIRST 5 ROWS (head):")
print("-" * 70)
print(df.head())

print("\n3. LAST 5 ROWS (tail):")
print("-" * 70)
print(df.tail(3))  # Show last 3 rows

# PART 3: Basic information about the dataset
print("\n4. DATASET INFO:")
print("-" * 70)
print(df.info())

print("\n5. COLUMN NAMES:")
print("-" * 70)
print(df.columns.tolist())

print("\n6. SUMMARY STATISTICS:")
print("-" * 70)
print(df.describe())

# PART 4: Accessing columns
print("\n7. ACCESSING A SINGLE COLUMN:")
print("-" * 70)
print(df['name'])  # Returns a Series

print("\n8. ACCESSING MULTIPLE COLUMNS:")
print("-" * 70)
print(df[['name', 'department', 'salary']])

# PART 5: Filtering data (like SQL WHERE)
print("\n9. FILTERING - EMPLOYEES IN ENGINEERING:")
print("-" * 70)
engineering = df[df['department'] == 'Engineering']
print(engineering[['name', 'salary']])

print("\n10. FILTERING - SALARIES ABOVE $80,000:")
print("-" * 70)
high_earners = df[df['salary'] > 80000]
print(high_earners[['name', 'department', 'salary']])

print("\n11. MULTIPLE CONDITIONS (AND):")
print("-" * 70)
# Engineering employees making over $85,000
filtered = df[(df['department'] == 'Engineering') & (df['salary'] > 85000)]
print(filtered[['name', 'salary']])

# PART 6: Sorting (like SQL ORDER BY)
print("\n12. SORTING BY SALARY (highest first):")
print("-" * 70)
sorted_df = df.sort_values('salary', ascending=False)
print(sorted_df[['name', 'salary']].head())

print("\n13. SORTING BY MULTIPLE COLUMNS:")
print("-" * 70)
sorted_df = df.sort_values(['department', 'salary'], ascending=[True, False])
print(sorted_df[['name', 'department', 'salary']])

# PART 7: Basic calculations
print("\n14. CALCULATING - AVERAGE SALARY:")
print("-" * 70)
avg_salary = df['salary'].mean()
print(f"Average salary: ${avg_salary:,.2f}")

print("\n15. CALCULATING - MAX, MIN, SUM:")
print("-" * 70)
print(f"Highest salary: ${df['salary'].max():,.2f}")
print(f"Lowest salary: ${df['salary'].min():,.2f}")
print(f"Total payroll: ${df['salary'].sum():,.2f}")
print(f"Median salary: ${df['salary'].median():,.2f}")

# PART 8: Grouping (like SQL GROUP BY)
print("\n16. GROUP BY DEPARTMENT:")
print("-" * 70)
grouped = df.groupby('department')['salary'].agg(['count', 'mean', 'sum'])
print(grouped)

print("\n17. GROUP BY WITH MULTIPLE AGGREGATIONS:")
print("-" * 70)
grouped = df.groupby('department').agg({
    'salary': ['mean', 'max', 'min'],
    'rating': 'mean',
    'employee_id': 'count'
})
print(grouped)

print("\nEXERCISE 1: HIGHEST RATED EMPLOYEE:")
print("-" * 70)
highest_rated = df.sort_values('rating', ascending=False).head(1)
print(highest_rated[['name', 'department', 'rating']])

# Alternative solution - more explicit
print("\nAlternative approach:")
highest_rated_employee = df[df['rating'] == df['rating'].max()]
print(highest_rated_employee[['name', 'department', 'rating']])

print("\nEXERCISE 2: EMPLOYEE COUNT BY DEPARTMENT:")
print("-" * 70)

# Method 1: Using value_counts()
print("Method 1 - value_counts():")
print(df['department'].value_counts())

print("\nMethod 2 - groupby with size():")
department_counts = df.groupby('department').size()
print(department_counts)

print("\nMethod 3 - groupby with count():")
department_counts = df.groupby('department')['employee_id'].count()
print(department_counts)

print("\nMethod 4 - As a DataFrame with sorted results:")
department_counts = df.groupby('department').size().reset_index(name='employee_count')
department_counts = department_counts.sort_values('employee_count', ascending=False)
print(department_counts)

print("\nEXERCISE 3: RECENT MARKETING HIRES:")
print("-" * 70)

# First, let's convert hire_date to datetime for proper comparison
df['hire_date'] = pd.to_datetime(df['hire_date'])

# Filter for Marketing AND hired after 2020
recent_marketing = df[
    (df['department'] == 'Marketing') &
    (df['hire_date'] > '2020-12-31')
]

print(recent_marketing[['name', 'department', 'hire_date', 'salary']])

# Alternative: Extract year and compare
print("\nAlternative - using year extraction:")
df['hire_year'] = df['hire_date'].dt.year
recent_marketing = df[
    (df['department'] == 'Marketing') &
    (df['hire_year'] > 2020)
]
print(recent_marketing[['name', 'department', 'hire_date', 'hire_year', 'salary']])

print("\n" + "=" * 70)
print("PANDAS BASICS COMPLETE!")
print("=" * 70)
