import argparse
import sys
import os

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

formato_padrao = os.environ.get("FORMATO_BC", "markdown")
choices_series = sorted(SERIES_CODIGOS.keys())
formatos_choices = sorted(EXPORTACAO_FORMATOS.keys())
parser = argparse.ArgumentParser(prog="bcb", description="Coleta dados de séries temporais do Banco Central")
parser.add_argument(
    "-f",
    "--formato",
    choices=formatos_choices,
    metavar="fmt",
    default=formato_padrao,
    help=f"Formato de arquivo de saída. Opções: {', '.join(formatos_choices)}.",
)
parser.add_argument(
    "-m",
    "--maximo",
    type=int,
    metavar="n",
    help="Máximo de registros a exibir (começa a partir do último)",
)
parser.add_argument(
    "-q",
    "--quiet",
    action="store_true",
    help="Omite mensagens de status",
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

dados = serie_temporal(args.serie)
if not args.quiet:
    print(f"Capturados dados de {dados[-1].data} a {dados[-1].data}.", file=sys.stderr)
if args.maximo:
    dados = dados[-args.maximo :]
resultado = EXPORTACAO_FORMATOS[args.formato](dados)
print(resultado)
