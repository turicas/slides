#!/bin/bash

INPUT="contracheque.csv"
head -1 "$INPUT"
grep --color=no -i "$1" "$INPUT" | \
	cut -d "," -f 2,15,20,22 | \
	sort
