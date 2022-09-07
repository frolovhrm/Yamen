import datetime
import sqlite3 as sq

base_name = 'yamen.db'


def checkDoubleDate():
    """ Проверяет наличие задвоений в базе """


    with sq.connect(base_name) as con:
        cursor = con.cursor()
        cursor.execute("SELECT id, date(date), time(date), strftime('%s', date), COUNT(*)  FROM readed_text GROUP BY date(date) HAVING COUNT(*) > 1")
        listnames = cursor.fetchall()
        # print(listnames)
        n = 0
        for i in listnames:
            n += 1
            # print(f'ID - {i[0]} Дата - {i[1]} , Время - {i[2]}, Час - {i[3]} количество записей - {i[4]}')
            first_group_ID = f'{i[0]}'
            date = f'{i[1]}'
            full_time = f'{i[2]}'
            hour = int(i[3])
            count_of_list = int(i[4])
            print(first_group_ID, date, full_time, hour, count_of_list)
            # var = 1
            # while var < count_of_list:


            if n > 2:
                break


if __name__ == '__main__':
    checkDoubleDate()