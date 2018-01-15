#!/bin/bash

INF=$1
RANK=$2  # file containing the gene ranking
PRED=$3  # file of the pathogenic predicted mutations

N=$(cat $RANK | wc -l)

for (( i=1; i<=${N}; i++ ));
do
    for p in "$INF"*.out.gz;
    do
        python scripts/file_merge.py \
            <(zcat ${p} | awk '{print $1,$2,$4,$5,$6}') \
            ${PRED} \
            -k1 1,2,3,4,5 \
            -k2 1,2,4,5,6 \
            -i \
            > p_t_pth.tmp

        # the second key (k2) is the gene name wich is the 
        # fifth column of the resulting intersection p_t_pth.tmp
        python scripts/file_merge.py <(head -n ${i} ${RANK}) p_t_pth.tmp -k1 1 -k2 5 -i | \
           wc -l 

    done | grep -v 0 | wc -l 
done > cumulative_curve_tumor_genes.txt

#for f in "$INF"*.out.gz;
#do
#    awk -f scripts/add_germline_somatic.awk <(zcat $p) | \
#            awk \
#                -v mt="germline" \
#                '{if($8!=ef && $8!="." && tolower($8)!="unknown" && $NF==mt) print $6}' | sort -u
#done | sort | uniq -c | sort -nrk 1 | awk '{print $2, $1}' \
#        > ${OF}/allbutsyn_germline_genes.txt


