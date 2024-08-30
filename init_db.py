import sqlite3
import uuid

connection = sqlite3.connect('database.db')


with open('create_table.sql') as f:
    connection.executescript(f.read())
       #sql_script = f.read()
       #connection.executescript(sql_script)   
cur = connection.cursor() 


cur.execute("INSERT INTO posts (id, title) VALUES (?, ?)",
            (uuid.uuid5(uuid.UUID("fb5134a9-440b-4b75-bf5a-fd0efc9fa201"), "finance.com ").bytes, 'Finance crashes: apocalypse incoming'))
#connection.executescript(sql_script)
connection.commit()
connection.close()           
