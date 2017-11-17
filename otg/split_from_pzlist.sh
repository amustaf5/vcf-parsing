#!/bin/bash

OTG_DIR=$1
PZ_LIST=$2
OUT_DIR=$3

start="10"

for pz in `cat $PZ_LIST`;
do
    for chr in "$OTG_DIR"*.vcf.gz;
    do
        out_file=$OUT_DIR$pz".vcf"
        
        # possibile alterantiva al primo awk for precalcolare la posizione dei pz
        # per ogni file di chromosoma leggerli nle loop otg_dir
        awk -v col="$start" -v p="$pz" -v out="$out_file" '{
            if (/^#CHROM/) {
                for (i=col; i<=NF; i++) 
                    if($i == p) {
                        pz_i=i 
                        break
                    }
            } 
            else {
                if(!/^#/ && length(pz_i) > 0) {
                    split($pz_i, sp, ":");
                    if (sp[1] != "0|0" && sp[1] != "0" && sp[1] != "."){
                        for (j=1; j<=col-1; j++)
                            printf("%s%s",$j,j==col-1?OFS $pz_i ORS:OFS) >> out
                    }
                }
            }
        }' <(zcat -f $chr)
    done 
    #if [ -f "$out_file" ]
    #then
    #    gzip "$out_file"
    #fi 
done
