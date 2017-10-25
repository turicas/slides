valor1 = float(input("Digite um número:"))
valor2 = float(input("Digite outro número:"))

if valor1 < 0 or valor2 < 0:
    print("Só faço com positivos.")
else:
    print((valor1 + valor2) / 2)
