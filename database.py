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

    conn.commit()

    conn.close()