import argparse

from banco_central import dados_para_csv, dados_para_markdown, serie_temporal

parser = argparse.ArgumentParser()
parser.add_argument("serie")
parser.add_argument("formato")
args = parser.parse_args()

if args.formato == "markdown":
    print(dados_para_markdown(serie_temporal(args.serie)))
elif args.formato == "csv":
    print(dados_para_csv(serie_temporal(args.serie)))
