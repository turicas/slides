valor1 = float(input("Digite um número:"))
valor2 = float(input("Digite outro número:"))

if valor1 >= 9000 and valor2 >= 9000:
    print("OVER 9K!")
    resposta = input('quer calcular a media?')
    if resposta.lower() == 'sim':
        media = (valor1 + valor2) / 2
        print(media)
else:
    print("Valores baixos =/")
