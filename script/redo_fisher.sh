#!/bin/bash

TCGA_DIR=$1
OTG_DIR=$2
N_TCGA=$3
N_OTG=$4
OF=$5

exonic_func="synonymous_SNV"

genes_tcga_germline=${TCGA_DIR}/allbutsyn_germline_genes.txt
genes_tcga_tumor=${TCGA_DIR}/allbutsyn_tumor_genes.txt
genes_otg=${OTG_DIR}/gene_counting_allbutsyn.txt

genes_ctable=${OF}/genes_ctable_allbut${exonic_func}.txt

# union genes otg tcga_germline > res.tmp
python scripts/genes_union.py <(awk '{print $2, $1}' $genes_otg) $genes_tcga_germline > res.tmp

# union genes res.tmp tcga_tumor > merge.txt
python scripts/genes_union.py res.tmp $genes_tcga_tumor > genes_merge.tmp

# compute contingency matrix merge.txt for each line > ctable.txt
# GENE | otg | otg ^mut | tcga germ | tcga germ ^mut | tcga tumor | tcga tumor ^mut |
awk -v nt="$N_TCGA" -v n1kg="$N_OTG" 'OFS="\t"{print $1, $2, n1kg-$2, $3, nt-$3, $4, nt-$4}' genes_merge.tmp > $genes_ctable

# compute fisher test three times:
# 1- 1kg vs tumor tcga
python scripts/computeFisher.py <(awk 'OFS="\t"{print $1, $2, $3, $6, $7}' $genes_ctable) --std | sort -nrk 7 > ${OF}/fisher_1kg_tumor_allbut${exonic_func}.txt

# 2- normal tcga vs tumor tcga
python scripts/computeFisher.py <(awk 'OFS="\t"{print $1, $4, $5, $6, $7}' $genes_ctable) --std | sort -nrk 7 > ${OF}/fisher_tcga_normal_tumor_allbut${exonic_func}.txt

# 3- 1kg vs normal tcga
python scripts/computeFisher.py <(awk 'OFS="\t"{print $1, $2, $3, $4, $5}' $genes_ctable) --std | sort -nrk 7 > ${OF}/fisher_1kg_tcga_normal_allbut${exonic_func}.txt

mv *.tmp trash/
