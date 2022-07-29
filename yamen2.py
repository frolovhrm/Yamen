import time

start_time = time.time()
import os
import pytesseract
import cv2
from PIL import Image

fulllistfiles = []
truelistfile = []
bedlistfiles = []
truetextfile = []

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
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


def readImagetoText_2(screenshotname):
    path_screen = f'C:\PetScaner\Screenshert/Screenshot_2021-07-19-21-36-53-777_ru.yandex.taximeter.x.jpg'
    img_cv = cv2.imread(path_screen)

    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

    config = r'--oem 3 --psm 6'
    string_text = pytesseract.image_to_string(img_rgb, lang='rus', config=config)
    string_text_split = " ".join(string_text.split())

    return string_text_split


readnewfilesifYandex()

i = 0
while i < 5:
    print(readImagetoText_2(fulllistfiles[i]))
    i += 1



print("\n--- %s seconds ---" % int(time.time() - start_time))