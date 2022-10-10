import time
import datetime
import sqlite3 as sq
import os
import pytesseract
import cv2
from PIL import Image
from readTextToFields import readTextToFields
from readTextToFields2 import readTextToFields2
import re



from tqdm import tqdm

screenshotspath = 'C:\PetScaner\Screenshort'
base_name = 'yamen_ob.db'


class Screen():
    def __init__(self, name):
        self.name = name
        self.required = 0 # Код ошибки, 0 - норма, 1 - нулевые данные, 2 - ошибка парсинга
        self.readed = False
        self.id = 0


# Отбираем подходящие файлы для сканирования и складывает их имена в базу"""
count = 0
for adress, dirs, files in os.walk(screenshotspath):
    print(f'В указанной папаке найдено файлов - {len(files)} \n\nПроверяем файлы и добавляем новые в базу ...')
    for file in tqdm(files):
        screen = Screen("'" + file + "'")
        with sq.connect(base_name) as con:
            cursor = con.cursor()
            cursor.execute(f"SELECT name FROM Screen WHERE  name = {screen.name}")
            if cursor.fetchone() is None:
                if 'yandex.taximeter' in screen.name:
                    cursor = con.cursor()
                    cursor.execute(
                        f"INSERT INTO Screen VALUES(null, {screen.name}, {screen.required}, {screen.readed}, null)")
                    count += 1
print(f'... найдено и добавленно в базу новых файлой - {count} \n')


class Fields(Screen):
    def __init__(self):
        self.id = 0
        self.date = 'null'
        self.time = 'null'
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

        return string

    def nameToDate(self):
        """ Из имени файла достаем дату """
        date_str = fields.name.split('_')
        datetimeplus = date_str[1]
        date_split = datetimeplus.split('-')
        date_split.pop(-1)
        date_time_str = ' '.join(date_split)
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')
        return date_time_obj


def notReadedFilesInBase():
    with sq.connect(base_name) as con:  # Проверяем количество доступных для расшифровки файлов
        cursor = con.cursor()
        cursor.execute("SELECT COUNT (readed) FROM Screen WHERE readed = '0' AND required = '0'")
        count = cursor.fetchone()
        notReadedFilesInBase = count[0]
        print(f'Всего файлов пригодных для расшифровки в базе - {notReadedFilesInBase}')
        return notReadedFilesInBase

notParsFile = []

fields = Fields()


n = notReadedFilesInBase()
if n > 0:
    try:
        k = int(input('Сколько файлов расшифровать? - '))
    except:
        quit()
    if k == 0:
        quit()
    if k <= n:

        # tqdm
            for i in (range(k)):
                with sq.connect(base_name) as con:  # Расшифровываем и раскладываем по полям базы
                    cursor = con.cursor()

                    fields.activ = 0.0
                    fields.rait = 0.0
                    fields.grate = 0
                    fields.all_profit = 0.0
                    fields.cash_profit = 0.0
                    fields.cart_profit = 0.0
                    fields.orders = 0
                    fields.income = 0
                    fields.commission = 0
                    fields.mileage = 0
                    fields.balance = 0.0


                    try:
                        cursor.execute(
                            "SELECT id, name FROM Screen WHERE readed = '0' AND required = '0' LIMIT 1")
                        name = cursor.fetchone()
                        # name = 'Screenshot_2022-02-15-15-43-47-080_ru.yandex.taximeter.jpg'
                        # try:
                        screen.id = name[0]
                        fields.name = name[1]
                    except:
                        print('Файлы в базе не обнаружены')
                        break
                    # fields.name = 'Screenshot_2022-02-15-15-43-47-080_ru.yandex.taximeter.jpg'
                    string = Fields.readImagetoText(fields.name)
                    string1 = string.replace('?', ' ') # Готовим специальную строку для записи в базу
                    string1 = string1.replace("'", ' ')
                    string1 = "'" + string1 + "'"
                    # print(stringT)
                    cursor.execute(f"UPDATE Screen SET string = {string1}  WHERE id = {screen.id}")
                    string_split = string.split()
                    # except TypeError:
                    #     print(f'\nОшибка распознавания {fields.name}')

                    # try:
                    fields.date = str(Fields.nameToDate(fields.name))
                    # print(f"Дата = {fields.date}")
                    if fields.date < '2022-04-04 00-00-00':
                        readTextToFields(fields, string_split)
                        # print(f'old way {screen.name}')
                        # print(string_split)
                    else:
                        readTextToFields2(fields, string_split)
                        # print(f'new way {screen.name}')
                        # print(string_split)
                    # # except:
                    #     # print(f'Не прокатило - {fields.name}')
                    #     notParsFile.append(fields.name)
                    #     cursor.execute(f"UPDATE Screen SET required = 2  WHERE id = {screen.id}") # Поля не прочитались - статус 2
                    #     continue
                    if fields.all_profit + fields.cart_profit + fields.cart_profit == 0:
                        # print(f'Понулям! id = {fields.id} - {fields.name}')
                        cursor.execute(f"UPDATE Screen SET required = 1  WHERE id = {screen.id}") # Поля равны нулю - статус 1
                    else:
                        list_filds = [fields.date, fields.date, fields.activ, fields.rait, fields.grate, fields.all_profit, fields.cash_profit, fields.cart_profit,
                                      fields.orders, fields.income, fields.commission, fields.mileage, fields.balance, fields.name, fields.verified]
                        # print(list_filds)
                        cursor.execute("INSERT INTO Fields VALUES(null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",list_filds)
                        cursor.execute('UPDATE Screen SET readed = ? WHERE id = ?', (True, screen.id))
            print('Готово! \n')

notReadedFilesInBase()

print(f'Нераспарсеных файлов за сессию {len(notParsFile)}')
for i in notParsFile:
    print(i)

