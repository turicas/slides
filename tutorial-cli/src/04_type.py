import argparse
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
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--formato", choices=EXPORTACAO_FORMATOS.keys(), default=formato_padrao)
parser.add_argument("-m", "--maximo", type=int)
parser.add_argument("serie", choices=SERIES_CODIGOS)
args = parser.parse_args()

dados = serie_temporal(args.serie)
if args.maximo is not None:
    print(f"Tipo de `args.maximo`: {type(args.maximo)}")
    dados = dados[-args.maximo :]
resultado = EXPORTACAO_FORMATOS[args.formato](dados)
print(resultado)
