import time
import datetime
import sqlite3 as sq
import os
import pytesseract
import cv2
from PIL import Image
from parsing import readTextToFelds
from parsing2 import readTextToFelds2
from cheskdouble import checkDoubleDate
from write_to_csv import writeToCsv
from tqdm import tqdm

start_time = time.time()
screenshotspath = 'C:\PetScaner\Screenshert'
base_name = 'yamen.db'


def sheckNewFileNameInBase(name):
    """ Проверяет наличие имени файла в базе"""
    with sq.connect(base_name) as con:
        cursor = con.cursor()
        cursor.execute(f"SELECT name_file FROM names_files WHERE name_file = {name}")
        if cursor.fetchone() is None:
            return True
        else:
            return False


def writeFileNameToBase(name):
    """ Записывает имя файла в базу """
    with sq.connect(base_name) as con:
        cursor = con.cursor()
        cursor.execute(f"INSERT INTO names_files VALUES(null, {name}, 'True', 'False')")


def readNewFilesIfYandexToBase():
    """ Отбираем подходящие файлы для сканирования и складывает их имена в базу"""
    count = 0
    for adress, dirs, files in os.walk(screenshotspath):
        for file in files:
            namefile = "'" + file + "'"
            if 'yandex.taximeter' in namefile:
                if sheckNewFileNameInBase(namefile):
                    writeFileNameToBase(namefile)
                    count += 1
    print(f'В базу добавлено новых файлов - {count} ')


def readImagetoText(filename):
    """ Переводит картинку в строку текста"""
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
    screenshotname = f'{screenshotspath}\{filename}'
    image = cv2.imread(screenshotname)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    config = r'--oem 3 --psm 6'
    string = pytesseract.image_to_string(gray, lang='rus', config=config)
    string_split = string.split()
    return string_split


def nameToDate(name):
    """ Из имени файла достаем дату """
    date_str = name.split('_')
    datetimeplus = date_str[1]
    date_split = datetimeplus.split('-')
    date_split.pop(-1)
    date_time_str = ' '.join(date_split)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')
    return date_time_obj


readNewFilesIfYandexToBase()  # Заносим в базу имена пригодных файлов с данными

with sq.connect(base_name) as con:  # Проверяем количество доступных для расшифровки файлов
    cursor = con.cursor()
    cursor.execute("SELECT COUNT (readed) FROM names_files WHERE readed = 'False' AND easyread = 'True'")
    count = cursor.fetchone()
    notReadFilesOnBase = count[0]
    print(f'Всего файлов пригодных для расшифровки в базе - {notReadFilesOnBase}')

if notReadFilesOnBase > 0:
    k = int(input('Сколько файлов расшифровать? - '))

    if k <= notReadFilesOnBase:
        j = 0
        count = 0

        with sq.connect(base_name) as con:  # Расшифровываем и раскладываем по полям базы
            cursor = con.cursor()

            # while j < k:
            for i in tqdm(range(k)):
                cursor.execute(
                    "SELECT id, name_file FROM names_files WHERE readed = 'False' AND easyread = 'True' LIMIT 1")
                name = cursor.fetchone()
                try:
                    id = name[0]
                    namefile = name[1]
                    stringline = readImagetoText(namefile)
                except TypeError:
                    print(name)

                try:
                    date = str(nameToDate(namefile))
                    if date < '2022-04-04 00-00-00':
                        fields = readTextToFelds(stringline, namefile)
                    else:
                        fields = readTextToFelds2(stringline, namefile)
                        # if fields[4] > 0:
                    cursor.execute("INSERT INTO readed_text VALUES(null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0);",
                                   fields)
                    cursor.execute('UPDATE names_files SET readed = ? WHERE id = ?', (True, id))
                    # j += 1
                    count += 1


                except ValueError:
                    print(namefile, ' - ', stringline)
                    cursor.execute('UPDATE names_files SET easyread = ? WHERE id = ?', (False, id))
                    # j += 1

                except IndexError:
                    print(namefile, ' - ', stringline)
                    cursor.execute('UPDATE names_files SET easyread = ? WHERE id = ?', (False, id))
                    # j += 1

            print(f'\nРасшифровано и добавленно в базу новых записей - {count}')

            cursor.execute("SELECT COUNT (*) FROM names_files WHERE easyread = 0")
            count = cursor.fetchone()
            print(f'Файлов с ошибкой расшифровки в базе - {count[0]}')



    else:
        print("Столько файлов нет")

q = input("\nПроверить задублированные данные в базе? (y - Да) - ")
if q == 'y':
    checkDoubleDate()

q = input("\nЭкспортировать данные в 'csv' файл? (y - Да) - ")
if q == 'y':
    writeToCsv()

print("\n--- %s seconds ---" % int(time.time() - start_time))
