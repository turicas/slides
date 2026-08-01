import csv
import datetime

from mercados.b3 import B3

b3 = B3()
with open("data/precos-xpml11.csv", mode="w") as fobj:
    writer = csv.DictWriter(fobj, fieldnames=["data", "preco_fechamento"])
    writer.writeheader()
    for negocio in b3.negociacao_bolsa("ano", datetime.date(2025, 1, 1)):
        if negocio.codigo_negociacao != "XPML11":
            continue
        writer.writerow({"data": negocio.data, "preco_fechamento": negocio.preco_ultimo})
