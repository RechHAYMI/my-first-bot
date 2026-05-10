import sqlite3
DB_NAME = "users.db"



def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, username TEXT)")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER, 
            amount REAL, 
            category TEXT, 
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )""")




def add_user(user_id, name, username):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO users (id, name, username) VALUES (?, ?, ?)",
                    (user_id, name, username))
    


def get_user_name(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE id = ?",
                    (user_id,))
        row = cur.fetchone()
    if row:
        return row[0]
    else:
        return "Аноним"
    


def update_user_name(user_id, new_name):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ? WHERE id = ?",
                    (new_name,user_id))



def add_expense(user_id, amount, category):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO expenses (user_id, amount, category) VALUES (?, ?, ?)",
                    (user_id, amount, category))


def get_total_expenses(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?",
                    (user_id,))
        row = cur.fetchone()
    if row and row[0]:
        return row[0]
    return 0


def get_category_stats(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT category, SUM(amount), AVG(amount) FROM expenses WHERE user_id = ? GROUP BY category",
                    (user_id,))
        row = cur.fetchall()
    return row



def delete_last_expense(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM expenses WHERE id = (SELECT MAX(id) FROM expenses WHERE user_id = ?)",
                    (user_id,))



def get_all_expenses(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT category, amount, date FROM expenses WHERE user_id = ? ORDER BY date DESC",
                    (user_id,))
        row = cur.fetchall()
    return row



def user_exists(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE user_id ?",
                    (user_id,))
        row = cur.fetchall()
    return row if not None