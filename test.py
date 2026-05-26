import sqlite3

conn = sqlite3.connect("test.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER, name TEXT)")
c.execute("INSERT INTO test VALUES (1, 'Sannvi')")
conn.commit()
conn.close()
print("DB created and row inserted!")
