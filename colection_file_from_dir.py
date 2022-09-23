import os

folderpath = "C:/PetScaner/Screenshert2/"
destinationfolder = "C:/PetScaner/Screenshert3/"
count = 0

q = input('Сейчас будет просканирован каталог со скринами, все подходящие файлы\n'
          'будут перемещены в рабочий каталог (n - выход) - ')
if q == 'n' or q == 'н':
    exit()

for files in os.walk(folderpath):
    for file in files[2]:
        if 'yandex.taximete' in file:
            os.replace(folderpath + file, destinationfolder + file)
            count += 1
print(f'Перемещено {count} файлов.')
