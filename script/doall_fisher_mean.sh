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
    for mut in "${MUT_TYPE[@]}";
    do
        for ((i=0; i<10; i++));
        do
            mt=
            case $mut in
                syn) mt="synonymous_SNV.txt";;
                nonsyn) mt="nonsynonymous_SNV.txt";;
                allbutsyn) mt="allbutsynonymous_SNV.txt";;
            esac

            # extract the lists of paths needed for computing the mean
            readlink -f /home/um99/rnz/data/bootstrap/${p}/${mut}/${i}/fisher_1kg_tcga_normal_${mt} >> paths_1tn.tmp
            readlink -f /home/um99/rnz/data/bootstrap/${p}/${mut}/${i}/fisher_1kg_tumor_${mt} >> paths_1tt.tmp
            readlink -f /home/um99/rnz/data/bootstrap/${p}/${mut}/${i}/fisher_tcga_normal_tumor_${mt} >> paths_tnt.tmp
        done

        # compute mean on current experiment for current mut type
        python scripts/compute_average_generic.py paths_1tn.tmp 0 1,2,3,4,6 | sort -nrk6 > /home/um99/rnz/data/bootstrap/${p}/${mut}/mean_1kg_tnormal.txt
        python scripts/compute_average_generic.py paths_1tt.tmp 0 1,2,3,4,6 | sort -nrk6 > /home/um99/rnz/data/bootstrap/${p}/${mut}/mean_1kg_ttumor.txt
        python scripts/compute_average_generic.py paths_tnt.tmp 0 1,2,3,4,6 | sort -nrk6 > /home/um99/rnz/data/bootstrap/${p}/${mut}/mean_tcga.txt

        mv *.tmp trash/ 
    done
done

