import cv2
import pytesseract
from PIL import Image
import sqlite3 as sq
import time
from tqdm import tqdm
from parsing import readTextToFelds
from parsing2 import readTextToFelds2

import datetime

screenshetspath = 'C:\PetScaner\Screenshort/'
base_name = 'yamen.db'
list_file = []
string_split = []
string_split_list = []

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


def nameToDate(name):
    """ Из имени файла достаем дату """
    date_str = name.split('_')
    datetimeplus = date_str[1]
    date_split = datetimeplus.split('-')
    date_split.pop(-1)
    date_time_str = ' '.join(date_split)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')
    return date_time_obj

list_file = ['Screenshot_2021-09-02-15-11-43-152_ru.yandex.taximeter.jpg']

# with sq.connect(base_name) as con:
#     cursor = con.cursor()
#     cursor.execute(f"SELECT name_file FROM names_files WHERE easyread = 0")
#     list = cursor.fetchall()
#     for i in list:
#         list_file.append(i[0])

# for filename in tqdm(list_file):

for filename in (list_file):
    # print(filename)
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
    screenshotname = screenshetspath + filename
    image = cv2.imread(screenshotname)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    config = r'--oem 3 --psm 6'
    string = pytesseract.image_to_string(gray, lang='rus', config=config)
    string_split = string.split()
    date = str(nameToDate(filename))
    if date < '2022-04-04 00-00-00':
        fields = readTextToFelds(string_split, filename)
        print('old')
    else:
        fields = readTextToFelds2(string_split, filename)
        print('new')
    string_split_list.append(fields)

for i in string_split_list:
    print(i)
