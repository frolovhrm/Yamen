import cv2
import pytesseract
from PIL import Image
import sqlite3 as sq
import time
from tqdm import tqdm
from parsing import readTextToFelds
import datetime

screenshetspath = 'C:\PetScaner\Screenshert//'
base_name = 'yamen.db'
list_file = []
string_split = []

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

list_file = ['Screenshot_2022-07-28-21-35-07-694_ru.yandex.taximeter.jpg',
            'Screenshot_2022-07-28-21-35-07-694_ru.yandex.taximeter.jpg',
            'Screenshot_2021-08-27-21-12-40-541_ru.yandex.taximeter.jpg',
            'Screenshot_2022-07-29-22-21-52-031_ru.yandex.taximeter.jpg',
            'Screenshot_2022-07-29-22-21-57-130_ru.yandex.taximeter.jpg',
            'Screenshot_2022-07-31-14-52-12-819_ru.yandex.taximeter.jpg',
            'Screenshot_2022-07-31-14-52-17-991_ru.yandex.taximeter.jpg',
            'Screenshot_2022-08-11-23-27-21-520_ru.yandex.taximeter.jpg',
            'Screenshot_2022-08-11-23-27-26-422_ru.yandex.taximeter.jpg']

def nameToDate(name):
    """ Из имени файла достаем дату """
    date_str = name.split('_')
    datetimeplus = date_str[1]
    date_split = datetimeplus.split('-')
    date_split.pop(-1)
    date_time_str = ' '.join(date_split)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')
    # print(date_time_obj )
    return date_time_obj

# with sq.connect(base_name) as con:
#     cursor = con.cursor()
#     cursor.execute(f"SELECT name_file FROM names_files WHERE easyread = 0")
#     list = cursor.fetchall()
#     for i in list:
#         list_file.append(i[0])

# for filename in tqdm(list_file):

for filename in (list_file):
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
    screenshotname = screenshetspath + filename
    image = cv2.imread(screenshotname)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    config = r'--oem 3 --psm 6'
    string = pytesseract.image_to_string(gray, lang='rus', config=config)
    string_split = string.split()
    date = str(nameToDate(filename))
    print(date)
    if date < '2022-04-04 00-00-00':
        print(readTextToFelds(string_split, filename))
    else:
     print('Now type file')



#     string_split.append(string.split())
#
#
# for i in string_split:
#     print(i)
