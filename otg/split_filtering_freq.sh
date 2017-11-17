#!/bin/bash

CHR_LIST=$1
PZ_LIST=$2
PY_FILTER=$3
OUT_DIR=$4

if [ $(ls "$OUT_DIR"*.out) ]; 
then
    echo "removing all previous output files"
    rm -I "$OUT_DIR"*.out
fi

for chr in $(cat < "$CHR_LIST");
do
    echo $chr
    awk -v out="$OUT_DIR" 'FNR==NR{pz_list[$1]=$2;next}
        !/^#/{
            for (pz_i in pz_list){
                split($pz_i, sp, ":");
                if (sp[1] != "0|0" && sp[1] != "0" && sp[1] != "."){
                    printf("%s %s %s %s %s %s %s %s %s %s\n", 
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $pz_i) > out"/"pz_list[pz_i]".part.vcf"
                } 
            }
        }' $PZ_LIST <(zcat $chr);
    
    for i in $(ls "$OUT_DIR"*.part.vcf);
    do
        echo $i
        # rivedi lo script py per append ooppure esegui loop a partire dai pz poi chr
        # confronta velocita escuzione tra i due diversi loop
        python $PY_FILTER "$i" -f 0.05 --append --out $OUT_DIR
        rm $i
    done
    #rm $OUT_DIR*.part*
done
