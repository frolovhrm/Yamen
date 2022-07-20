import time

start_time = time.time()
import os
import pytesseract
import cv2
# import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
screenshotspath = 'C:\PetScaner\Screenshert'
fulllistfiles = []
truelistfile = []
newfiles = 0
bedlistfiles = []
one_file = ''


def readnewfilesifYandex():  # Выбирает скрины из указанной папки ести они с яндекса и пишет в список
    newfiles = 0
    for adress, dirs, files in os.walk(screenshotspath):
        for file in files:
            if 'yandex.taximeter' in file:
                if files not in fulllistfiles:
                    fulllistfiles.append(file)
                    newfiles += 1
    print(f'Добавленно {newfiles} новых файлов')


def readImagetoText(screenshotname):  # распознает текст в картинке, сохнаняет в строку
    # image = cv2.imread(name)
    image = change_size(Image.open(screenshotname))

    string = pytesseract.image_to_string(image, lang='rus')
    string2 = " ".join(string.split())
    return string2


def read_one(path):
    filename = f'C:\PetScaner\Screenshert/{path}'
    readedtext = readImagetoText(filename)
    print(f'{readedtext}')


def b_w(path):  # Переводит скрин в ЧБ формат и сохнаняет его в новую папку меняя имя
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


def change_size(img):  # изменяет размер скрина до оптимального
    height_size = int(float(img.size[1]) / 3)
    width_size = int(float(img.size[0]) / 3)
    new_image = img.resize((width_size, height_size))
    # new_image.show()
    # new_image.save('BW_resize2.jpg')
    return new_image


def save_resulties():  # Записывает в файлы результаты работы, списки обработаных файлов
    fullfile = open('fulllist.txt', 'w+')
    for st in fulllistfiles:
        fullfile.write(st)
    fullfile.close()

    truefile = open('truelist.txt', 'w')
    for st in truelistfile:
        truefile.write(st)
    truefile.close()

    bedfile = open('bedlist.txt', 'w')
    for st in bedlistfiles:
        bedfile.write(st)
    bedfile.close()


def read_old_true_file_list():  # Читает файл с сохраненным списком файлов пригодных для парсинга
    try:
        oldfile = open("truelist.txt")
        readfile = oldfile.read()
        oldtruefilelist = readfile.split()
        oldfile.close()
        return oldtruefilelist
    except FileNotFoundError:
        quest = input('Старый список файлов не обнаружен. Cоздать новый truelist.txt? (Y/N) \n')
        if quest == 'n':
            print('Тогда пока')
            quit()
        else:
            print('Будет создан новый список')

def read_old_full_list_files():  # Читает файл с сохраненным списком всех скринов
    try:
        oldfile = open("fulllist.txt")
        readfile = oldfile.read()
        oldfulllistfiles = readfile.split()
        oldfile.close()
        return oldfulllistfiles
    except FileNotFoundError:
        quest = input('Старый список файлов не обнаружен. Cоздать новый truelist.txt? (Y/N) \n')
        if quest == 'n':
            print('Тогда пока')
            quit()
        else:
            print('Будет создан новый список')


readtext = ''
substreng = ('Самозанятый', 'Сегодня', 'За заказы')
true_flag = False
bedlist = ''
oldtruefilelist = []

readnewfilesifYandex()

read_old_true_file_list()

n = 0
while n <= 50:  # len(listfiles)
    filename = f'C:\PetScaner\Screenshert/{fulllistfiles[n]}'
    readedtext = readImagetoText(filename)
    n += 1
    for sub in substreng:
        if readedtext.find(sub) != -1:
            truelistfile.append(fulllistfiles[n])
            true_flag = True
            break
        else:
            true_flag = False
    if true_flag == False:
        bedlistfiles.append(fulllistfiles[n])

print(f'Подходящих файлов {len(truelistfile)}, битых {len(bedlistfiles)}')

save_resulties()

print("--- %s seconds ---" % int(time.time() - start_time))
