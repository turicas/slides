import datetime
from mercados.ibge import IBGE

ibge = IBGE()
inflacao = {}
for taxa in ibge.historico("IPCA"):
    inflacao[taxa.data] = taxa.valor
    print(f"IPCA em {taxa.data}: {taxa.valor}")

valor = 1000
inicio = datetime.date(2020, 1, 15)
fim = datetime.date(2025, 9, 15)
variacao = inflacao[fim] / inflacao[inicio]
valor_ajustado = variacao * valor
print(f"R$ {valor} em {inicio} = R$ {valor_ajustado:.2f} em {fim}")
print(f"R$ {valor} em {fim} = R$ {valor / variacao:.2f} em {inicio}")
