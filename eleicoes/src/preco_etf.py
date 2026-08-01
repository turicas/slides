import csv
import datetime
from collections import defaultdict

from mercados.b3 import B3

b3 = B3()
precos_por_data = defaultdict(dict)
for ano in range(2020, 2025 + 1):
    for negocio in b3.negociacao_bolsa("ano", datetime.date(ano, 1, 1)):
        if negocio.codigo_negociacao not in ("BOVA11", "DIVO11"):
            continue
        precos_por_data[negocio.data][negocio.codigo_negociacao] = negocio.preco_ultimo
with open("data/precos-etfs.csv", mode="w") as fobj:
    writer = csv.DictWriter(fobj, fieldnames=["data", "preco_BOVA11", "preco_DIVO11"])
    writer.writeheader()
    for data in precos_por_data.keys():
        row = precos_por_data[data]
        writer.writerow({"data": data, "preco_BOVA11": row.get("BOVA11"), "preco_DIVO11": row.get("DIVO11")})
