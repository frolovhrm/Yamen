import datetime
from tqdm import tqdm
import re


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
    # print(str_line)
    while position < len(str_line):

        """ Неверный скрин """
        if str_line[position] == 'История':
            break

        if str_line[position] == 'За' and str_line[position + 1] == 'неделю':
            break

        if str_line[position] == 'Сегодня':
            if str_line[position + 1] == '0,00':
                break
            if str_line[position + 1] == '0,00Р':
                break
            if str_line[position + 1] == '0,00?':
                break
            if str_line[position + 1] == '0,00?Р':
                break

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
            all_profit_str = str_line[position + 1] + str_line[position + 2] + str_line[position + 3]
            try:
                all_profit_str = all_profit_str.replace(',', '.')
                # print(all_profit_str)
                all_profit_str_num = re.findall(r'\d*\.\d*', all_profit_str)
                # print(all_profit_str_num)
                all_profit = float(all_profit_str_num[0])
            except:

                all_profit = 999999999999
                print(all_profit)

            """ Выручка карта """
        if str_line[position] == 'карта':

            cart_profit_str = str_line[position - 3] + str_line[position - 2] + str_line[position - 1]
            try:
                cart_profit_str = cart_profit_str.replace(',', '.')
                # print(cart_profit_str)
                cart_profit_str_num = re.findall(r'\d*\.\d*', cart_profit_str)
                # print(cart_profit_str_num)
                cart_profit = float(cart_profit_str_num[0])
            except:
                print(f'\nError!!! Card')

        """ Выручка наличные """
        if str_line[position] == 'карта':
            if str_line[position + 1] != 'водителя':
                if len(str_line[position + 2]) == 1:
                    cash_profit_str = str_line[position + 2] + str_line[position + 3] + str_line[position + 4]
                else:
                    cash_profit_str = str_line[position + 2]

                cash_profit_str = cash_profit_str.replace(',', '.')
                cash_profit_str_num = re.findall(r'\d*\.\d*', cash_profit_str)
                # print(cash_profit_str1)
                # cash_profit_str = cash_profit_str[:-1]
                # cash_profit_str = cash_profit_str.replace(',', '.')
                # print()
                cash_profit = float(cash_profit_str_num[0])

        """ Заказов """
        if str_line[position] == 'заказов':
            # print(str_line[position - 1])
            try:
                orders = int(str_line[position - 1])

            except:
                orders = 99999  # Заглушка

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
                    mileage = 99999  # Заглушка

        if str_line[position] == 'Баланс':
            if position < len(str_line) - 4:
                try:
                    if len(str_line[position + 1]) == 1:
                        balance_str = str_line[position + 1] + str_line[position + 2]
                    else:
                        balance_str = str_line[position + 1]
                    balance_str = balance_str[:-1]
                    balance_str = balance_str.replace(',', '.')
                    balance = float(balance_str)
                except:
                    print(f'balanse - {name}')

        position += 1
    ''' Получение даты из имени файла'''

    date_str = name.split('_')
    datetimeplus = date_str[1]
    date_split = datetimeplus.split('-')
    date_split.pop(-1)
    date_time_str = ' '.join(date_split)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')

    return date_time_obj, activ, rait, grate, all_profit, cart_profit, cash_profit, orders, income, commission, mileage, balance, name
