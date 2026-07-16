import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Dict-like row access
    return conn

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    # Fetch team members from the database
    cursor.execute('SELECT * FROM team')
    members = cursor.fetchall()
    conn.close()
    return render_template('index.html', members=members)

@app.route('/update_status/<int:member_id>', methods=['POST'])
def update_status(member_id):
    data = request.get_json()
    if data is None or 'is_available' not in data:
        return jsonify({"success": False, "error": "Invalid request data"}), 400
        
    is_available = 1 if data['is_available'] else 0
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute('SELECT id FROM team WHERE id = ?', (member_id,))
    member = cursor.fetchone()
    if not member:
        conn.close()
        return jsonify({"success": False, "error": "Member not found"}), 404
        
    # Update availability
    cursor.execute('UPDATE team SET is_available = ? WHERE id = ?', (is_available, member_id))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "is_available": is_available == 1})

if __name__ == '__main__':
    app.run(debug=True)
