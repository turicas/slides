import argparse
import datetime
import os
import re
import sys

from banco_central import (
    SERIES_CODIGOS,
    dados_para_csv,
    dados_para_markdown,
    serie_temporal,
)

EXPORTACAO_FORMATOS = {
    "markdown": dados_para_markdown,
    "md": dados_para_markdown,
    "csv": dados_para_csv,
}


def extrai_data(valor):
    if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", valor):
        return datetime.datetime.strptime(valor, "%Y-%m-%d").date()
    elif re.match("[0-9]{2}/[0-9]{2}/[0-9]{4}", valor):
        return datetime.datetime.strptime(valor, "%d/%m/%Y").date()
    raise argparse.ArgumentTypeError(f"Formato de data não reconhecido para {repr(valor)}")
    # `ValueError` e `TypeError` também são coletados pelo parser


formato_padrao = os.environ.get("FORMATO_BC", "markdown")
choices_series = sorted(SERIES_CODIGOS.keys())
formatos_choices = sorted(EXPORTACAO_FORMATOS.keys())
parser = argparse.ArgumentParser(prog="bcb", description="Coleta dados de séries temporais do Banco Central")
parser.add_argument(
    "-F",
    "--formato",
    choices=formatos_choices,
    metavar="fmt",
    default=formato_padrao,
    help=f"Formato de arquivo de saída. Opções: {', '.join(formatos_choices)}.",
)
parser.add_argument(
    "-f",
    "--final",
    type=extrai_data,
    metavar="data",
    help=f"Data de corte final (exclusive)",
)
parser.add_argument(
    "-i",
    "--inicio",
    type=extrai_data,
    metavar="data",
    help=f"Data de corte inicial (inclusive)",
)
parser.add_argument(
    "-m",
    "--maximo",
    type=int,
    metavar="n",
    help="Máximo de registros a exibir (começa a partir do último)",
)
stderr_group = parser.add_mutually_exclusive_group()
stderr_group.add_argument(
    "-q",
    "--quiet",
    action="store_true",
    help="Omite mensagens de status",
)
stderr_group.add_argument(
    "--verbose",
    action="store_true",
    help="Mostra o máximo de mensagens de status",
)
parser.add_argument(
    "-v",
    "--version",
    "--versao",
    action="version",
    version="%(prog)s 1.0.0",
    help="Exibe a versão atual do programa.",
)
parser.add_argument(
    "serie",
    choices=choices_series,
    metavar="serie",
    help=f"Código da série. Opções: {', '.join(choices_series)}.",
)
args = parser.parse_args()

if args.verbose:
    print(f"Baixando dados de para {args.serie}")
dados = serie_temporal(args.serie)
if args.verbose:
    print(f"Capturados dados de {dados[-1].data} a {dados[-1].data}.", file=sys.stderr)
if args.inicio:
    dados = [registro for registro in dados if registro.data >= args.inicio]
if args.final:
    dados = [registro for registro in dados if registro.data < args.final]
if args.maximo:
    qtd_antes = len(dados)
    dados = dados[-args.maximo :]
    qtd_depois = len(dados)
    if args.verbose:
        print(f"Dados filtrados de {qtd_antes} para {qtd_depois} registros.")
resultado = EXPORTACAO_FORMATOS[args.formato](dados)
print(resultado)
