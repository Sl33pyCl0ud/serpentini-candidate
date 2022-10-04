from functools import total_ordering
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

cursor.execute("""SELECT * FROM deals""") 
deals = cursor.fetchall()

cursor.execute("""SELECT * FROM users""") 
users = cursor.fetchall()

#Create an object commissions, the key being the user_id, the year and month of close_date (format YYYY-MM) and the value the total of commission paid in the month.
commissions = {}
deal_commission = {}
for user in users:
    cursor.execute("""SELECT * FROM deals WHERE user_id = ?""", (user[0],))
    deals_by_user = cursor.fetchall()
    total_amount = 0
    for deal in deals_by_user:
        cursor.execute("""SELECT objective FROM users WHERE id = ?""", (deal[2],))
        objective = cursor.fetchone()[0]
        total_amount += deal[1]
        if total_amount <= objective * 0.5:
            commission = deal[1] * 0.05
        elif total_amount <= objective and total_amount > objective * 0.5:
            part_1 = deal[1] - (total_amount - objective * 0.5)
            commission = part_1 * 0.05 + (total_amount - objective * 0.5) * 0.1
        elif total_amount > objective:
            if deal[1] > objective and total_amount - deal[1] < objective:
                part_1 = deal[1] - (total_amount - objective * 0.5)
                part_2 = deal[1] - part_1 - (total_amount - objective)
                commission = part_1 * 0.05 + part_2 * 0.1 + (total_amount - objective) * 0.15
            elif total_amount - deal[1] < objective:
                part_2 = deal[1] - (total_amount - objective)
                commission = part_2 * 0.1 + (total_amount - objective) * 0.15
            else:
                commission = deal[1] * 0.15
        deal_commission[deal[0]] = commission
        payment_date = deal[4]
        year_month = payment_date[:7]
        user_id = deal[2]
        if user_id not in commissions:
            commissions[user_id] = {}
        if year_month not in commissions[user_id]:
            commissions[user_id][year_month] = 0
        commissions[user_id][year_month] += commission

print ("commissions:", commissions)
print ("deal_commission:", deal_commission)

conn.close()
    
    
