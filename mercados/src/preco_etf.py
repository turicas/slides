import csv
import datetime

from mercados.b3 import B3

b3 = B3()
with open("data/precos-etfs.csv", mode="w") as fobj:
    writer = csv.DictWriter(fobj, fieldnames=["data", "preco_fechamento"])
    writer.writeheader()
    for ano in range(2020, 2025 + 1):
        for negocio in b3.negociacao_bolsa("ano", datetime.date(ano, 1, 1)):
            if negocio.codigo_negociacao not in ("BOVA11", "DIVO11"):
                continue
            writer.writerow({"data": negocio.data, "preco_fechamento": negocio.preco_ultimo})
