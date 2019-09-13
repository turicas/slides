#!/bin/bash

SCHEMA="/home/turicas/projects/socios-brasil/schema-full/empresa.csv"
FILENAME="/home/turicas/projects/socios-brasil/data/output-full/empresa.csv.xz"

time rows pgimport --schema="$SCHEMA" "$FILENAME" "$POSTGRESQL_URI" empresa
