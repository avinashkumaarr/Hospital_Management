import sqlite3

conn = sqlite3.connect('medilink.db')
c = conn.cursor()
c.execute("PRAGMA table_info(patient)")
for col in c.fetchall():
    print(col)
