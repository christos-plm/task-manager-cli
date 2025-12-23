# sql_aggregates_practice.py - Practice SQL aggregate functions and GROUP BY
import sqlite3

# Create a sales database
conn = sqlite3.connect('sales.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY,
        product_id INTEGER,
        quantity INTEGER,
        sale_date TEXT,
        customer_region TEXT
    )
''')

# Insert products
products = [
    (1, 'Laptop', 'Electronics', 999.99),
    (2, 'Mouse', 'Electronics', 24.99),
    (3, 'Keyboard', 'Electronics', 79.99),
    (4, 'Monitor', 'Electronics', 299.99),
    (5, 'Desk Chair', 'Furniture', 199.99),
    (6, 'Standing Desk', 'Furniture', 499.99),
    (7, 'Notebook', 'Supplies', 4.99),
    (8, 'Pen Set', 'Supplies', 12.99),
    (9, 'Webcam', 'Electronics', 89.99),
    (10, 'Bookshelf', 'Furniture', 149.99)
]
cursor.executemany('INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?)', products)

# Insert sales (more realistic data)
sales = [
    (1, 1, 2, '2024-01-15', 'North'),
    (2, 2, 5, '2024-01-16', 'South'),
    (3, 3, 3, '2024-01-16', 'North'),
    (4, 1, 1, '2024-01-17', 'East'),
    (5, 5, 2, '2024-01-18', 'West'),
    (6, 7, 10, '2024-01-18', 'North'),
    (7, 4, 1, '2024-01-19', 'South'),
    (8, 6, 1, '2024-01-20', 'East'),
    (9, 2, 8, '2024-01-20', 'North'),
    (10, 8, 5, '2024-01-21', 'West'),
    (11, 1, 3, '2024-01-22', 'South'),
    (12, 3, 2, '2024-01-22', 'North'),
    (13, 9, 4, '2024-01-23', 'East'),
    (14, 5, 1, '2024-01-24', 'West'),
    (15, 7, 15, '2024-01-25', 'South'),
    (16, 4, 2, '2024-01-25', 'North'),
    (17, 10, 3, '2024-01-26', 'East'),
    (18, 2, 6, '2024-01-27', 'West'),
    (19, 6, 2, '2024-01-28', 'North'),
    (20, 1, 1, '2024-01-28', 'South')
]
cursor.executemany('INSERT OR REPLACE INTO sales VALUES (?, ?, ?, ?, ?)', sales)

conn.commit()

print("=" * 70)
print("SALES DATABASE CREATED")
print("=" * 70)

# QUERY 1: Basic aggregates - overall statistics
print("\n1. OVERALL SALES STATISTICS:")
print("-" * 70)
cursor.execute('''
    SELECT 
        COUNT(*) as total_sales,
        SUM(quantity) as total_items_sold,
        AVG(quantity) as avg_items_per_sale
    FROM sales
''')
result = cursor.fetchone()
print(f"Total sales transactions: {result[0]}")
print(f"Total items sold: {result[1]}")
print(f"Average items per sale: {result[2]:.2f}")

# QUERY 2: Revenue by product (JOIN + aggregate)
print("\n2. TOTAL REVENUE BY PRODUCT:")
print("-" * 70)
cursor.execute('''
    SELECT 
        products.product_name,
        SUM(sales.quantity) as units_sold,
        products.price,
        SUM(sales.quantity * products.price) as total_revenue
    FROM sales
    JOIN products ON sales.product_id = products.product_id
    GROUP BY products.product_name, products.price
    ORDER BY total_revenue DESC
''')
print(f"{'Product':20} | {'Units Sold':>10} | {'Price':>10} | {'Revenue':>12}")
print("-" * 70)
for row in cursor.fetchall():
    print(f"{row[0]:20} | {row[1]:>10} | ${row[2]:>9.2f} | ${row[3]:>11,.2f}")

# QUERY 3: Sales by category
print("\n3. SALES BY PRODUCT CATEGORY:")
print("-" * 70)
cursor.execute('''
    SELECT 
        products.category,
        COUNT(sales.sale_id) as num_transactions,
        SUM(sales.quantity) as total_units,
        SUM(sales.quantity * products.price) as total_revenue
    FROM sales
    JOIN products ON sales.product_id = products.product_id
    GROUP BY products.category
    ORDER BY total_revenue DESC
''')
print(f"{'Category':15} | {'Transactions':>12} | {'Units':>10} | {'Revenue':>12}")
print("-" * 70)
for row in cursor.fetchall():
    print(f"{row[0]:15} | {row[1]:>12} | {row[2]:>10} | ${row[3]:>11,.2f}")

# QUERY 4: Sales by region
print("\n4. SALES BY CUSTOMER REGION:")
print("-" * 70)
cursor.execute('''
    SELECT 
        customer_region,
        COUNT(*) as num_sales,
        SUM(quantity) as total_items,
        ROUND(AVG(quantity), 2) as avg_items_per_sale
    FROM sales
    GROUP BY customer_region
    ORDER BY total_items DESC
''')
print(f"{'Region':10} | {'Sales':>8} | {'Items':>10} | {'Avg/Sale':>10}")
print("-" * 70)
for row in cursor.fetchall():
    print(f"{row[0]:10} | {row[1]:>8} | {row[2]:>10} | {row[3]:>10.2f}")

# QUERY 5: Top performing products (using HAVING to filter groups)
print("\n5. PRODUCTS WITH REVENUE OVER $1,000:")
print("-" * 70)
cursor.execute('''
    SELECT 
        products.product_name,
        SUM(sales.quantity * products.price) as total_revenue
    FROM sales
    JOIN products ON sales.product_id = products.product_id
    GROUP BY products.product_name
    HAVING total_revenue > 1000
    ORDER BY total_revenue DESC
''')
print(f"{'Product':20} | {'Total Revenue':>15}")
print("-" * 70)
for row in cursor.fetchall():
    print(f"{row[0]:20} | ${row[1]:>14,.2f}")

# QUERY 6: Most expensive product in each category
print("\n6. MOST EXPENSIVE PRODUCT IN EACH CATEGORY:")
print("-" * 70)
cursor.execute('''
    SELECT 
        products.category,
        products.product_name,
        products.price
    FROM products
    WHERE products.price = (
        SELECT MAX(price)
        FROM products as p2
        WHERE p2.category = products.category
    )
    ORDER BY products.category
''')
print(f"{'Category':15} | {'Product':20} | {'Price':>10}")
print("-" * 70)
for row in cursor.fetchall():
    print(f"{row[0]:15} | {row[1]:20} | ${row[2]:>9.2f}")

# QUERY 7: Electronics sales by region
print("\n7. ELECTRONICS SALES BY REGION:")
print("-" * 70)
cursor.execute('''
    SELECT 
        sales.customer_region,
        COUNT(sales.sale_id) as num_purchases,
        SUM(sales.quantity) as total_electronics_sold,
        SUM(sales.quantity * products.price) as total_revenue
    FROM sales
    JOIN products ON sales.product_id = products.product_id
    WHERE products.category = 'Electronics'
    GROUP BY sales.customer_region
    ORDER BY total_electronics_sold DESC
''')
print(f"{'Region':10} | {'Purchases':>10} | {'Units Sold':>12} | {'Revenue':>12}")
print("-" * 70)
for row in cursor.fetchall():
    print(f"{row[0]:10} | {row[1]:>10} | {row[2]:>12} | ${row[3]:>11,.2f}")

# QUERY 8: Average transaction value by region
print("\n8. AVERAGE TRANSACTION VALUE BY REGION:")
print("-" * 70)
cursor.execute('''
    SELECT 
        sales.customer_region,
        COUNT(sales.sale_id) as num_transactions,
        SUM(sales.quantity * products.price) as total_revenue,
        AVG(sales.quantity * products.price) as avg_transaction_value
    FROM sales
    JOIN products ON sales.product_id = products.product_id
    GROUP BY sales.customer_region
    ORDER BY avg_transaction_value DESC
''')
print(f"{'Region':10} | {'Transactions':>12} | {'Total Revenue':>15} | {'Avg Value':>12}")
print("-" * 70)
for row in cursor.fetchall():
    print(f"{row[0]:10} | {row[1]:>12} | ${row[2]:>14,.2f} | ${row[3]:>11,.2f}")

# QUERY 9: Products with no sales
print("\n9. PRODUCTS WITH NO SALES:")
print("-" * 70)
cursor.execute('''
    SELECT 
        products.product_name,
        products.category,
        products.price
    FROM products
    LEFT JOIN sales ON products.product_id = sales.product_id
    WHERE sales.sale_id IS NULL
    ORDER BY products.category, products.product_name
''')
result = cursor.fetchall()
if result:
    print(f"{'Product':20} | {'Category':15} | {'Price':>10}")
    print("-" * 70)
    for row in result:
        print(f"{row[0]:20} | {row[1]:15} | ${row[2]:>9.2f}")
else:
    print("All products have been sold at least once!")

conn.close()
print("\n" + "=" * 70)
print("ANALYSIS COMPLETE!")
print("=" * 70)
