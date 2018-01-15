#!/bin/bash

INF=$1
RANK=$2  # file containing the gene ranking
PRED=$3  # file of the pathogenic predicted mutations

START=$4
END=$5 # (cat $RANK | wc -l)

declare -a RES=()
declare -a GER=()
declare -a SOM=()

for p in $(ls "$INF"*.out.gz);
do
    # selecting all the mutation (tumor) that are also predicted as pathogenic
    python scripts/file_merge.py \
        <(zcat ${p} | awk '{print $1,$2,$4,$5,$6}') \
        ${PRED} \
        -k1 1,2,3,4,5 \
        -k2 1,2,3,4,5 \
        --intersect \
        > p_t_pth_${START}_${END}.tmp

    # selecting only germline mutation in current patient that are also predicted as pathogenic
    python scripts/file_merge.py \
        <(zcat $p | awk -f scripts/add_germline_somatic.awk | awk -v mt="germline" '{if($NF==mt) print $1,$2,$4,$5,$6}') \
        ${PRED} \
        -k1 1,2,3,4,5 \
        -k2 1,2,3,4,5 \
        --intersect \
        > p_germ_pth_${START}_${END}.tmp

    # selecting only somatic mutation in current patient that are also predicted as pathogenic
    python scripts/file_merge.py \
        <(zcat $p | awk -f scripts/add_germline_somatic.awk | awk -v mt="somatic" '{if($NF==mt) print $1,$2,$4,$5,$6}') \
        ${PRED} \
        -k1 1,2,3,4,5 \
        -k2 1,2,3,4,5 \
        --intersect \
        > p_soma_pth_${START}_${END}.tmp

    for (( j=${START}; j<=${END}; j++ ));
    do
        # the second key (k2) is the gene name wich is the 
        # fifth column of the resulting intersection p_t_pth.tmp
        count=$(python scripts/file_merge.py <(head -n ${j} ${RANK}) p_t_pth_${START}_${END}.tmp -k1 1 -k2 5 --intersect | wc -l)
        if (( count > 0 )); then
            ((RES[$j]++))
        fi

        # germline
        countGER=$(python scripts/file_merge.py <(head -n ${j} ${RANK}) p_germ_pth_${START}_${END}.tmp -k1 1 -k2 5 --intersect | wc -l)
        if (( countGER > 0 )); then
            ((GER[$j]++))
        fi

        # somatic
        countSOM=$(python scripts/file_merge.py <(head -n ${j} ${RANK}) p_soma_pth_${START}_${END}.tmp -k1 1 -k2 5 --intersect | wc -l)
        if (( countSOM > 0 )); then
            ((SOM[$j]++))
        fi
    done 
done

printf '%s\n' "${RES[@]}" > cumulative_curve_tumor_genes_${START}_${END}.txt
printf '%s\n' "${GER[@]}" > cumulative_curve_germline_genes_${START}_${END}.txt
printf '%s\n' "${SOM[@]}" > cumulative_curve_somatic_genes_${START}_${END}.txt
