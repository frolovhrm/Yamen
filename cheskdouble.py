import datetime
import sqlite3 as sq

base_name = 'yamen.db'


def checkDoubleDate():
    """ Проверяет наличие задвоений в базе """


    with sq.connect(base_name) as con:
        cursor = con.cursor()
        cursor.execute("SELECT date(date), COUNT(*)  FROM readed_text GROUP BY date(date) HAVING COUNT(*) > 1")
        listnames = cursor.fetchall()
        # print(listnames)
        for i in listnames:
            print(f'Дата - {i[0]} , количество записей - {i[1]}')


# checkDoubleDate()