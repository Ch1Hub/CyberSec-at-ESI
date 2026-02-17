import os
import re
from flask import Flask, request, render_template

app = Flask(__name__)
app.secret_key = 'nosql_secret'

# --- SIMULATED MONGODB COLLECTION ---
# Note: "released": False means it shouldn't be seen normally.
products_db = [
    {"id": 1, "name": "Corporate Gift Basket", "category": "Gifts", "released": True, "description": "Perfect for clients."},
    {"id": 2, "name": "Mystery Box", "category": "Gifts", "released": False, "description": "Contains unreleased prototypes."},
    {"id": 3, "name": "USB Gadget", "category": "Tech", "released": True, "description": "Useful tech."},
    {"id": 4, "name": "Smart Watch v2", "category": "Tech", "released": False, "description": "Next gen watch."},
    {"id": 5, "name": "Office Chair", "category": "Furniture", "released": True, "description": "Ergonomic."},
]

@app.route('/')
def index():
    category = request.args.get('category', 'Gifts')
    
    # --- VULNERABLE CODE SIMULATION ---
    # Scenario: The developer is using a $where clause (JavaScript) 
    # query = "this.category == '" + category + "'"
    
    results = []
    error_msg = None

    for prod in products_db:
        # 1. Construct the Vulnerable Query String
        # In a real Mongo $where injection, the server executes: this.category == 'USER_INPUT'
        # We simulate 'this' context using the product dict
        
        # NOTE: We construct the raw string to mimic the injection surface
        js_query = f"'{prod['category']}' == '{category}'"
        
        # 2. Syntax Translation (JS to Python) for simulation purposes
        # The user will inject JS syntax (||, &&). Python needs 'or', 'and'.
        # We replace them to allow the exploit to work in this simulated environment.
        py_query = js_query.replace("||", " or ").replace("&&", " and ")
        
        # 3. Execution
        try:
            # We enforce a constraint: Normally, the app appends " && this.released == true"
            # BUT, usually in these labs, if you inject "|| 1 ||", you short-circuit everything.
            # Let's assume the developer logic is:
            # if (eval(query) AND product.released): show()
            # BUT the vulnerability allows overriding the logic if the query itself handles the logic.
            
            # To match the lab solution exactly: 
            # The injection "Gifts'||1||'" results in "category == 'Gifts' || 1 || ''"
            # This evaluates to TRUE for ALL items.
            
            is_match = eval(py_query)
            
            # Logic of the lab: 
            # Ideally, the server adds " && released" automatically.
            # However, if the user injects a payload that makes the WHOLE statement true,
            # or if the "released" check is part of the WHERE clause that got messed up.
            
            # For this simulation, if the Injection is detected (always True), we show everything.
            if is_match:
                 # Check 'released' ONLY if the query didn't force a "True" bypass
                 # If the user injected "|| 1", is_match is True.
                 # In a real specific Mongo case, we might see unreleased items.
                 # Let's simulate: If the query evaluates to True, we verify 'released'.
                 # UNLESS the injection broke the logic.
                 
                 # Simplification for the Lab goal:
                 # If the user performed the specific injection "||1||", we show hidden items.
                 if " or 1 or " in py_query or " or 1" in py_query:
                     results.append(prod)
                 elif prod['released']:
                     results.append(prod)
                     
        except SyntaxError:
            # This simulates the "JavaScript syntax error" mentioned in the lab
            error_msg = "SyntaxError: Unexpected token ILLEGAL (MongoDB execution failed)"
            break
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            break

    return render_template('index.html', products=results, error=error_msg, current_cat=category)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)