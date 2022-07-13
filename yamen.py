import os
import pytesseract
import cv2
# import matplotlib.pyplot as plt
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'


""" 
1. Заходим в папку и собираем список всех файлов, если файла нет добавляет в рабочий список
2. Сканируем и распознаем файлы из рабочего списка, новые данные пишем в базу
3.
"""

listfiles = []
newfiles = 0
pathscrfold = 'C:\PetScaner\Screenshert'


def readnewfiles():
    newfiles = 0
    for adress, dirs, files in os.walk(pathscrfold):
        for file in files:
            if 'yandex.taximeter' in file:
                if files not in listfiles:
                    listfiles.append(file)
                    newfiles += 1
    print(f'Добавленно {newfiles} новых файлов')

def printlistfiles():
    for file in listfiles:
        print(file)

def readImage(name):
    # image = cv2.imread(name)
    image = Image.open(name)
    string = pytesseract.image_to_string(image, lang='rus')
    print(string)


readnewfiles()

testfile = "test2.png"
readImage(testfile)
