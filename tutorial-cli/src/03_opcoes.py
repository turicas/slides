import argparse

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

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--formato", choices=EXPORTACAO_FORMATOS.keys(), default="markdown")
parser.add_argument("serie", choices=SERIES_CODIGOS)
args = parser.parse_args()

dados = serie_temporal(args.serie)
resultado = EXPORTACAO_FORMATOS[args.formato](dados)
print(resultado)
