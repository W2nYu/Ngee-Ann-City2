import sqlite3

print('running file')
connection = sqlite3.connect('ngeeanncity.db')

# with open('schema.sql') as f:
#     connection.executescript(f.read())
res = connection.execute("Select * From saved_games").fetchall()
print(res)

# cur = connection.cursor()

# connection.commit()
connection.close()

print('ended')
