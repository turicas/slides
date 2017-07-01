import csv

beneficiarios = open('beneficiarios-ufpr.txt').read()
ordens = csv.DictReader(open('ordens-bancarias.csv'))
for ordem in ordens:
    if ordem['favorecidos'] not in beneficiarios:
        print(ordem['favorecidos'])
