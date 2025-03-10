import sqlite3


connection = sqlite3.connect('music_rows.db')

cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Rows (name TEXT NOT NULL,
row TEXT NOT NULL
)
''')

cursor.execute('INSERT INTO Rows VALUES ("Гимн Российской Федерации", "5 -5 2 2 -7 5 -2 -2 2 -7 2 2 1 2 2 2 1 2 -7 9 -2 -2 2 -3 -4 5 -1 -2 2 -7 5 -2 -2 2 -7 12 -1 -2 -2")')
cursor.execute('INSERT INTO Rows VALUES ("В лесу родилась ёлочка", "9 -2 2 -4 -5 9 1 -3 5 -10 8 -1 -2 -2 -5 9 -2 2 -4 7 -10 8 -1 -2 -2 -5 9 -2 2 -4")')
cursor.execute('INSERT INTO Rows VALUES ("А знаешь, всё ещё будет", "9 -2 2 1 -1 -9 9 -2 2 -2 -2 1 1 2 3 -2 -1 -2 -2 2 -7 9 -2 2 1 -1 -9 9 -2 2 -2 -2 1 1 2 3 -2 -1 -2 -2 2 2 -2 -2")')
cursor.execute('INSERT INTO Rows VALUES ("Группа крови", "-1 -2 7 -7 2 1 -1 5 -5 1 -3 3 -3 2 1 -1 -4 -3 8 -1 1 -3 2 1 -1 5 -5 1 -3 3 -3 2 1 -1 5 -2 -2 -1 1 -1 -2")')
cursor.execute('INSERT INTO Rows VALUES ("К Элизе", "-1 1 -1 1 -5 3 -2 -3 -5 5 2 -7 5 2 1 -8 12 -1 1 -1 1 -5 3 -2 -3 -5 5 2 -7 8 -1 -2 2 1 2 2 -9 10 -1 -2 -9 11 -2 -2 2 -2 -1 -7 8 -1 -2")')

connection.commit()

connection.close()