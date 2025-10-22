import argparse

from banco_central import (
    SERIES_CODIGOS,
    dados_para_csv,
    dados_para_markdown,
    serie_temporal,
)

EXPORTACAO_FORMATOS = {
    "markdown": dados_para_markdown,
    "csv": dados_para_csv,
}

parser = argparse.ArgumentParser()
parser.add_argument("serie", choices=SERIES_CODIGOS)
parser.add_argument("formato", choices=EXPORTACAO_FORMATOS.keys())
args = parser.parse_args()

dados = serie_temporal(args.serie)
resultado = EXPORTACAO_FORMATOS[args.formato](dados)
print(resultado)
