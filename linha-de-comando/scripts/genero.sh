#!/bin/bash

echo "name,classification"
sort data/palestrantes.txt | \
	cut -d " " -f 1 | \
	iconv -f utf8 -t ascii//TRANSLIT | \
	tr '[:lower:]' '[:upper:]' | \
	sort | \
	while read nome; do
		echo -e ".mode csv\nSELECT first_name,classification FROM nomes WHERE first_name = '$nome'" | \
			sqlite3 data/db.sqlite
	done
