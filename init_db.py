import sqlite3

def start():
    connection = sqlite3.connect('database.db')
    setup ="""DROP TABLE IF EXISTS posts;
    DROP TABLE IF EXISTS comments;

    CREATE TABLE posts (
        id VARCHAR(200) PRIMARY KEY,
        title TEXT NOT NULL,
        link VARCHAR(2083)
    );

    CREATE TABLE comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user VARCHAR(20) NOT NULL,
        body TEXT NOT NULL,
        post VARCHAR(200) NOT NULL,
        created DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(post) REFERENCES posts(id)
    );

    """
    # with open('create_table.sql') as f:
    connection.executescript(setup)
    connection.close()

def populate():
    connection = sqlite3.connect('database.db')
    cur = connection.cursor() 
    cur.execute("INSERT INTO posts (id, title, link) VALUES (?, ?, ?)",
            ("asd", 'Finance crashes: apocalypse incoming', "bbc.co.uk"))
    cur.execute("INSERT INTO comments (user, body, post) VALUES (?, ?, ?)",
            ("Fritz John", 'No my savings are gone :(', "asd"))
    cur.execute("INSERT INTO comments (user, body, post) VALUES (?, ?, ?)",
            ("Thomas Blomp", 'I soiled my pants', "asd"))
    connection.close()


if __name__== '__main__':
    start()
    populate()