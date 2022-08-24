import time
import datetime
import sqlite3 as sq

start_time = time.time()
import os
import pytesseract
import cv2
from PIL import Image
from parsing import readTextToFelds




screenshetspath = 'C:\PetScaner\Screenshert'

def sheckNewFileNameInBase(name):
    """ Проверяем наличие файла в базе"""
    with sq.connect('yamen.db') as con:
        cursor = con.cursor()
        name = f"'{name}'"
        cursor.execute(f"SELECT name_file FROM names_files WHERE name_file = {name}")
        if cursor.fetchone() is None:
            return True
        else:
            return False


def readNewFilesIfYandexToBase():
    """ Собираем список файлов подходящих для сканирования и кладем их в базу"""
    filelist = []
    for adress, dirs, files in os.walk(screenshetspath):
        for file in files:
            if 'yandex.taximeter' in file:
                if sheckNewFileNameInBase(file):
                    filelist.append("'" + file + "'")
    writeFileNameToSql(filelist)
    print(f'В базу добавлено {len(filelist)} новых файлов \n')


def writeFileNameToSql(list):
    """ Пишем имя файла в базу"""
    reques = True
    with sq.connect('yamen.db') as con:
        cursor = con.cursor()
        for n in list:
            cursor.execute(f"INSERT INTO names_files VALUES(null, {n}, 'Falce')")

def readImagetoText(filename):  # распознает текст в картинке, сохнаняет в строку
    """ Переводим картинку в текст"""
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
    screenshotname = f'{screenshetspath}\{filename}'
    image = cv2.imread(screenshotname)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    config = r'--oem 3 --psm 6'
    string = pytesseract.image_to_string(gray, lang='rus', config=config)
    string2 = string.split()
    return string2

def nameToDate(name):
    """ Из имени файла достаем дату """
    date_str = name.split('_')
    datetimeplus = date_str[1]
    date_split = datetimeplus.split('-')
    date_split.pop(-1)
    date_time_str = ' '.join(date_split)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')
    return date_time_obj


readNewFilesIfYandexToBase()


# i = int(input('Сколько файлов прочитать?'))
j = 0
count = 0

with sq.connect('yamen.db') as con:
    cursor = con.cursor()
    while j < 12:
        name = cursor.execute("SELECT id, name_file FROM names_files WHERE readed = 'Falce' LIMIT 1")
        for i in name:
            id = i[0]
            name = str(i[1])
            stringline = readImagetoText(name)
            filds = readTextToFelds(stringline, name)
            cursor.execute("INSERT INTO readed_text VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", filds)

        cursor.execute('UPDATE names_files SET readed = ? WHERE id = ?', ( True, id))

        count += 1
        j += 1
    print(f'Расшифровано и добавленно в базу новых записей - {count}')


print("\n--- %s seconds ---" % int(time.time() - start_time))
