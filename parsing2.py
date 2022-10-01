import datetime


def readTextToFelds2(str_line, name):
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
        # print(position)
        """ Неверный скрин """
        if str_line[position] == 'История':
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
                orders = int(str_line[position - 1])
            except ValueError:
                orders = 9999999999  # Заглушка
            # print('orders - ' + orders)

        """ Активность, Рейтинг, Уровень """
        if str_line[position] == 'Самозанятый':
            # print('Activ, grait, rait')
            activ = int(str_line[position + 1])
            rait = float(str_line[position + 2])
            if str_line[position + 3] == 'Бронза':
                grate = 3
            if str_line[position + 3] == 'Золото':
                grate = 2
            if str_line[position + 3] == 'Платина':
                grate = 1
            # print('Activ - ', activ, 'grait - ', grate, 'rait - ', rait)

        # if str_line[position] == 'Сегодня':
        #     """ Всего выручка """
        #     print('All')
        #
        #     if len(str_line[position + 2]) == 1:  # если сиввол только один, добавляем из следующей позиции
        #         all_profit_str = str_line[position + 1] + str_line[position + 2]
        #     else:
        #         all_profit_str = str_line[position + 2]
        #     try:
        #         all_profit_str = all_profit_str[:-1]
        #         all_profit_str = all_profit_str.replace(',', '.')
        #         all_profit = float(all_profit_str)
        #     except:
        #         all_profit_str = all_profit_str[:-2]
        #         all_profit_str = all_profit_str.replace(',', '.')
        #         all_profit = float(all_profit_str)

        """ Выручка карта """
        if str_line[position] == 'По':
            # print('Cart')
            if len(str_line[position + 2]) == 1:  # если сиввол только один, добавляем из следующей позиции
                cart_profit_str = str_line[position + 2] + str_line[position + 3]
            else:
                cart_profit_str = str_line[position + 2]

            cart_profit_str = cart_profit_str[:-1]
            cart_profit_str = cart_profit_str.replace(',', '.')
            cart_profit = float(cart_profit_str)
            # print('Cart - ', cart_profit)

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
                    cash_profit = float(cash_profit_str)
                    # print('Cash - ', cash_profit)
                except:
                    print(f'Ошибка в позиции {str_line[position]}')
                    # print(cash_profit_str)

        """ Комиссия """
        if str_line[position] == 'Сервис':
            # print('Comission')
            try:
                if len(str_line[position + 2]) == 1:  # если сиввол только один, добавляем из следующей позиции
                    commission_str = str_line[position + 2] + str_line[position + 3]

                else:
                    commission_str = str_line[position + 2]

                commission_str = commission_str[:-1]
                commission_str = commission_str.replace(',', '.')
                commission = float(commission_str)

            except:
                print('Error Comission - ', commission)
                print(str_line)
                print(str_line[position + 2], commission_str[:-1], commission_str.replace(',', '.'))

        """ Баланс """
        if str_line[position] == 'Баланс':
            # print('Balance')
            if len(str_line[position + 1]) == 1:  # если сиввол только один, добавляем из следующей позиции
                balance_str = str_line[position + 1] + str_line[position + 2]
            else:
                balance_str = str_line[position + 1]

            balance_str = balance_str[:-1]
            balance_str = balance_str.replace(',', '.')
            balance = float(balance_str)
            # print('Balance - ', balance)

        position += 1

    ''' Получение даты из имени файла'''
    date_str = name.split('_')
    datetimeplus = date_str[1]
    date_split = datetimeplus.split('-')
    date_split.pop(-1)
    date_time_str = ' '.join(date_split)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')

    # print(date_time_obj, activ, rait, grate, all_profit, cart_profit, cash_profit, orders, income, commission, mileage, balance, name)
    # print("")
    return date_time_obj, activ, rait, grate, all_profit, cart_profit, cash_profit, orders, income, commission, mileage, balance, name
