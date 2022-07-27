import time

start_time = time.time()
import os
import pytesseract
import cv2
from PIL import Image, ImageDraw

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
screenshotspath = 'C:\PetScaner\Screenshert'
fulllistfiles = []
truelistfile = []
bedlistfiles = []
truetextfile = []
newfiles = 0
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


def readImagetoText(filename):  # распознает текст в картинке, сохнаняет в строку
    # image = cv2.imread(name)
    # image = b_w(image)
    screenshotname = f'C:\PetScaner\Screenshert/{filename}'
    image = cv2.imread(screenshotname)
    # small_image = change_size(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray.show()

    config = r'--oem 3 --psm 6'

    string = pytesseract.image_to_string(gray, lang='rus', config=config)
    string2 = " ".join(string.split())
    return string2

def readImagetoText_2(screenshotname):
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
    img_cv = cv2.imread(f'C:\PetScaner\Screenshert/[{screenshotname}]')

    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

    config = r'--oem 3 --psm 6'
    string_text = pytesseract.image_to_string(img_rgb, lang='rus', config=config)
    string_text_split = " ".join(string_text.split())

    return string_text_split

def change_size(img):  # изменяет размер скрина до оптимального
    height_size = int(float(img.size[1]) / 3)
    width_size = int(float(img.size[0]) / 3)
    new_image = img.resize((width_size, height_size))
    # new_image.show()
    # new_image.save('BW_resize2.jpg')
    return new_image


def read_one(path):
    filename = f'C:\PetScaner\Screenshert/{path}'
    readedtext = readImagetoText(filename)
    print(f'{readedtext}')


def b_w_to_file(path):  # Переводит скрин в ЧБ формат и сохнаняет его в новую папку меняя имя
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

def b_w(image):  # Переводит скрин в ЧБ формат и сохнаняет его в новую папку меняя имя
    image = Image.open(filename)
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.
    factor = 200
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
    image.save('wb.jpg', "JPEG")
    del draw
    return image





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


def parsstr_1(splited):
    """ Сегодня и За заказы - по старому"""
    # date = date(0)
    all_profit = float(0.0)
    cash_profit = 0
    noncach_profin = 0
    orders = 0
    orders_str = ''
    income = 0
    commission = 0
    mileage = 0
    balance = 0
    str_line = splited
    n = 0
    i = 0
    print(str_line)
    all_profit_str = ''

    for step in str_line:     # all_profit - Сегодня
        if step == 'Сегодня':
            n = i
            while True:
                if str_line[n + 1] == '>':
                    break
                else:
                    print(str_line[n + 1])
                    all_profit_str = all_profit_str + str_line[n + 1]
                    n +=1
                    if n > 10:
                        break
            all_profit_str = all_profit_str.replace('Р', '')
            all_profit_str = all_profit_str.replace('}', '')
            all_profit_str = all_profit_str.replace(',', '.')
            all_profit = float(all_profit_str)

            print (f'За сегодня {all_profit}')

        if step == 'За':
            orders_str = str_line[i + 4]
            if orders_str == 'б':
                orders = 6
            else:
                orders = int(orders_str)

            print(f'Заказов {orders}')

        i += 1










readtext = ''
substreng = ('Самозанятый', 'Сегодня', 'За заказы')
true_flag = False
bedlist = ''
oldtruefilelist = []
parsstr = []

readnewfilesifYandex()

read_old_true_file_list()

n = 0
while n <= 1:  # len(listfiles)

    readedtext = readImagetoText(fulllistfiles[n])

    if fulllistfiles[n] == 'Screenshot_2021-07-19-21-37-09-3468_ru.yandex.taximeter.x.jpg':
        print(readedtext)
        pars_str = readedtext.split()
        parsstr_1(pars_str)
        break
    for sub in substreng:
        if readedtext.find(sub) != -1:
            truelistfile.append(fulllistfiles[n])
            truetextfile.append(f'{fulllistfiles[n]} {readedtext}')
            true_flag = True


            break
        else:
            true_flag = False
    if true_flag == False:
        bedlistfiles.append(fulllistfiles[n])
    n += 1
print(f'Подходящих файлов {len(truelistfile)}, битых {len(bedlistfiles)}')

save_resulties()

for text in truetextfile:
    print(text)


print("\n--- %s seconds ---" % int(time.time() - start_time))

