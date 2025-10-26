import csv
from mercados.document import InformeRendimentos
from mercados.fundosnet import FundosNet

fnet = FundosNet()

with open("data/rendimento-xpml11.csv", mode="w") as fobj:
    writer = csv.DictWriter(fobj, fieldnames=["data", "valor"])
    writer.writeheader()
    for doc in fnet.busca(tipo="Rendimentos e Amortizações", cnpj="28.757.546/0001-00", situacao="A"):
        xml = fnet.baixa_xml(doc.url)
        for informe in InformeRendimentos.from_xml(xml):
            writer.writerow({"data": informe.data_pagamento, "valor": informe.valor_por_cota})
