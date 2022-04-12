import os
import sqlite3


# create a database called name_database.db
# add one table to the database called names_table
# add columns to the database table: Id, first_name, last_name, age

conn = sqlite3.connect('data.db')
cur = conn.cursor()
cur.execute("SELECT * FROM data")

record = cur.fetchall()
for row in record:
    print(row)
cur.close()
conn.close()


