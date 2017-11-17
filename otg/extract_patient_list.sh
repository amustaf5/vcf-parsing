#!/bin/bash

OTG_DIR=$1
PZ_LIST=$2

start="10"

for chr in "$OTG_DIR"*.vcf.gz;
do
    awk -v col="$start" '{
        if (/^#CHROM/) {
            for (i=col; i<=NF; i++) 
                print $i
        }
    }' <(zcat -f $chr)
done | sort | uniq > $PZ_LIST
