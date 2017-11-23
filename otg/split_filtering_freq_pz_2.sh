#!/bin/bash

CHR_LIST=$1
PZ_LIST=$2
PY_FILTER=$3
OUT_DIR=$4


IFS=$'\n'
for pz in $(cat < "$PZ_LIST");
do
    for chr in $(cat < "$CHR_LIST");
    do
        awk -v p="$pz" -v out="$OUT_DIR" '!/^#/{
            split(p, pz_i);
            split($pz_i[1], sp, ":");
            if (sp[1] != "0|0" && sp[1] != "0" && sp[1] != "."){
                printf("%s %s %s %s %s %s %s %s %s %s\n", 
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $pz_i[1]) >> out"/"pz_i[2]".tmp.vcf"
            } 
        }' <(zcat $chr);
    done

    for i in $(ls "$OUT_DIR"*.tmp.vcf);
    do
        # rivedi lo script py per append ooppure esegui loop a partire dai pz poi chr
        # confronta velocita escuzione tra i due diversi loop
        python $PY_FILTER "$i" -f 0.05 --out $OUT_DIR
        rm $i
    done
done
