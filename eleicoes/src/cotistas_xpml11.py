import csv
from mercados.document import InformeFII
from mercados.fundosnet import FundosNet

fnet = FundosNet()

with open("data/cotistas-xpml11.csv", mode="w") as fobj:
    writer = csv.DictWriter(fobj, fieldnames=["data", "cotistas"])
    writer.writeheader()
    for doc in fnet.busca(tipo="Informe Mensal Estruturado", cnpj="28.757.546/0001-00", situacao="A"):
        xml = fnet.baixa_xml(doc.url)
        for informe in InformeFII.from_xml(xml):
            writer.writerow({"data": informe.competencia, "cotistas": informe.dados["Cotistas"]["@total"]})
