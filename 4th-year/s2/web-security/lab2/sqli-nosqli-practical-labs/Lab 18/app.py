import sqlite3
from flask import Flask, request

app = Flask(__name__)
conn = sqlite3.connect(':memory:', check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE secret (flag TEXT)")
c.execute("INSERT INTO secret VALUES ('FLAG{N0_SP4C3S_ALLOWED_H3R3}')")

@app.route('/')
def index():
    uid = request.args.get('id', '')
    
    # --- WAF ---
    if ' ' in uid:
        return "WAF BLOCKED: Spaces are forbidden!", 403
    if 'UNION' in uid.upper():
        return "WAF BLOCKED: UNION keyword forbidden!", 403
        
    # La solution est d'utiliser /**/ (mais python sqlite ne supporte pas tjrs les commentaires inline standard comme MySQL)
    # Astuce pour ce lab: utiliser des Tabulations (%09) ou des sauts de ligne (%0A) qui ne sont pas des espaces ' '
    
    try:
        # On nettoie juste pour la forme, mais le filtre ci-dessus est le vrai challenge
        query = f"SELECT * FROM secret WHERE rowid = {uid}"
        c.execute(query)
        res = c.fetchone()
        if res:
            return f"Result: {res[0]}"
        return "No result"
    except Exception as e:
        return f"Error (Blind?): {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)