import sqlite3

conn = sqlite3.connect('ma_base.db')

cursor = conn.cursor()

cursor.execute("""SELECT COUNT() FROM users""")
nb_users = cursor.fetchone()[0]

def calculateCompensation():
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
            print(name, "with the id number", i+1, "will be compensated by", compensation)
        elif nb_deals > 0 and nb_deals <= 2:
            cursor.execute("""SELECT SUM(amount) FROM deals WHERE user_id = ?""", (i+1,))
            total_amount = cursor.fetchone()[0]
            compensation = total_amount * 0.1
            if total_amount > 2000:
                compensation += 500
            name = cursor.execute("""SELECT name FROM users WHERE id = ?""", (i+1,)).fetchone()[0]
            print(name, "with the id number", i+1, "will be compensated by", compensation)
        else:
            name = cursor.execute("""SELECT name FROM users WHERE id = ?""", (i+1,)).fetchone()[0]
            print("No compensation for",name, "with the id number", i+1, "because he has no deals")

calculateCompensation()

conn.close()