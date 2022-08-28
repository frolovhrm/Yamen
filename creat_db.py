import sqlite3 as sq


with sq.connect('yamen.db') as con:
    cur = con.cursor()


    cur.execute ("""CREATE TABLE IF NOT EXISTS names_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name_file text NOT NULL,
    easyread BOOLEAN NOT NULL DEFAULT True,
    readed BOOLEAN NOT NULL DEFAULT False
    )""")

    cur.execute ("""CREATE TABLE IF NOT EXISTS readed_text (
    date TEXT NOT NULL,
    activ INTEGER,
    rait REAL,
    grate INTEGER,
    all_profit REAL,
    cash_profit REAL,
    cart_profit REAL,
    orders INTEGER,
    income INTEGER,
    commission INTEGER,
    mileage INTEGER,
    balance REAL,
    files_name REAL
    )""")

print('Новая база созданна')
