# sql_practice.py - Practicing SQL with Python
import sqlite3

# Create a connection to a database (creates file if doesn't exist)
conn = sqlite3.connect('practice.db')
cursor = conn.cursor()

# Create a table for storing books
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER,
        rating REAL
    )
''')

# Insert some sample books
books_data = [
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 4.2),
    ('To Kill a Mockingbird', 'Harper Lee', 1960, 4.5),
    ('1984', 'George Orwell', 1949, 4.6),
    ('Pride and Prejudice', 'Jane Austen', 1813, 4.3),
    ('The Catcher in the Rye', 'J.D. Salinger', 1951, 3.8),
]

cursor.executemany('INSERT INTO books (title, author, year, rating) VALUES (?, ?, ?, ?)', books_data)
conn.commit()

print("=== All Books ===")
cursor.execute('SELECT * FROM books')
for row in cursor.fetchall():
    print(row)

print("\n=== Books published after 1950 ===")
cursor.execute('SELECT title, author, year FROM books WHERE year > 1950')
for row in cursor.fetchall():
    print(f"{row[0]} by {row[1]} ({row[2]})")

print("\n=== Books with rating above 4.0, sorted by rating ===")
cursor.execute('SELECT title, rating FROM books WHERE rating > 4.0 ORDER BY rating DESC')
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} stars")

print("\n=== Count of books ===")
cursor.execute('SELECT COUNT(*) FROM books')
count = cursor.fetchone()[0]
print(f"Total books: {count}")

print("\n=== Average rating ===")
cursor.execute('SELECT AVG(rating) FROM books')
avg_rating = cursor.fetchone()[0]
print(f"Average rating: {avg_rating:.2f}")

cursor.execute('INSERT INTO books (title, author, year, rating) VALUES (?, ?, ?, ?)', ('Ulysses', 'James Joyce', 1920, 3.8))
conn.commit()
print("\n=== Added a book ===\n")

print("=== All Books ===")
cursor.execute('SELECT * FROM books')
for row in cursor.fetchall():
    print(row)

print("\n=== Books by George Orwell ===")
cursor.execute('SELECT title FROM books WHERE author = "George Orwell"')
for row in cursor.fetchall():
    print(f"{row[0]}")

cursor.execute('UPDATE books SET rating = ? WHERE title = ?', (5.0, '1984'))
conn.commit()
print("\n=== Updated 1984 rating ===\n")

print("=== All Books ===")
cursor.execute('SELECT * FROM books')
for row in cursor.fetchall():
    print(row)

print("\n=== Average rating ===")
cursor.execute('SELECT AVG(rating) FROM books')
avg_rating = cursor.fetchone()[0]
print(f"Average rating: {avg_rating:.2f}")

cursor.execute('DELETE FROM books WHERE title = ?', ('Ulysses',))
conn.commit()
print("\n=== Deleted a book ===\n")

print("=== All Books ===")
cursor.execute('SELECT * FROM books')
for row in cursor.fetchall():
    print(row)

print("\n=== The oldest book in the DB ===")
cursor.execute('SELECT title, year FROM books ORDER BY year LIMIT 1')
for row in cursor.fetchall():
    print(f"{row[0]} published in {row[1]}")

# Close the connection
conn.close()
print("\nDatabase connection closed!")

