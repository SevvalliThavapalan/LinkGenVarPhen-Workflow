#!/bin/bash

# first argument: directory of files e.g: clinical
# second argument: search term e-g: gene name 
# redirect output to file using >  file_name.txt

for f in $1/*gbff.gz; #path needs to be adapted
do
    declare x #makes X an integer
    declare -i y
    
    #echo $f

    x=$(zgrep -A 30 ${2} "$f" | grep -m 1 "/protein_id=") # gets 30 lines after gene name and then fist match with prot ID
    if ! [ -z "$x" ]
    then
        echo -e $x '\t' $f >> $3 # how to add value to a string
    fi

    
done


