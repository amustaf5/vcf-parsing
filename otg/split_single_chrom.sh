#!/bin/bash

file=$1
OUT_DIR=$2

start="10"

    awk -v col="$start" -v out="$OUT_DIR" '{
        if (/^#CHROM/) {
            split($0,data,"\t")
            n=length(data)
            for (i=col; i<=NF; i++) 
                pz_list[i]=$i
        } 
        else {
            if(substr($0,1,1) != "#"){
                split($0,data,"\t")
                for (i=col; i<=n; i++){
                    split(data[i], sp, ":");
                    if (sp[1] != "0|0" && sp[1] != "0" && sp[1] != "."){
                          for (j=1; j<=col-1; j++)
                              printf("%s%s",$j,j==col-1?OFS $data[i] ORS:OFS)>>" out"/"pz_list[pz_i]".vcf.gz"  
                    }
                }
            }
        }
    }' <(zcat -f $file)
