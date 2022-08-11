import csv

filename = 'test.csv'

with open(filename, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

results = []
with open(filename) as File:
    reader = csv.DictReader(File)
    for row in reader:
        results.append(row)
        print (results)
        results = []
