import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS sessies (id INTEGER PRIMARY KEY AUTOINCREMENT, datum TEXT, start_tijd TEXT, eind_tijd TEXT, duur_minuten INTEGER)")
connection.commit()
connection.close()