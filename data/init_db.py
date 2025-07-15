import sqlite3

conn = sqlite3.connect("data/database.sqlite3")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostname TEXT NOT NULL,
    ip TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    monitor_command TEXT DEFAULT 'uptime'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER,
    message TEXT,
    severity TEXT,
    timestamp TEXT,
    status TEXT,
    FOREIGN KEY (device_id) REFERENCES devices(id)
)
""")

conn.commit()
conn.close()