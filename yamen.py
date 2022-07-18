import os
import pytesseract
import cv2
# import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import time


start_time = time.time()

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
screenshotspath = 'C:\PetScaner\Screenshert'
listfiles = []
truelistfile = []
newfiles = 0
worklist = ['test.jpg', 'test2.jpg', 'test3.jpg', 'test4.jpg']
numtruefiles = 0
bedfiles = []
one_file = ''


def readnewfilesifYandex():
    newfiles = 0
    for adress, dirs, files in os.walk(screenshotspath):
        for file in files:
            if 'yandex.taximeter' in file:
                if files not in listfiles:
                    listfiles.append(file)
                    newfiles += 1
    print(f'Добавленно {newfiles} новых файлов')


def printlistfiles():
    for file in listfiles:
        print(file)


def readImagetoText(screenshotname):
    # image = cv2.imread(name)
    image = Image.open(screenshotname)
    string = pytesseract.image_to_string(image, lang='rus')
    string2 = " ".join(string.split())
    return string2


def check_one(path):
    # filename = f'C:\PetScaner\Screenshert/{path}'
    filename = 'C:\PetScaner/venv\Yamen/ans.jpg'
    readedtext = readImagetoText(filename)
    print(f'{readedtext}')

def b_w(path):
    filename = f'C:\PetScaner\Screenshert/{path}'

    image = Image.open(filename)
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.
    factor = 100
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = a + b + c
            if (S > (((255 + factor) // 2) * 3)):
                a, b, c = 255, 255, 255
            else:
                a, b, c = 0, 0, 0
            draw.point((i, j), (a, b, c))
    filenameBW = f'C:\PetScaner\Screenshert/BW/BW_{path}'
    image.save(filenameBW, "JPEG")
    del draw



# one_file = 'Screenshot_2021-07-19-21-37-09-368_ru.yandex.taximeter.x.jpg'
#
# bw(one_file)

readnewfilesifYandex()

n = 0
while n <= 10:
    filename = listfiles[n]
    b_w(filename)

    print(n)
    n +=1



# if one_file:
#     check_one(one_file)
# else:
#
#     n = 0
#     readtext = ''
#     substreng1 = ('Самозанятый', 'Сегодня', 'За заказы')
#
#     while n <= 10:  # len(listfiles)
#         filename = f'C:\PetScaner\Screenshert/{listfiles[n]}'
#         readedtext = readImagetoText(filename)
#         # print(f'{n + 1}. {readedtext}')
#         n += 1
#
#         if readedtext.find(substreng1) != -1:
#             truelistfile.append(readedtext)
#             numtruefiles += 1
#         elif readedtext.find(substreng2) != -1:
#             truelistfile.append(readedtext)
#             numtruefiles += 1
#         elif readedtext.find(substreng2) != -1:
#             truelistfile.append(readedtext)
#             numtruefiles += 1
#         else:
#             bedfiles.append(readedtext)
#             print(filename)
#
#     print(f'Подходящих файлов {numtruefiles}')

print("--- %s seconds ---" % (time.time() - start_time))