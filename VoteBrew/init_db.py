import sqlite3

# Connection to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS coffees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        votes INTEGER DEFAULT 0,
        image_url TEXT
    )
''')

# Clear existing entries if any, to reset cleanly
cursor.execute('DELETE FROM coffees')

# Seed data
coffees_data = [
    ("Vanilla Latte", "Creamy espresso latte infused with sweet vanilla notes and topped with smooth steamed milk.", 95, "https://images.unsplash.com/photo-1683122925249-8b15d807db4b?q=80&w=730&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
    ("Mocha", "Espresso mixed with creamy milk and chocolate for a sweet, velvety flavor.", 95, "https://images.unsplash.com/photo-1578314675249-a6910f80cc4e?auto=format&fit=crop&w=400&h=400&q=80"),
    ("Flat White", "Velvety microfoam with rich espresso flavor.", 88, "https://plus.unsplash.com/premium_photo-1674327105076-36c4419864cf?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
    ("Caramel Macchiato", "Espresso layered with milk and caramel.", 110, "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
    ("Nitro Cold Brew", "Cold brew infused with nitrogen for a creamy texture.", 135, "https://images.unsplash.com/photo-1626436273393-27c3ec1548a9?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
    ("Colombian Supremo", "Balanced sweetness with chocolate undertones.", 102, "https://images.unsplash.com/photo-1598811465492-4138d1f4fbee?q=80&w=880&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
]

# Insert seeds
cursor.executemany('''
    INSERT INTO coffees (name, description, votes, image_url)
    VALUES (?, ?, ?, ?)
''', coffees_data)

conn.commit()
conn.close()
print("Database initialized and seeded successfully!")
