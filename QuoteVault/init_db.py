import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote_text TEXT NOT NULL,
        author TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Seed data so the history isn't empty at first
cursor.execute('DELETE FROM quotes') # Clean reset

seed_quotes = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill")
]

cursor.executemany('''INSERT INTO quotes (quote_text, author) VALUES (?, ?)''', seed_quotes)

conn.commit()
conn.close()

print("Database initialized with seed data.")
