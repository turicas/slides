import csv
from decimal import Decimal

from mercados.bcb import BancoCentral


bc = BancoCentral()
inicio = "2020-01-01"

# Baixa dados da TR por dia
tr_por_data = {
    taxa.data: taxa.valor
    for taxa in bc.serie_temporal("TR", inicio=inicio)
}

# Baixa dados da Selic por dia e calcula rentabilidade da poupança
dados = []
for taxa in bc.serie_temporal("Selic meta", inicio=inicio):
    if taxa.data not in tr_por_data:
        continue
    selic_ao_ano = taxa.valor / 100
    selic_ao_mes = (1 + float(selic_ao_ano)) ** (1 / 12) - 1
    if selic_ao_ano > Decimal("0.085"):
        tr_ao_mes = tr_por_data[taxa.data] / 100
        poupanca_ao_mes = Decimal("0.005") + tr_ao_mes
    else:
        poupanca_ao_mes = 0.70 * selic_ao_mes
    dados.append(
        {"data": taxa.data, "selic_ao_mes": selic_ao_mes, "tr_ao_mes": tr_ao_mes, "poupanca_ao_mes": poupanca_ao_mes}
    )

# Salva resultados em CSV
with open("data/poupanca.csv", mode="w") as fobj:
    writer = csv.DictWriter(fobj, fieldnames=list(dados[0].keys()))
    writer.writeheader()
    writer.writerows(dados)
