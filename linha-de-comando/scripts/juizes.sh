#!/bin/bash

echo "Número de linhas do arquivo inicial:"
wc -l contracheque.csv

echo "Criando arquivo com Moro e Bruno..."
head -1 contracheque.csv > juizes.csv
grep --color=no -i "SERGIO FERNANDO MORO" contracheque.csv >> juizes.csv
grep --color=no -i "BRUNO SOUZA SAVINO" contracheque.csv >> juizes.csv
echo "Arquivo criado. Total de linhas: $(wc -l juizes.csv)"
