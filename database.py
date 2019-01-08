import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

insert_query = "INSERT INTO users VALUES(NULL, ?, ?)"

"""
users = [
    ('Kraken', 'asdf'),
    ('Rahul', 'abcd')
]

cursor.executemany(insert_query, users)
"""


select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
