#!/bin/bash

# generic script to execute same command on all myout folders

#p1="myout/tcga/0.005_10/" 
#p2="myout/tcga/0.005_5/"
#p3="myout/tcga/0.05_10/"
#p4="myout/tcga/0.05_5/"
#p5="myout/tcga/0.01_10/"
#p6="myout/tcga/0.01_5/"

#PATHLIST=($p1 $p2 $p3 $p4 $p5 $p6)
PATHLIST=("01_5" "01_10" "005_5" "005_10" "05_5" "05_10")
MUT_TYPE=("syn" "nonsyn" "allbutsyn")

for p in "${PATHLIST[@]}";
do
    out=tables/fisher_test/${p}/allbutsyn
    mkdir -p $out
    ./scripts/redo_fisher.sh myout/tcga/0.${p}/new/ myout/otg/${p%_*}/ 525 2504 $out 
done

