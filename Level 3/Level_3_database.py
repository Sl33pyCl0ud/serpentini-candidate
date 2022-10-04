import sqlite3

conn = sqlite3.connect('ma_base_3.db')

cursor = conn.cursor()
cursor.execute("""DROP TABLE IF EXISTS users""")
cursor.execute("""DROP TABLE IF EXISTS deals""")
cursor.execute("""CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT, objective INTEGER)""")
cursor.execute("""CREATE TABLE deals (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, amount INTEGER, user_id INTEGER, close_date TEXT, payment_date TEXT)""")
conn.commit()

user = []
user.append(("Nicolas", 1000))
user.append(("Math", 500))
cursor.executemany("""
INSERT INTO users(name, objective) VALUES(?, ?)""", user) 
conn.commit()

deals = []
deals.append((500, 1, "2018-05-01", "2018-05-20"))
deals.append((1000, 2, "2018-05-15", "2018-05-25"))
deals.append((800, 1, "2018-05-15", "2018-05-26"))
deals.append((700, 2, "2018-05-25", "2018-06-02"))
deals.append((700, 1, "2018-05-26", "2018-05-30"))
deals.append((1000, 1, "2018-05-30", "2018-06-13"))
deals.append((550, 2, "2018-06-02", "2018-07-06"))
deals.append((600, 1, "2018-06-15", "2018-06-18"))
cursor.executemany("""
INSERT INTO deals(amount, user_id, close_date, payment_date) VALUES(?, ?, ?, ?)""", deals)
conn.commit()

conn.close()