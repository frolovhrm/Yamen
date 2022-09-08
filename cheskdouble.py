import datetime
import sqlite3 as sq

base_name = 'yamen.db'


def checkDoubleDate():
    """ Проверяет наличие задвоений в базе """
    id_ = 0
    date = ''
    activ = 0
    rait = 0.0
    grate = 0
    all_profit = 0.0
    cart_profit = 0.0
    cash_profit = 0.0
    orders = 0
    income = 0.0
    commission = 0.0
    mileage = 0
    balance = 0.0





    with sq.connect(base_name) as con:
        cursor = con.cursor()
        cursor.execute(
            "SELECT id, date(date), activ, rait, grate, all_profit, cart_profit, cash_profit, orders, income, commission, mileage, balance, COUNT(*)  FROM readed_text WHERE verified = 0  GROUP BY date(date) HAVING COUNT(*) > 1")
        listnames = cursor.fetchone()
        # for i in listnames:
        #     print(i)
        print(listnames)
        for i in listnames:
            if activ < i[2]:
                activ < i[2]
            if rait < i[3]:
                rait = i[3]
            if grate < i[4]:
                grate = i[4]
            if all_profit < i[5]:
                all_profit = i[5]
            if cart_profit < i[6]:
                cart_profit = i[6]
            if cash_profit < i[7]:
                cash_profit = i[7]
            if orders < i[8]:
                orders = i[8]
            if income < i[9]:
                income = i[9]
            if commission < i[10]:
                commission = i[10]
            if mileage < i[11]:
                mileage = i[11]
            if balance < i[12]:
                balance = i[12]



if __name__ == '__main__':
    checkDoubleDate()

    # cursor.execute(
    #     "SELECT id, date(date), time(date), strftime('%s', date), COUNT(*)  FROM readed_text WHERE verified = 0  GROUP BY date(date) HAVING COUNT(*) > 1")
    #     # first_group_ID = listnames[0]
    #     # date = listnames[1]
    #     # full_time = listnames[2]
    #     # hour = int(listnames[3])
    #     # count_duble_fiels = int(listnames[4])
    #     # print(first_group_ID, date, full_time, hour, count_duble_fiels)
