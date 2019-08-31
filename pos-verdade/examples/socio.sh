#!/bin/bash

SCHEMA="/home/turicas/projects/socios-brasil/schema-full/socio.csv"
FILENAME="/home/turicas/projects/socios-brasil/data/output-full/socio.csv.gz"

/usr/bin/time rows pgimport --schema="$SCHEMA" "$FILENAME" "$POSTGRESQL_URI" socio
