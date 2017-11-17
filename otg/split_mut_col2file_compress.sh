#!/bin/bash

OTG_DIR=$1
OUT_DIR=$2

start="10"

for chr in "$OTG_DIR"*.vcf.gz;
do
    awk -v col="$start" -v out="$OUT_DIR" '{
        if (/^#CHROM/) {
            for (i=col; i<=NF; i++) 
                pz_list[i]=$i
        } 
        else {
            for (pz_i in pz_list){
                split($pz_i, sp, ":");
                if (sp[1] != "0|0" && sp[1] != "0" && sp[1] != "."){
                    command = "gzip -c >>" out"/"pz_list[pz_i]".vcf.gz" 
                    for (j=1; j<=col-1; j++)
                        printf("%s%s",$j,j==col-1?OFS $pz_i ORS:OFS) | command
                }
            }
        }
    }' <(zcat -f $chr)
done
