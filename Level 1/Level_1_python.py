# coding: utf-8

import sqlite3

conn = sqlite3.connect('ma_base.db')

cursor = conn.cursor()
cursor.execute("""DROP TABLE IF EXISTS users""")
cursor.execute("""DROP TABLE IF EXISTS deals""")
cursor.execute("""CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT)""")
cursor.execute("""CREATE TABLE deals (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, amount INTEGER, user_id INTEGER)""")
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


cursor.execute("""SELECT COUNT() FROM users""")
nb_users = cursor.fetchone()[0]
for i in range(nb_users):
    cursor.execute("""SELECT COUNT() FROM deals WHERE user_id = ?""", (i+1,))
    nb_deals = cursor.fetchone()[0]
    if nb_deals > 2:
        cursor.execute("""SELECT SUM(amount) FROM deals WHERE user_id = ?""", (i+1,))
        total_amount = cursor.fetchone()[0]
        compensation = total_amount * 0.2
        if total_amount > 2000:
             compensation += 500
        name = cursor.execute("""SELECT name FROM users WHERE id = ?""", (i+1,)).fetchone()[0]
        print(name, "will be compensated by", compensation)
    elif nb_deals > 0 and nb_deals <= 2:
        cursor.execute("""SELECT SUM(amount) FROM deals WHERE user_id = ?""", (i+1,))
        total_amount = cursor.fetchone()[0]
        compensation = total_amount * 0.1
        if total_amount > 2000:
             compensation += 500
        name = cursor.execute("""SELECT name FROM users WHERE id = ?""", (i+1,)).fetchone()[0]
        print(name, "will be compensated by", compensation)
    else:
        name = cursor.execute("""SELECT name FROM users WHERE id = ?""", (i+1,)).fetchone()[0]
        print("No compensation for",name,"because he has no deals")

conn.close()