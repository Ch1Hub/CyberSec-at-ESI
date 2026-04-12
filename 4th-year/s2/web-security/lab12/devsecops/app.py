import os
from flask import Flask, request
import sqlite3

app = Flask(__name__)

AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")

@app.route('/user')
def get_user():
    username = request.args.get('username')

    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        cursor.fetchall()

    return "Query executed successfully."

if __name__ == '__main__':
    app.run(host=os.environ.get("APP_HOST", "127.0.0.1"), port=int(os.environ.get("APP_PORT", "5000")))
