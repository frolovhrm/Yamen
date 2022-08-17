import sqlite3 as sq


with sq.connect('yamen.db') as con:
    cur = con.cursor()


    cur.execute ("""CREATE TABLE IF NOT EXISTS names_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    name_file text NOT NULL,
    readed BOOLEAN NOT NULL DEFAULT falce
    )""")

    cur.execute ("""CREATE TABLE IF NOT EXISTS readed_text (
    date TEXT NOT NULL,
    position INTEGER,
    activ REAL,
    rait REAL,
    grate INTEGER,
    all_profit REAL,
    cash_profit REAL,
    cart_profit REAL,
    orders INTEGER,
    income INTEGER,
    commission INTEGER,
    mileage INTEGER,
    balance REAL
    )""")