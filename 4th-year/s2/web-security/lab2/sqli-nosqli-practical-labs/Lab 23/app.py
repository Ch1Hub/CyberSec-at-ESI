import os
import re
from flask import Flask, request, render_template, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'nosql_blind_secret'

# --- DATA ---
# Administrator password is 'security' (8 chars, lowercase)
users_db = [
    {"username": "administrator", "password": "security", "email": "admin@example.com", "role": "admin"},
    {"username": "wiener", "password": "peter", "email": "wiener@example.com", "role": "user"},
    {"username": "carlos", "password": "montoya", "email": "carlos@example.com", "role": "user"}
]

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple login check (secure for this part)
        for user in users_db:
            if user['username'] == username and user['password'] == password:
                session['user'] = user
                return redirect(url_for('index'))
        return render_template('login.html', error="Invalid credentials")
        
    return render_template('login.html')

@app.route('/user/lookup')
def user_lookup():
    if 'user' not in session:
        return jsonify({"message": "Unauthorized"}), 403

    # --- VULNERABLE PARAMETER ---
    # The user input is injected into a JavaScript string context
    username_input = request.args.get('user', '')
    
    found_user = None

    # Simulation loop (mimics MongoDB $where scanning documents)
    for user in users_db:
        # 1. Simulate the vulnerability:
        # MongoDB Query: this.username == 'USER_INPUT'
        
        # We construct the "JS" string
        js_query = f"this.username == '{username_input}'"
        
        # 2. Transpile JS to Python for simulation
        # We need to support payloads like: 
        #   wiener' && this.password.length < 10 || 'a'=='b
        #   administrator' && this.password[0] == 's
        
        py_query = js_query
        
        # Regex replacements to mimic JS syntax in Python Eval:
        # Replace 'this.prop.length' -> len(user['prop'])
        py_query = re.sub(r"this\.([a-zA-Z0-9_]+)\.length", r"len(user['\1'])", py_query)
        
        # Replace 'this.prop' -> user['prop']
        py_query = re.sub(r"this\.([a-zA-Z0-9_]+)", r"user['\1']", py_query)
        
        # Replace operators
        py_query = py_query.replace("&&", " and ").replace("||", " or ")
        py_query = py_query.replace("true", "True").replace("false", "False")

        try:
            # 3. Evaluate
            # 'user' variable is available in the eval context
            if eval(py_query):
                found_user = user
                break # Return first match
        except Exception:
            # Syntax error in injection results in a 500 or just "not found"
            # In this lab, we return "Could not find user" if syntax breaks logic or is false
            pass

    if found_user:
        return jsonify({
            "username": found_user['username'],
            "email": found_user['email'],
            "role": found_user['role']
        })
    else:
        return jsonify({"message": "Could not find user"}), 404

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)