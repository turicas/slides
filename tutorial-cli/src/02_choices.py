import argparse

from banco_central import (
    SERIES_CODIGOS,
    dados_para_csv,
    dados_para_markdown,
    serie_temporal,
)

parser = argparse.ArgumentParser()
parser.add_argument("serie", choices=SERIES_CODIGOS)
parser.add_argument("formato", choices=["markdown", "csv"])
args = parser.parse_args()

if args.formato == "markdown":
    print(dados_para_markdown(serie_temporal(args.serie)))
elif args.formato == "csv":
    print(dados_para_csv(serie_temporal(args.serie)))
