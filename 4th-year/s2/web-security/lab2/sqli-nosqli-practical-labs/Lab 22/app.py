import os
import re
from flask import Flask, request, render_template, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'nosql_auth_secret'

# --- SIMULATED MONGODB USERS COLLECTION ---
# Administrator is first, simulating standard DB indexing where finding "first match" gets admin.
users_db = [
    {"username": "administrator", "password": "s3cr3t_admin_password_x99", "role": "admin"},
    {"username": "wiener", "password": "peter", "role": "user"},
    {"username": "carlos", "password": "montoya_password", "role": "user"}
]

# --- HELPER: SIMULATE MONGODB QUERY MATCHING ---
def mongo_match(doc_value, query_value):
    """
    Checks if a document field matches the query value, 
    handling MongoDB operators: $ne (not equal), $regex.
    """
    # 1. If query is a dictionary (Potential Operator Injection)
    if isinstance(query_value, dict):
        # Handle $ne (Not Equal)
        if '$ne' in query_value:
            return doc_value != query_value['$ne']
        
        # Handle $regex (Regular Expression)
        if '$regex' in query_value:
            try:
                pattern = query_value['$regex']
                return re.search(pattern, doc_value) is not None
            except re.error:
                return False
                
        # (Other operators like $gt could be added here)
        return False

    # 2. Standard exact match (String vs String)
    return doc_value == query_value

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # --- VULNERABLE CODE ---
    # The application accepts JSON directly and passes it to the query engine.
    
    # 1. Parse Input (Expecting JSON usually for NoSQL apps)
    data = request.get_json(silent=True)
    
    # Fallback to form data if JSON not provided (to mimic standard login behavior initially)
    if not data:
        data = {
            "username": request.form.get("username"),
            "password": request.form.get("password")
        }

    username_query = data.get('username')
    password_query = data.get('password')

    # 2. Execute Query (Simulated db.users.findOne({...}))
    logged_in_user = None
    
    for user in users_db:
        # Check Username AND Password using our Mongo Simulator
        # This allows injecting {"$ne": ""} into username_query or password_query
        match_user = mongo_match(user['username'], username_query)
        match_pass = mongo_match(user['password'], password_query)
        
        if match_user and match_pass:
            logged_in_user = user
            break # findOne stops at first match

    if logged_in_user:
        session['user'] = logged_in_user['username']
        return jsonify({"status": "success", "redirect": "/"})
    else:
        return jsonify({"status": "fail", "message": "Invalid username or password"}), 401

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)