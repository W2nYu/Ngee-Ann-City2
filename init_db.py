import sqlite3

print('running file')
connection = sqlite3.connect('ngeeanncity.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()

print('ended')
