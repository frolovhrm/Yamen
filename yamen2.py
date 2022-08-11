import time
import datetime

start_time = time.time()
import os
import pytesseract
import cv2
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'

fulllistfiles = []
truelistfile = []
bedlistfiles = []
truetextfileZan = []
falsetextfile = []
zan = 0
seg = 0
zaza = 0

screenshotspath = 'C:\PetScaner\Screenshert'


def readnewfilesifYandex():  # Выбирает скрины из указанной папки ести они с яндекса и пишет в список
    newfiles = 0
    for adress, dirs, files in os.walk(screenshotspath):
        for file in files:
            if 'yandex.taximeter' in file:
                if files not in fulllistfiles:
                    fulllistfiles.append(file)
                    newfiles += 1
    print(f'Добавленно {newfiles} новых файлов')


def readImagetoText(filename):  # распознает текст в картинке, сохнаняет в строку
    screenshotname = f'C:\PetScaner\Screenshert/{filename}'
    image = cv2.imread(screenshotname)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    config = r'--oem 3 --psm 6'
    string = pytesseract.image_to_string(gray, lang='rus', config=config)
    string2 = " ".join(string.split())
    return string2

def nameToDate(name):
    date_str = name.split('_')
    datetimeplus = date_str[1]
    date_split = datetimeplus.split('-')
    date_split.pop(-1)
    date_time_str = ' '.join(date_split)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y %m %d %H %M %S')
    print('Дата и время:', date_time_obj)



readnewfilesifYandex()


i = 0
while i < 2:
    stringline = readImagetoText(fulllistfiles[i])
    i += 1
    print(i)
    nameToDate(fulllistfiles[i])

    if 'занятый' in stringline:
        zan += 1
        continue
    if 'За заказы' in stringline:
        zaza += 1
        continue
    if 'Сегодня' in stringline:
        seg += 1
        continue
    else:
        falsetextfile.append(stringline)

print(f'Самозанятый {zan}, За заказы {zaza}, Сегодня {seg}, Остальные {len(falsetextfile)}')
for falsetext in falsetextfile:
    print(falsetext)


print("\n--- %s seconds ---" % int(time.time() - start_time))
