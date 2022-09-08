import csv
import sqlite3 as sq

base_name = 'yamen.db'
filename = 'yamenbase.csv'


def writeToCsv():
    with sq.connect(base_name) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM readed_text")
        mylist = cursor.fetchall()

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['id', 'date_time_obj', 'activ', 'rait', 'grate', 'all_profit', 'cart_profit', 'cash_profit',
                      'orders', 'income', 'commission', 'mileage', 'balance', 'name', 'verified']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
        for row in mylist:
            id_ = row[0]
            date_time_obj = row[1]
            activ = row[2]
            rait = row[3]
            grate = row[4]
            all_profit = row[5]
            cart_profit = row[6]
            cash_profit = row[7]
            orders = row[8]
            income = row[9]
            commission = row[10]
            mileage = row[11]
            balance = row[12]
            name = row[13]
            verified = row[14]
            writer.writerow(
                {'id': id_, 'date_time_obj': date_time_obj, 'activ': activ, 'rait': rait, 'grate': grate,
                 'all_profit': all_profit, 'cart_profit': cart_profit, 'cart_profit': cart_profit,
                 'cash_profit': cash_profit, 'orders': orders, 'income': income, 'commission': commission,
                 'mileage': mileage, 'balance': balance, 'name': name, 'verified': verified})

    print('Файл подготовлен и сохнанен в папку с программой.\nУдачи!')

if __name__ == '__main__':
    writeToCsv()