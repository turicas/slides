#!/bin/bash


for file in $(ls *.dot); do
    new_filename=$(echo $file | sed 's/\.dot$//g')
    dot -Tpng -o../media/images/$new_filename.png $file

    #dot -Tpng -omedia/images/$new_filename-dot.png $file
    #neato -Tpng -omedia/images/$new_filename-neato.png $file
    #fdp -Tpng -omedia/images/$new_filename-fdp.png $file
done
