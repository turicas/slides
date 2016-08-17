import csv


filename = 'examples/data/tesouro-direto.csv'
reader = csv.DictReader(open(filename))
for row in reader:
    print(row)
