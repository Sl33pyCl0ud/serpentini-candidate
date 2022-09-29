# coding: utf-8

import sqlite3

conn = sqlite3.connect('ma_base.db')

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     name TEXT,
)
""")
conn.commit()

users = []
users.append(("Nicolas"))
users.append(("Math"))
cursor.executemany("""
INSERT INTO users(name) VALUES(?, ?)""", users)
conn.commit()

deals = []
deals.append((500, 1))
deals.append((1000, 2))
deals.append((800, 1))
deals.append((1000, 2))
deals.append((300, 2))
deals.append((300, 2))
cursor.executemany("""
INSERT INTO deals(amount, user_id) VALUES(?, ?)""", deals)
conn.commit()

cursor.execute("""SELECT name FROM users""")
user1 = cursor.fetchone()
print(user1)


conn.close()