import sqlite3

connection = sqlite3.connect('database.db')


with open('create_table.sql') as f:
    connection.executescript(f.read())
       #sql_script = f.read()
       #connection.executescript(sql_script)   
cur = connection.cursor() 

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('The newest post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
           ('The oldest post', 'hwllo')
           )
#connection.executescript(sql_script)
connection.commit()
connection.close()           
