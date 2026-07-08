import sqlite3
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB = 'database.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# Route 1: Home page (serves index and displays history)
@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM quotes ORDER BY timestamp DESC')
    history = cursor.fetchall()

    conn.close()

    return render_template('index.html', history=history)


# Route 2: Generate random quote and save to history
@app.route('/generate', methods=['GET'])
def generate_quote():
    try:
        # Fetch a random quote from external API
        response = requests.get('https://dummyjson.com/quotes/random', timeout=5)
        response.raise_for_status()
        data = response.json()

        quote_text = data.get('quote')
        author = data.get('author')

        # Insert into SQLite Database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO quotes (quote_text, author) VALUES (?, ?)',
            (quote_text, author)
        )
        conn.commit()

        # Get the ID and timestamp of the newly inserted record
        new_id = cursor.lastrowid
        cursor.execute('SELECT timestamp FROM quotes WHERE id = ?', (new_id,))
        row = cursor.fetchone()
        timestamp = row['timestamp'] if row else ""
        conn.close()

        # Send JSON response back to AJAX
        return jsonify({
            "success": True,
            "quote": quote_text,
            "author": author,
            "timestamp": timestamp
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to fetch quote: {str(e)}"
        }), 500
    

# Route 3: Clear all history
@app.route("/clear", methods=['POST'])
def clear_history():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM quotes')

        conn.commit()
        conn.close()
        return jsonify({"success": True})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


