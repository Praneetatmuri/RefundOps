import sqlite3
import hashlib
import os

DB_NAME = "refundops.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT,
            gmail_email TEXT,
            gmail_app_pass TEXT
        )
    ''')
    # Stats Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            key TEXT PRIMARY KEY,
            value INTEGER
        )
    ''')
    # Bot State Table (For Human-in-the-Loop)
    c.execute('''
        CREATE TABLE IF NOT EXISTS bot_state (
            key TEXT PRIMARY KEY,
            value TEXT,
            payload TEXT
        )
    ''')
    # Initialize 'current_action'
    c.execute("INSERT OR IGNORE INTO bot_state (key, value, payload) VALUES ('current_action', 'IDLE', '{}')")



    # Initialize 'refund_count' if not exists
    c.execute("INSERT OR IGNORE INTO stats (key, value) VALUES ('refund_count', 0)")
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, gmail, app_pass):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        hashed = hash_password(password)
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, hashed, gmail, app_pass))
        conn.commit()
        conn.close()
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    except Exception as e:
        return False, str(e)

def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    hashed = hash_password(password)
    c.execute("SELECT gmail_email, gmail_app_pass FROM users WHERE username=? AND password_hash=?", (username, hashed))
    result = c.fetchone()
    conn.close()
    if result:
        return True, result[0], result[1] # Return gmail, app_pass
    return False, None, None

def increment_refund_count():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("UPDATE stats SET value = value + 1 WHERE key = 'refund_count'")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"DB Error: {e}")
        return False

def get_stats():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT value FROM stats WHERE key = 'refund_count'")
        result = c.fetchone()
        conn.close()
        count = result[0] if result else 0
        return {
            "refunds_processed": count,
            "time_saved_minutes": count * 8,  # Assume 8 mins per refund
            "money_saved_inr": count * 4500   # Assume ₹4,500 per refund
        }
    except Exception as e:
        print(f"Stats Error: {e}")
        return {"refunds_processed": 0, "time_saved_minutes": 0, "money_saved_inr": 0}

# --- BOT STATE MANAGEMENT ---
def set_bot_state(status, payload):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        import json
        payload_str = json.dumps(payload)
        c.execute("UPDATE bot_state SET value = ?, payload = ? WHERE key = 'current_action'", (status, payload_str))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"DB Error: {e}")
        return False

def get_bot_state():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT value, payload FROM bot_state WHERE key = 'current_action'")
        result = c.fetchone()
        conn.close()
        if result:
            import json
            return {"status": result[0], "payload": json.loads(result[1])}
        return {"status": "IDLE", "payload": {}}
    except Exception:
        return {"status": "IDLE", "payload": {}}

def set_user_decision(decision):
    try:
        current = get_bot_state()
        payload = current.get("payload", {})
        payload["decision"] = decision
        set_bot_state(current["status"], payload)
        return True
    except:
        return False

