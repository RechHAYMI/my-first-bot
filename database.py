import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, username TEXT)")

    conn.commit()

    conn.close()

def add_user(user_id, name, username):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (id, name, username) VALUES (?, ?, ?)",
                (user_id, name, username))
    
def get_user_name(user_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM users WHERE id = ?",
                (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return row[0]
    else:
        return "Аноним"
    
def update_user_name(user_id, new_name):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("UPDATE users SET name = ? WHERE id = ?",
                (new_name,user_id))
    conn.commit()
    conn.close()