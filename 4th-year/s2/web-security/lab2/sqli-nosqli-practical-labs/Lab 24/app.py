import os
import re
from flask import Flask, request, render_template, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'nosql_unknown_fields_secret'

# --- DATA ---
# User 'djamel' has a hidden field 'resetToken'.
# Attackers must find the NAME of the field ('resetToken') then the VALUE.
users_db = [
    {
        "username": "djamel", 
        "password": "old_password", 
        "email": "djamel@example.com",
        "resetToken": "a1b2c3d4",  # The hidden field to exfiltrate
        "role": "user",
        "account_locked": True     # Simulating the 'Account locked' state mentioned in the lab
    },
    {
        "username": "wiener", 
        "password": "peter", 
        "email": "wiener@example.com", 
        "role": "user",
        "account_locked": False
    }
]

# --- HELPER: Transpile JS Injection to Python ---
def evaluate_js_injection(js_query, user_doc):
    """
    Simulates MongoDB $where execution by converting JS syntax to Python.
    Supported payloads:
    - Object.keys(this)[1].match('^.{0}a.*')
    - this.resetToken.match('^.{0}a.*')
    - '0' or '1'
    """
    try:
        # 1. Simple Boolean cases ('0', '1')
        if js_query.strip() == '0': return False
        if js_query.strip() == '1': return True

        # 2. Convert 'this' to 'user_doc'
        # We handle 'Object.keys(this)' first
        py_query = js_query.replace("Object.keys(this)", "list(user_doc.keys())")
        
        # We handle direct property access 'this.prop'
        py_query = py_query.replace("this.", "user_doc.")
        
        # 3. Handle JavaScript .match('regex')
        # We convert:  ENTITY.match('REGEX')  -->  re.search('REGEX', ENTITY)
        # Regex explanation: Capture entity before .match, capture regex inside quotes
        
        # Pattern for: something.match('pattern')
        match_pattern = r"([a-zA-Z0-9_\[\]\(\)\.]+)\.match\('([^']*)'\)"
        
        # We need a loop to handle multiple matches if necessary, but usually there's one.
        # Replacement: re.search('pattern', something)
        if ".match" in py_query:
            py_query = re.sub(match_pattern, r"re.search('\2', \1)", py_query)

        # 4. Preparing the eval context
        # We need to make sure accessing user_doc.field works. 
        # But 'user_doc' is a dict. user_doc.field is not valid python. user_doc['field'] is.
        # Quick fix: We wrap the dict in a simple class for dot notation access just for eval
        class DotDict(dict):
            __getattr__ = dict.get
            
        context_user = DotDict(user_doc)
        
        # Evaluate
        # Note: re is needed in eval context
        return eval(py_query, {"re": re, "user_doc": context_user, "list": list})

    except Exception as e:
        # If syntax error or index out of range (during enumeration), return False (mimic Mongo error)
        return False

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # --- VULNERABLE ENDPOINT ---
    data = request.get_json(silent=True)
    if not data: return jsonify({"message": "Invalid request"}), 400

    username_in = data.get('username')
    password_in = data.get('password')
    where_in    = data.get('$where') # The injection point

    # 1. Find User
    target_user = next((u for u in users_db if u['username'] == username_in), None)
    
    if not target_user:
        return jsonify({"message": "Invalid username or password"}), 200

    # 2. Check Password (supporting $ne injection)
    password_match = False
    if isinstance(password_in, dict) and '$ne' in password_in:
        if target_user['password'] != password_in['$ne']:
            password_match = True
    elif target_user['password'] == password_in:
        password_match = True

    # 3. Check $where Injection (If provided)
    where_match = True
    if where_in:
        where_match = evaluate_js_injection(where_in, target_user)

    # 4. Final Decision Logic (Mimicking Lab Behavior)
    if password_match and where_match:
        # In the lab, if we bypass auth for Djamel, we see "Account locked"
        if target_user.get('account_locked'):
            return jsonify({"message": "Account locked"}), 200
        else:
            # Login success for others
            session['user'] = target_user['username']
            return jsonify({"message": "Login successful", "redirect": "/"}), 200
    
    return jsonify({"message": "Invalid username or password"}), 200

@app.route('/forgot-password', methods=['GET'])
def forgot_password():
    # Vulnerable logic: We check if any parameter key matches a hidden field name?
    # Actually, the lab says: GET /forgot-password?resetToken=invalid -> "Invalid token"
    # GET /forgot-password?foo=invalid -> Standard page
    
    # Check for the correct parameter name presence
    if 'resetToken' in request.args:
        token_val = request.args.get('resetToken')
        user = next((u for u in users_db if u.get('resetToken') == token_val), None)
        
        if user:
            # Token valid, show reset form
            return render_template('reset.html', token=token_val, user=user['username'])
        else:
            return "Invalid token", 400 # The signal that parameter name is correct but value wrong
            
    return render_template('forgot.html')

@app.route('/reset', methods=['POST'])
def reset():
    token = request.form.get('token')
    new_pass = request.form.get('new_password')
    
    user = next((u for u in users_db if u.get('resetToken') == token), None)
    if user:
        user['password'] = new_pass
        user['account_locked'] = False # Unlock account
        return "Password reset! You can now login."
    return "Error."

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)