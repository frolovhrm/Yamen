import time

start_time = time.time()
import os
import pytesseract
import cv2
# import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
screenshotspath = 'C:\PetScaner\Screenshert'
listfiles = []
truelistfile = []
newfiles = 0
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
    image = change_size(Image.open(screenshotname))

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
    filename = f'C:\PetScaner\Screenshert/BW/BW_{path}'
    image.save(filename, "JPEG")
    del draw

def change_size(img):
    height_size = int(float(img.size[1]) / 3)
    width_size = int(float(img.size[0]) / 3)
    new_image = img.resize((width_size, height_size))
    # new_image.show()
    # new_image.save('BW_resize2.jpg')
    return new_image



readtext = ''
substreng = ('Самозанятый', 'Сегодня', 'За заказы')
true_flag = False

readnewfilesifYandex()

n = 0
while n <= 10:  # len(listfiles)
    filename = f'C:\PetScaner\Screenshert/{listfiles[n]}'
    readedtext = readImagetoText(filename)
    n += 1
    for sub in substreng:
        if readedtext.find(sub) != -1:
            truelistfile.append(readedtext)
            numtruefiles += 1
            true_flag = True
            break
        else:
            true_flag = False
    if true_flag == False:
        bedfiles.append(f'{filename} -----> {readedtext}')

print(f'Подходящих файлов {numtruefiles}, битых {len(bedfiles)}')

for i in truelistfile:
    print(i)
print()

print("--- %s seconds ---" % int(time.time() - start_time))
