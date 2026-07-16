import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Drop existing table if starting fresh
    cursor.execute('DROP TABLE IF EXISTS team')
    
    # Create the team availability table
    cursor.execute('''
        CREATE TABLE team (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            is_available INTEGER NOT NULL DEFAULT 1
        )
    ''')
    
    # Core seed data as shown in design mockup
    mock_members = [
        ("Alex Rivers", "Senior Developer", 1),
        ("Samantha Chen", "UX Designer", 0),
        ("Jordan Taylor", "Project Manager", 1),
        ("Maria Garcia", "Marketing Lead", 0),
        ("Lucas Bennett", "Backend Engineer", 1)
    ]
    
    cursor.executemany(
        'INSERT INTO team (name, role, is_available) VALUES (?, ?, ?)', 
        mock_members
    )
    
    conn.commit()
    conn.close()
    print("Database initialized and populated with team availability data successfully!")

if __name__ == '__main__':
    init_db()
