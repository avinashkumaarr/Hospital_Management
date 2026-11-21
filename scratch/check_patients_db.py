import sqlite3

conn = sqlite3.connect('medilink.db')
c = conn.cursor()
c.execute("SELECT aadhaar_number, full_name, mobile FROM patient")
for row in c.fetchall():
    print(row)
