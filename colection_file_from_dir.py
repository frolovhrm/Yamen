import os
import shutil

folderpath = "C:/PetScaner/Screenshert2"
destinationfolder = "C:/PetScaner/Screenshert2/1"
count = 0


# folderpath = input('Введите путь к папке с новым сканам: ')

for files in os.walk(folderpath):
    print(len(files[2]))
    for file in files[2]:
        if 'yandex.taximete' in file:
            file1 = f'{folderpath}\\{file}'
            file2 = f'{destinationfolder}\\{file}'
            shutil.copyfile(file1, file2)
            count += 1
        print(f'{count} - {file}')

print(f'Найдено {count} новый файлов.')
