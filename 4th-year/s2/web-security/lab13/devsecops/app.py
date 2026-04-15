from flask import Flask, request
import os
import sqlite3

app = Flask(__name__)

@app.route('/user')
def get_user():
    username = request.args.get('username')
    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

    return "Query executed successfully."

if __name__ == '__main__':
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "5000"))
    app.run(host=host, port=port)
