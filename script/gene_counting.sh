#!/bin/bash

INF=$1
OF=$2
exonic_func="nonsynonymous_SNV"

for f in "$INF"*.out.gz;
do
    awk -f add_germline_somatic.awk <(zcat $f) | tee \
        >(awk \
            -v ef="$exonic_func" \
            -v mt="germline" \
            -f list_genes.awk | sort -u >> ${OF}/germline.tmp) \
        >(awk \
            -v ef="$exonic_func" \
            -v mt="somatic" \
            -f list_genes.awk | sort -u >> ${OF}/somatic.tmp) \
        >/dev/null;
done

cat ${OF}/germline.tmp | sort | uniq -c | sort -nrk 1 | awk '{print $2, $1}' \
    > ${OF}/germline_genes.txt

cat ${OF}/somatic.tmp | sort | uniq -c | sort -nrk 1 | awk '{print $2, $1}' \
    > ${OF}/somatic_genes.txt

rm ${OF}/somatic.tmp ${OF}/germline.tmp
