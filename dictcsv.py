import csv

with open('Test.csv') as csvfile:
    readers = csv.DictReader(csvfile)
    reader = list(readers)
print(reader)
print(reader[1]["Lat"], " ", reader[1]['Long'], " ", reader[1]['Junction'], " ", reader[1]['Number Junctions'])