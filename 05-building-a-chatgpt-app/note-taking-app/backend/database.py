import sqlite3

DB_PATH = "notes.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def execute_query(query, params=(), one=False):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query, params)
    if query.strip().upper().startswith("SELECT"):
        rv = c.fetchall()
        conn.close()
        return (rv[0] if rv else None) if one else rv
    else:
        conn.commit()
        # Return rows affected for UPDATE/DELETE, lastrowid for INSERT
        if query.strip().upper().startswith("INSERT"):
            result = c.lastrowid
        else:  # UPDATE or DELETE
            result = c.rowcount
        conn.close()
        return result
