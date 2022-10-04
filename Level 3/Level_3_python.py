import sqlite3

conn = sqlite3.connect('ma_base_3.db')

cursor = conn.cursor()

cursor.execute("""SELECT * FROM deals""") 
deals = cursor.fetchall()

cursor.execute("""SELECT * FROM users""") 
users = cursor.fetchall()

commissions = {}
deal_commission = {}

def calculateCommission():
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
                if total_amount - deal[1] < objective * 0.5:
                    part_1 = deal[1] - (total_amount - objective * 0.5)
                    commission = part_1 * 0.05 + (total_amount - objective * 0.5) * 0.1
                else:
                    commission = deal[1] * 0.1
            elif total_amount > objective:
                if total_amount - deal[1] < objective * 0.5:
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

calculateCommission()

conn.close()
    
    
