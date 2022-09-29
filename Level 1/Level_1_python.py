# coding: utf-8

import sqlite3

conn = sqlite3.connect('ma_base.db')

cursor = conn.cursor()
cursor.execute("""DROP TABLE IF EXISTS users""")
cursor.execute("""DROP TABLE IF EXISTS deals""")
cursor.execute("""CREATE TABLE IF NOT EXISTS  users (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS  deals (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, amount INTEGER, user_id INTEGER)""")
conn.commit()

name1 = "Nicolas"
name2 = "Math"
cursor.execute("""INSERT INTO users(name) VALUES(?)""", (name1,))
cursor.execute("""INSERT INTO users(name) VALUES(?)""", (name2,))
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

cursor.execute("""SELECT amount, user_id FROM deals""")
deals_print = cursor.fetchall()
print(deals_print)

cursor.execute("""SELECT COUNT() FROM deals where user_id == 1""")
count = cursor.fetchone()[0]
print(count)


conn.close()