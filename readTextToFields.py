import datetime
import re


def readTextToFields(fields, str_line):
    """ Парсим строку, достаем данные по полям"""
    print(fields.name, str_line)

    position = 0
    bed_words = ['История', 'Отмена', 'Обновлен', 'этот', 'Поездка', 'попали', 'Оцените', 'качества', 'следующем', 'Доступно', 'комплименты', 'приоритет','транзакции']

    while position < len(str_line):
        # print(position)
        """ Неверный скрин """
        attention = ''
        for i in bed_words:
            if str_line[position] == i:
                attention = 'attention'
                # print(fields.name, i)
                break
        if attention == 'attention':
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
            try:
                fields.activ = int(str_line[position + 1])
                fields.rait = float(str_line[position + 2])
                if str_line[position + 3] == 'Бронза':
                    fields.grate = 3
                if str_line[position + 3] == 'Золото':
                    fields.grate = 2
                if str_line[position + 3] == 'Платина':
                    fields.grate = 1
            except:
                fields.activ = 999999999999
                fields.rait = 9999999999999
                fields.grate = 999999999999
                print(f'Error active old {fields.name} - {str_line[position + 1]}/{str_line[position + 2]}')
            position += 1
            continue

        if str_line[position] == 'Сегодня':
            """ Всего выручка """
            all_profit_str = str_line[position + 1] + str_line[position + 2] + str_line[position + 3]
            try:
                all_profit_str = all_profit_str.replace(',', '.')
                # print(all_profit_str)
                all_profit_str_num = re.findall(r'\d*\.\d*', all_profit_str)
                # print(all_profit_str_num)
                fields.all_profit = float(all_profit_str_num[0])
            except:
                fields.all_profit = 999999999999
                print(f'Error all_profit old {fields.name} - {all_profit_str}')
            position += 1
            continue

            """ Выручка карта """
        if str_line[position] == 'карта':

            cart_profit_str = str_line[position - 2] + str_line[position - 1]
            try:
                cart_profit_str = cart_profit_str.replace(',', '.')
                if cart_profit_str.isdigit():
                    fields.cart_profit = float(cart_profit_str_num[0])
                else:
                    # print(cart_profit_str)
                    cart_profit_str_num = re.findall(r'\d*\.\d*', cart_profit_str)
                    # print(cart_profit_str_num)
                    fields.cart_profit = float(cart_profit_str_num[0])
            except:
                fields.cart_profit = 9999999999999
                print(f'Error card old {fields.name} - {cart_profit_str}')

        """ Выручка наличные """
        if str_line[position] == 'карта':
            if str_line[position + 1] != 'водителя':
                if len(str_line[position + 2]) == 1:
                    cash_profit_str = str_line[position + 2] + str_line[position + 3]
                    # print(cash_profit_str)
                else:
                    cash_profit_str = str_line[position + 2]

                cash_profit_str = cash_profit_str.replace(',', '.')
                if cash_profit_str.isdigit():
                    fields.cash_profit = float(cash_profit_str)
                    # print(fields.cash_profit )
                else:
                    try:
                        cash_profit_str_num = re.findall(r'\d*\.\d*', cash_profit_str)
                        fields.cash_profit = float(cash_profit_str_num[0])
                        # print(fields.cash_profit)
                    except:
                        fields.cash_profit = 9999999999999
                        print(f"Ошибка cash Old {fields.name} - {cash_profit_str}")
            position += 1
            continue

        """ Заказов """
        if str_line[position] == 'заказов' or str_line[position] == 'заказа':
            if str_line[position + 1] == 'Комиссия':
                # print(str_line[position - 1])
                if str_line[position - 1].isdigit():
                    try:
                        fields.orders = int(str_line[position - 1])
                    except:
                        fields.orders = 99999999999
                        print(f'Error order old {fields.name} - {str_line[position - 1]}')
                else:
                    try:
                        orders_str = str_line[position - 1]
                        orders_str_num = re.findall(r'\d*', orders_str)
                        fields.orders = int(orders_str_num[0])
                    except:
                        if orders_str_num[0].isdigit():
                            fields.orders = 99999999999
                            print(f'Error2 order old {fields.name} - "{str_line[position - 1]}"')
                        else:
                            fields.orders = 0
            position += 1
            continue

        """ Комиссия """
        if str_line[position] == 'Комиссия' and str_line[position + 1] == 'парка':
            if str_line[position - 1] == 'Яндекса':
                position += 1
                continue

            commission_str = str_line[position - 2] + str_line[position - 1]
            commission_str = commission_str[:-1]
            commission_str = commission_str.replace(',', '.')
            if commission_str.isdigit():
                try:
                    fields.commission = float(commission_str)
                except:
                    fields.commission = 999999999
                    print(f'Error commission old {fields.name} - {commission_str}')
            else:
                try:
                    # print(commission_str)
                    commission_num = re.findall(r'\d*\.\d*', commission_str)
                    # print(commission_num)
                    fields.commission = float(commission_num[0])
                except:
                    fields.commission = 99999999999
                    print(f'Error2 commission old {fields.name} - {commission_str}')

            position += 1
            continue

        """ Пробег """
        if str_line[position] == 'Пробег':
            mileage_str = str_line[position + 1]
            if str_line[position + 1] == 'О':
                fields.mileage = 0
                position += 1
                continue
            if str_line[position + 1] == 'З':
                fields.mileage = 3
                position += 1
                continue


            if str_line[position + 1].isdigit():
                try:
                    fields.mileage = int(str_line[position + 1])
                except:
                    print(f'Error mileage {fields.name} - {mileage_str}')
            else:
                try:
                    fields.mileage = int(str_line[position + 2])
                except:
                    fields.mileage = 999999999999
                    print(f'Error mileage old {fields.name} - {str_line[position + 1]}/{str_line[position + 2]}')

            position += 1
            continue

        if str_line[position] == 'Баланс':
            if position < len(str_line) - 4:
                try:
                    if len(str_line[position + 1]) == 1:
                        balance_str = str_line[position + 1] + str_line[position + 2]
                    else:
                        balance_str = str_line[position + 1]
                    balance_str = balance_str[:-1]
                    balance_str = balance_str.replace(',', '.')
                    fields.balance = float(balance_str)
                except:
                    fields.balance = 9999999999999
                    print(f'Error balanse old {fields.name} - {balance_str}')

        position += 1
    ''' Получение даты из имени файла'''

    date_str = fields.name.split('_')
    datetimeplus = date_str[1]
    date_split = datetimeplus.split('-')
    date_split.pop(-1)
    date_time_str = ' '.join(date_split)
    fields.date = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')
