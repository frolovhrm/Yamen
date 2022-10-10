import datetime
import re


def readTextToFields2(fields, str_line):
    """ Парсим строку, достаем данные по полям"""

    print(fields.name, str_line)
    position = 0
    bed_words = ['История', 'Отмена', 'Обновлен', 'Поездка', 'попали', 'этот', 'Оцените', 'качества', 'следующем', 'Доступно', 'комплименты', 'приоритет', 'транзакции']
    # global atention

    while position < len(str_line):
        atention = ''

        """ Неверный скрин """
        for i in bed_words:
            if str_line[position] == i:
                atention = 'atention'
                # print(fields.name, i)
                break
        if atention == 'atention':
            break


        if str_line[position] == 'За' and str_line[position + 1] == 'неделю':
            break


        if str_line[position] == 'Сегодня':
            if str_line[position + 2] == '0, 00':
                break
            if str_line[position + 2] == '0,00Р':
                break
            if str_line[position + 2] == '0,00?':
                break
            if str_line[position + 2] == '0,00?Р':
                break

        """ Заказов """
        if str_line[position] == 'заказ':
            # print('orders')
            try:
                fields.orders = int(str_line[position - 1])
            except ValueError:
                fields.orders = 9999999999  # Заглушка
                print(f'Error orders - {str_line[position - 1]}')
            # print('orders - ' + orders)
            position += 1
            continue

        """ Активность, Рейтинг, Уровень """
        if str_line[position] == 'Самозанятый':
            # print('Activ, grait, rait')
            try:
                fields.activ = int(str_line[position + 1])
            except:
                print(f'Activ - {fields.name} - {str_line[position + 1]}')

            fields.rait = float(str_line[position + 2])
            if str_line[position + 3] == 'Бронза':
                fields.grate = 3
            if str_line[position + 3] == 'Золото':
                fields.grate = 2
            if str_line[position + 3] == 'Платина':
                fields.grate = 1
            # print('Activ - ', activ, 'grait - ', grate, 'rait - ', rait)
            position += 1
            continue

        if str_line[position] == 'Сегодня':
            """ Всего выручка """
            # print('All')

            if len(str_line[position + 2]) == 1:  # если сиввол только один, добавляем из следующей позиции
                all_profit_str = str_line[position + 2] + str_line[position + 3]
            else:
                all_profit_str = str_line[position + 2]

            all_profit_str = all_profit_str[:-1]
            all_profit_str = all_profit_str.replace(',', '.')

            if all_profit_str.isdigit():
                fields.all_profit = float(all_profit_str)
            else:
                # try:
                    all_profit_str_num = re.findall(r'\d*\.\d*', all_profit_str)
                    fields.all_profit = float(all_profit_str_num[0])
                # except:
                #     print(f"Ошибка All_profit_new - {fields.name} - {all_profit_str} ")
            position += 1
            continue

        """ Выручка карта """
        if str_line[position] == 'По':
            # print('Cart')
            if len(str_line[position + 2]) == 1:  # если сиввол только один, добавляем из следующей позиции
                cart_profit_str = str_line[position + 2] + str_line[position + 3]
            else:
                cart_profit_str = str_line[position + 2]

            cart_profit_str = cart_profit_str[:-1]
            cart_profit_str = cart_profit_str.replace(',', '.')
            fields.cart_profit = float(cart_profit_str)
            # print('Cart - ', cart_profit)
            position += 1
            continue

        """ Выручка наличные """
        if str_line[position] == 'Наличными':
            if str_line[position + 1] != 'или':
                # print('Cash')
                if len(str_line[position + 1]) == 1:  # если сиввол только один, добавляем из следующей позиции
                    cash_profit_str = str_line[position + 1] + str_line[position + 2]
                else:
                    cash_profit_str = str_line[position + 1]

                try:
                    cash_profit_str = cash_profit_str[:-1]
                    cash_profit_str = cash_profit_str.replace(',', '.')
                    fields.cash_profit = float(cash_profit_str)
                    # print('Cash - ', cash_profit)
                except:
                    print(f'Ошибка в позиции {str_line[position]}')
                    # print(cash_profit_str)
            position += 1
            continue


        """ Комиссия """
        if str_line[position] == 'Сервис':
            # print('Comission')

            if len(str_line[position + 2]) == 1:  # если сиввол только один, добавляем из следующей позиции
                commission_str = str_line[position + 2] + str_line[position + 3]

            else:
                commission_str = str_line[position + 2]

            commission_str = commission_str[:-1]
            commission_str = commission_str.replace(',', '.')

            if commission_str.isdigit():
                fields.commission = float(commission_str)
            else:
                # try:
                commission_str_num = re.findall(r'\d*\.\d*', commission_str)
                fields.commission = float(commission_str_num[0])
            # except:
            #     print(f"Ошибка Cash - {commission_str} - {fields.name}")
            position += 1
            continue

        """ Баланс """
        if str_line[position] == 'Баланс':
            # print('Balance')
            if len(str_line[position + 1]) == 1:  # если сиввол только один, добавляем из следующей позиции
                balance_str = str_line[position + 1] + str_line[position + 2]
            else:
                balance_str = str_line[position + 1]

            balance_str = balance_str[:-1]
            balance_str = balance_str.replace(',', '.')
            fields.balance = float(balance_str)
            # print('Balance - ', balance)

        position += 1

    ''' Получение даты из имени файла'''
    date_str = fields.name.split('_')
    datetimeplus = date_str[1]
    date_split = datetimeplus.split('-')
    date_split.pop(-1)
    date_time_str = ' '.join(date_split)
    fields.date = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')
