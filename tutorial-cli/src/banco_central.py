import csv
import datetime
import json
from dataclasses import dataclass
from decimal import Decimal
from io import StringIO
from urllib.request import urlopen

SERIES_CODIGOS = {
    "Selic": 11,
    "IPCA": 433,
    "IPCA-15": 7478,
}


@dataclass
class Taxa:
    data: datetime.date
    valor: Decimal

    @classmethod
    def carrega(cls, registro: dict[str, str]):
        return cls(
            data=datetime.datetime.strptime(registro["data"], "%d/%m/%Y").date(),
            valor=Decimal(registro["valor"]).quantize(Decimal("0.01")),
        )

    def serializa(self):
        return {"data": self.data.isoformat(), "valor": str(self.valor)}


def serie_temporal(nome: str, timeout: float = 5.0) -> list[Taxa]:
    "Baixa histórico de algum indicador do Sistema de Gestão de Séries Temporais (SGS) do Banco Central"
    codigo = SERIES_CODIGOS[nome]
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial=01/01/2024"
    resposta = urlopen(url, timeout=timeout)
    dados_json = resposta.read()
    return [Taxa.carrega(registro) for registro in json.loads(dados_json)]


def dados_para_markdown(dados: list[Taxa]) -> str:
    "Transforma lista de dicionários de série temporal em uma tabela markdown"
    resultado = []
    resultado.append("|    Data    |  Valor  |")
    resultado.append("|------------|---------|")
    for taxa in dados:
        data_fmt = taxa.data.strftime("%d/%m/%Y")
        valor_fmt = f"{taxa.valor:6.2f}%"
        resultado.append(f"| {data_fmt} | {valor_fmt} |")
    return "\n".join(resultado)


def dados_para_csv(dados: list[Taxa]) -> str:
    "Transforma lista de dicionários de série temporal em uma string CSV"
    fobj = StringIO()
    writer = csv.DictWriter(fobj, fieldnames=["data", "valor"])
    writer.writeheader()
    for registro in dados:
        registro_dict = registro.serializa()
        writer.writerow(registro_dict)
    fobj.seek(0)
    return fobj.read()
