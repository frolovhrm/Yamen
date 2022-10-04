import time
import datetime
import sqlite3 as sq
import os
import pytesseract
import cv2
from PIL import Image
# from parsing import readTextToFelds
# from parsing2 import readTextToFelds2
# from cheskdouble import checkDoubleDate
# from write_to_csv import writeToCsv
from tqdm import tqdm

screenshotspath = 'C:\PetScaner\Screenshort'
base_name = 'yamen_ob.db'


class Screen():
    def __init__(self, name):
        self.name = name
        self.required = True
        self.readed = False


# Отбираем подходящие файлы для сканирования и складывает их имена в базу"""
count = 0
for adress, dirs, files in os.walk(screenshotspath):
    print(f'В указанной папаке найдено файлов - {len(files)},\nпроверяем файлы и добавляем новые в базу ...')
    for file in tqdm(files):
        screen = Screen("'" + file + "'")
        with sq.connect(base_name) as con:
            cursor = con.cursor()
            cursor.execute(f"SELECT name FROM Screen WHERE  name = {screen.name}")
            if cursor.fetchone() is None:
                if 'yandex.taximeter' in screen.name:
                    cursor = con.cursor()
                    cursor.execute(
                        f"INSERT INTO Screen VALUES(null, {screen.name}, {screen.required}, {screen.readed})")
                    count += 1
print(f'... найдено и добавленно в базу новых файлой - {count}')


class Fields(Screen):
    def __init__(self):
        self.id = 0
        self.date = ''
        self.activ = 0
        self.rait = 0
        self.grate = 0
        self.all_profit = 0.0
        self.cash_profit = 0.0
        self.cart_profit = 0.0
        self.orders = 0
        self.income = 0.0
        self.commission = 0.0
        self.mileage = 0
        self.balance = 0.0
        self.name = ''
        self.verified = False

    def readImagetoText(self):
        """ Переводит картинку в строку текста"""
        pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
        screenshotname = f'{screenshotspath}\{fields.name}'
        image = cv2.imread(screenshotname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        config = r'--oem 3 --psm 6'
        string = pytesseract.image_to_string(gray, lang='rus', config=config)
        string_split = string.split()
        return string_split

with sq.connect(base_name) as con:  # Проверяем количество доступных для расшифровки файлов
    cursor = con.cursor()
    cursor.execute("SELECT COUNT (readed) FROM Screen WHERE readed = '0' AND required = '1'")
    count = cursor.fetchone()
    notReadedFilesInBase = count[0]
    print(f'Всего файлов пригодных для расшифровки в базе - {notReadedFilesInBase}')

fields = Fields()


if notReadedFilesInBase > 0:
    k = int(input('Сколько файлов расшифровать? - '))
    if k <= notReadedFilesInBase:
        j = 0
        count = 0

        with sq.connect(base_name) as con:  # Расшифровываем и раскладываем по полям базы
            cursor = con.cursor()

        for i in tqdm(range(k)):
            cursor.execute(
                "SELECT id, name FROM Screen WHERE readed = '0' AND required = '1' LIMIT 1")
            name = cursor.fetchone()
            try:
                fields.id = name[0]
                fields.name = name[1]
                stringline = Fields.readImagetoText(fields)
                print(stringline)
            except TypeError:
                print(fields)


