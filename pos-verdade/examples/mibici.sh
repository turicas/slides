#!/bin/bash

set -e

URL="https://datos.jalisco.gob.mx/sites/default/files/historico_de_viajes_programa_mibici_08_2018_0.csv"
FILENAME=$(basename $URL)
CLEAN_FILENAME="mibici.csv.gz"
SQL_FILENAME="mibici-per-day.sql"
OUTPUT_FILENAME="mibici-per-day.csv"

# Download
#wget -O "$FILENAME" "$URL"

# Clean
sed 's/"NA"/""/g' "$FILENAME" | gzip - > "$CLEAN_FILENAME"

# Import
time rows pgimport "$CLEAN_FILENAME" $POSTGRESQL_URI mibici

# Analyze + export
time rows pgexport --is-query $POSTGRESQL_URI "$(cat $SQL_FILENAME)" "$OUTPUT_FILENAME"

# Visualize the result
rows print "$OUTPUT_FILENAME"
