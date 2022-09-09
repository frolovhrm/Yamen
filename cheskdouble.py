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
    global duble_date

    with sq.connect(base_name) as con:
        cursor = con.cursor()
        cursor.execute(
            "SELECT date(date), COUNT(*)  FROM readed_text WHERE verified = 0  GROUP BY date(date) HAVING COUNT(*) > 1")
        listcount = cursor.fetchall()
        # print(listcount) # Собрали список всех дат и количество записей по ним
        for i in listcount:
            duble_date = i[0]
            count = i[1]
            s = f"SELECT id FROM readed_text WHERE date(date) = '{duble_date}'"
            cursor.execute(s)
            list_id = cursor.fetchall()
            # print(list_id) # Собрали список всех ID задублированых дат
            print(duble_date, count)

            for num in list_id: # Берем список ID от одной даты и сливаем все в один файл
                id_ = int(num[0])
                s = f"SELECT activ, rait, grate, all_profit, cash_profit, cart_profit, orders, income, commission, mileage, balance FROM readed_text WHERE id = {id_}"
                cursor.execute(s)
                fields = cursor.fetchone()
                # print(fields)

                if activ < int(fields[0]):
                    activ = fields[0]
                if rait < fields[1]:
                    rait = fields[1]
                if grate < fields[2]:
                    grate = fields[2]
                if all_profit < fields[3]:
                    all_profit = fields[3]
                if cash_profit < fields[4]:
                    cash_profit = fields[4]
                if cart_profit < fields[5]:
                    cart_profit = fields[5]
                if orders < fields[6]:
                    orders = fields[6]
                if income < fields[7]:
                    income = fields[7]
                if commission < fields[8]:
                    commission = fields[8]
                if mileage < fields[9]:
                    mileage = fields[9]
                if balance < fields[10]:
                    balance = fields[10]

                # помечаем запись как проверенную
                s = f"UPDATE readed_text SET verified = 1 WHERE id = {id_}"
                cursor.execute(s)
                print(f'{id_} - пометили')
            #     print(duble_date)
            #
            print(duble_date, activ, rait, grate, all_profit, cash_profit, cart_profit,  orders, income, commission, mileage, balance)

            # Пишем данные в базу новой строкой
            s = f"INSERT INTO true_date VALUES(null, '{duble_date}', {activ}, {rait}, {grate}, {all_profit}, {cash_profit}, {cart_profit}, {orders}, {income}, {commission}, {mileage}, {balance})"
            cursor.execute(s)


if __name__ == '__main__':
    checkDoubleDate()
