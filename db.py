import sqlite3

conn = sqlite3.connect("API_DATA.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        response_time REAL,
        status_code INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
conn.close()
print("DB Ready")
