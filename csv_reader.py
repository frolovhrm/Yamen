import csv

filename = 'test.csv'



with open(filename, mode="w", encoding='utf-8') as w_file:
    names = ["Имя", "Возраст"]
    file_writer = csv.DictWriter(w_file, delimiter = ",", lineterminator="\r", fieldnames=names)
    file_writer.writeheader()
    for i in range(5):
        file_writer.writerow({"Имя": i, "Возраст": i})


# with open(filename, newline='') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)
#
# results = []
# with open(filename) as File:
#     reader = csv.DictReader(File)
#     for row in reader:
#         results.append(row)
#         print (results)
#         results = []
