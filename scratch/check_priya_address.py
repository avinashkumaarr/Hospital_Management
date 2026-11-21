import sqlite3

conn = sqlite3.connect('medilink.db')
c = conn.cursor()
c.execute("SELECT aadhaar_number, full_name, address FROM patient WHERE full_name LIKE '%Priya%'")
print(c.fetchall())
