#!/bin/bash

INPUT="contracheque.csv"
head -1 "$INPUT"  # header
grep --color=no -i "$1" "$INPUT"
