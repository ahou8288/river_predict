
#-----------------------------------------------------------------------------
# Database
import sqlite3

def create_tables():
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='USER';")
    if cursor.rowcount == 0:
        conn.execute('''CREATE TABLE USER
             (id        INT AUTO_INCREMENT PRIMARY KEY,
             username   VARCHAR(20) NOT NULL,
             );''')

def insert_test_user():
    conn.execute('''INSERT INTO USER (username,password)
        VALUES
        ('Bob','cat'),
        ('Jeff','dog')''')
    conn.commit()

def sql_test():
    cursor = conn.execute('''SELECT * FROM USER''')
    display_text = cursor.fetchall()
    print(display_text)

#Open the database file
conn = sqlite3.connect('storage.db')

create_tables()
insert_test_user()
sql_test()