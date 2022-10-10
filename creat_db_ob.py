import sqlite3 as sq

with sq.connect('yamen_ob.db') as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS Screen (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name text NOT NULL,
    required INTEGER NOT NULL DEFAULT 0,
    readed BOOLEAN NOT NULL DEFAULT False,
    string text
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS Fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    time TEXT,
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
    name REAL,
    verified BOOLEAN NOT NULL DEFAULT False     
    )""")

    # cur.execute("""CREATE TABLE IF NOT EXISTS true_date (
    # id INTEGER PRIMARY KEY AUTOINCREMENT,
    # date TEXT,
    # activ INTEGER,
    # rait REAL,
    # grate INTEGER,
    # all_profit REAL,
    # cash_profit REAL,
    # cart_profit REAL,
    # orders INTEGER,
    # income INTEGER,
    # commission INTEGER,
    # mileage INTEGER,
    # balance REAL
    #
    # )""")

print('Новая база созданна')
