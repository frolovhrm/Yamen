import datetime


def readTextToFelds(str_line, name):
    """ Парсим строку, достаем данные по полям"""

    position = 0
    activ = 0.0
    rait = 0.0
    grate = 0
    all_profit = 0.0
    cash_profit = 0.0
    cart_profit = 0.0
    orders = 0
    income = 0
    commission = 0
    mileage = 0
    balance = 0.0

    while position < len(str_line):

        """ Активность, Рейтинг, Уровень """
        if str_line[position] == 'Самозанятый':
            activ = int(str_line[position + 1])
            rait = float(str_line[position + 2])
            if str_line[position + 3] == 'Бронза':
                grate = 3
            if str_line[position + 3] == 'Золото':
                grate = 2
            if str_line[position + 3] == 'Платина':
                grate = 1

        if str_line[position] == 'Сегодня':
            """ Всего выручка """
            if len(str_line[position + 1]) == 1:
                all_profit_str = str_line[position + 1] + str_line[position + 2]
            else:
                all_profit_str = str_line[position + 1]
            try:
                all_profit_str = all_profit_str[:-1]
                all_profit_str = all_profit_str.replace(',', '.')
                all_profit = float(all_profit_str)
            except:
                all_profit_str = all_profit_str[:-2]
                all_profit_str = all_profit_str.replace(',', '.')
                all_profit = float(all_profit_str)

            """ Выручка карта """
            if str_line[position + 3] == '>':
                if len(str_line[position + 4]) == 1:
                    cart_profit_str = str_line[position + 4] + str_line[position + 5]
                else:
                    cart_profit_str = str_line[position + 4]
                cart_profit_str = cart_profit_str[:-1]
                cart_profit_str = cart_profit_str.replace(',', '.')
                cart_profit = float(cart_profit_str)

        """ Выручка наличные """
        if str_line[position] == 'карта':
            if str_line[position + 1] != 'водителя':
                if len(str_line[position + 2]) == 1:
                    cash_profit_str = str_line[position + 2] + str_line[position + 3]
                else:
                    cash_profit_str = str_line[position + 2]
                cash_profit_str = cash_profit_str[:-1]
                cash_profit_str = cash_profit_str.replace(',', '.')
                cash_profit = float(cash_profit_str)

        """ Заказов """
        if str_line[position] == 'заказы':
            try:
                if str_line[position + 3] == '›':
                    orders = int(str_line[position + 4])
                else:
                    orders = int(str_line[position + 3])
            except ValueError:
                if str_line[position + 4] == 'О':
                    orders = 0
                else:
                    orders = 99999

            """ Комиссия """
            # commission = str_line[position + 7]

        """ Пробег """
        if str_line[position] == 'Пробег':
            try:
                mileage = int(str_line[position + 1])

            except ValueError:
                mileage_str = str_line[position + 1]
                mileage_str = mileage_str[:-2]
                if mileage_str == 'О':
                    mileage = 0
                else:
                    mileage = 99999

        if str_line[position] == 'Баланс':
            if len(str_line[position + 1]) == 1:
                balance_str = str_line[position + 1] + str_line[position + 2]
            else:
                balance_str = str_line[position + 1]
            balance_str = balance_str[:-1]
            balance_str = balance_str.replace(',', '.')
            balance = float(balance_str)

        position += 1
    ''' Получение даты из имени файла'''

    date_str = name.split('_')
    datetimeplus = date_str[1]
    date_split = datetimeplus.split('-')
    date_split.pop(-1)
    date_time_str = ' '.join(date_split)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')

    return date_time_obj, activ, rait, grate, all_profit, cart_profit, cash_profit, orders, income, commission, mileage, balance, name
