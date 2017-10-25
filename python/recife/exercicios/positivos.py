valor1 = float(input('digite o primeiro: '))
valor2 = float(input('digite o segundo: '))

if valor1 < 0 or valor2 < 0:
    print('me recuso!')
else:
    print((valor1 + valor2) / 2)
