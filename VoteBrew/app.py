import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DATABASE = 'database.db'

# Helper function to get database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name (e.g. row['name'])
    return conn

# Route to render the coffee list page
@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    # Fetch coffees ordered by most votes first
    cursor.execute('SELECT * FROM coffees ORDER BY votes DESC')
    coffees = cursor.fetchall()
    conn.close()
    return render_template('index.html', coffees=coffees)

# API Route to handle vote increments (called via AJAX)
@app.route('/vote/<int:coffee_id>', methods=['POST'])
def vote(coffee_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if this coffee exists
    cursor.execute('SELECT votes FROM coffees WHERE id = ?', (coffee_id,))
    row = cursor.fetchone()
    
    if row is None:
        conn.close()
        return jsonify({"success": False, "error": "Coffee not found"}), 404

    # Calculate new vote total
    new_votes = row['votes'] + 1
    
    # Update count in database
    cursor.execute('UPDATE coffees SET votes = ? WHERE id = ?', (new_votes, coffee_id))
    conn.commit()
    conn.close()
    
    # Return updated count as JSON to the frontend
    return jsonify({"success": True, "votes": new_votes})

if __name__ == '__main__':
    app.run(debug=True)
