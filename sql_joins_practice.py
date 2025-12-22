# sql_joins_practice.py - Practice SQL JOINs
import sqlite3

# Create database
conn = sqlite3.connect('company.db')
cursor = conn.cursor()

# Create employees table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        department_id INTEGER,
        salary REAL
    )
''')

# Create departments table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY,
        department_name TEXT NOT NULL,
        location TEXT
    )
''')

# Create projects table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY,
        project_name TEXT NOT NULL,
        employee_id INTEGER,
        budget REAL
    )
''')

# Insert departments
departments = [
    (1, 'Engineering', 'San Francisco'),
    (2, 'Marketing', 'New York'),
    (3, 'Sales', 'Boston'),
    (4, 'HR', 'Chicago')
]
cursor.executemany('INSERT OR REPLACE INTO departments VALUES (?, ?, ?)', departments)

# Insert employees
employees = [
    (1, 'Alice Johnson', 1, 95000),
    (2, 'Bob Smith', 1, 85000),
    (3, 'Carol White', 2, 75000),
    (4, 'David Brown', 2, 70000),
    (5, 'Eve Davis', 3, 80000),
    (6, 'Frank Wilson', 3, 78000),
    (7, 'Grace Lee', 1, 92000),
    (8, 'Henry Chen', 4, 65000)
]
cursor.executemany('INSERT OR REPLACE INTO employees VALUES (?, ?, ?, ?)', employees)

# Insert projects
projects = [
    (1, 'Website Redesign', 1, 50000),
    (2, 'Mobile App', 2, 75000),
    (3, 'Marketing Campaign', 3, 30000),
    (4, 'Product Launch', 4, 40000),
    (5, 'Database Migration', 7, 60000),
    (6, 'Customer Survey', 5, 15000)
]
cursor.executemany('INSERT OR REPLACE INTO projects VALUES (?, ?, ?, ?)', projects)

conn.commit()

print("=" * 60)
print("DATABASE CREATED WITH SAMPLE DATA")
print("=" * 60)

# QUERY 1: Basic JOIN - Show employees with their departments
print("\n1. EMPLOYEES AND THEIR DEPARTMENTS:")
print("-" * 60)
cursor.execute('''
    SELECT employees.name, departments.department_name, employees.salary
    FROM employees
    JOIN departments ON employees.department_id = departments.department_id
    ORDER BY employees.salary DESC
''')
for row in cursor.fetchall():
    print(f"{row[0]:20} | {row[1]:15} | ${row[2]:,.2f}")

# QUERY 2: Show employees with their projects
print("\n2. EMPLOYEES AND THEIR PROJECTS:")
print("-" * 60)
cursor.execute('''
    SELECT employees.name, projects.project_name, projects.budget
    FROM employees
    JOIN projects ON employees.employee_id = projects.employee_id
    ORDER BY projects.budget DESC
''')
for row in cursor.fetchall():
    print(f"{row[0]:20} | {row[1]:25} | ${row[2]:,.2f}")

# QUERY 3: Three-table JOIN - Projects with employee names AND departments
print("\n3. PROJECTS WITH EMPLOYEE AND DEPARTMENT INFO:")
print("-" * 60)
cursor.execute('''
    SELECT 
        projects.project_name,
        employees.name,
        departments.department_name,
        projects.budget
    FROM projects
    JOIN employees ON projects.employee_id = employees.employee_id
    JOIN departments ON employees.department_id = departments.department_id
    ORDER BY projects.budget DESC
''')
for row in cursor.fetchall():
    print(f"{row[0]:25} | {row[1]:15} | {row[2]:12} | ${row[3]:,.2f}")

# QUERY 4: Calculate total salary by department
print("\n4. TOTAL SALARY BY DEPARTMENT:")
print("-" * 60)
cursor.execute('''
    SELECT 
        departments.department_name,
        COUNT(employees.employee_id) as employee_count,
        SUM(employees.salary) as total_salary,
        AVG(employees.salary) as avg_salary
    FROM departments
    JOIN employees ON departments.department_id = employees.department_id
    GROUP BY departments.department_name
    ORDER BY total_salary DESC
''')
for row in cursor.fetchall():
    print(f"{row[0]:15} | Employees: {row[1]} | Total: ${row[2]:,.2f} | Avg: ${row[3]:,.2f}")

# QUERY 5: Show all employees in the Engineering Department
print("\n5. EMPLOYEES IN THE ENGINEERING DEPARTMENT:")
print("-" * 60)
cursor.execute('''
    SELECT
        employees.name, employees.salary
    FROM employees
    JOIN departments ON employees.department_id=departments.department_id
    WHERE departments.department_name = 'Engineering'
    ORDER BY employees.salary DESC
''')
for row in cursor.fetchall():
    print(f"{row[0]:20} | ${row[1]:,.2f}")

# QUERY 6: Show the employee working on the most expensive project
print("\n6. EMPLOYEE WORKING ON THE MOST EXPENSIVE PROJECT:")
print("-" * 60)
cursor.execute('''
    SELECT
        employees.name,
        projects.project_name,
        projects.budget
    FROM employees
    JOIN projects ON employees.employee_id=projects.employee_id
    ORDER BY projects.budget DESC
    LIMIT 1
''')
result = cursor.fetchone()
if result:
    print(f"Employee: {result[0]}")
    print(f"Project: {result[1]}")
    print(f"Budget: ${result[2]:,.2f}")

# QUERY 7: Show total project budget by department
print("\n7. TOTAL PROJECT BUDGET BY DEPARTMENT:")
print("-" * 60)
cursor.execute('''
    SELECT 
        departments.department_name,
        COUNT(projects.project_id) as project_count,
        SUM(projects.budget) as total_budget
    FROM departments
    JOIN employees ON departments.department_id = employees.department_id
    JOIN projects ON employees.employee_id = projects.employee_id
    GROUP BY departments.department_name
    ORDER BY total_budget DESC
''')
for row in cursor.fetchall():
    print(f"{row[0]:15} | Projects: {row[1]} | Total Budget: ${row[2]:,.2f}")

# QUERY 8: Show employees who don't have any projects
print("\n7. EMPLOYEES WHO DON'T HAVE ANY PROJECTS:")
print("-" * 60)
cursor.execute('''
    SELECT
        employees.name,
        departments.department_name
    FROM employees
    LEFT JOIN projects ON employees.employee_id=projects.employee_id
    LEFT JOIN departments ON employees.department_id=departments.department_id
    WHERE projects.project_id IS NULL
''')
for row in cursor.fetchall():
    print(f"{row[0]:20} | {row[1]:15}")

conn.close()
print("\n" + "=" * 60)
print("PRACTICE COMPLETE!")
print("=" * 60)
