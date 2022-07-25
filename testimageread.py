import time

start_time = time.time()
import os
import pytesseract
import cv2
from PIL import Image, ImageDraw

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
img_cv = cv2.imread('C:\PetScaner\Screenshert/Screenshot_2021-07-21-06-17-44-355_ru.yandex.taximeter.x.jpg')

img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)


config = r'--oem 3 --psm 6'
string_text = pytesseract.image_to_string(img_rgb, lang='rus', config=config)
string_text2 = " ".join(string_text.split())

print(string_text)
print(string_text2)


print(f'Время выполнения {int(time.time() - start_time)} сек.')
