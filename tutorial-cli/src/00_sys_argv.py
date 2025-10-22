import sys

from banco_central import dados_para_csv, dados_para_markdown, serie_temporal

serie = sys.argv[1]
formato = sys.argv[2]

if formato == "markdown":
    print(dados_para_markdown(serie_temporal(serie)))
elif formato == "csv":
    print(dados_para_csv(serie_temporal(serie)))
