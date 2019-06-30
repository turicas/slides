#!/bin/bash

wget --quiet -O - "http://congresso.abraji.org.br/Salas/" \
    | grep '"label"' \
    | sed 's/.*<b>//; s/<\/b>.*//' \
    | grep -v 'A confirmar' \
    | sort -u \
    > palestrantes.txt
