#!/bin/bash

FOLDER=$1
OUTPTH=$2

if [ ! -d "$OUTPTH" ]; then
    mkdir $OUTPTH;
fi

# path to python program
vcfparsing="/home/renzo/thesis/github_repository/main_vcfnnvrprsr.py"

# arrays containing all possibile values
pop_frequency_list=(0.005 0.01 0.05)
AD1=5
AD2=10
AAFreq=5

# loop for each pop freq value
for pf in "${pop_frequency_list[@]}";
do
    OF1="${OUTPTH}/${pf}_${AD1}"
    OF2="${OUTPTH}/${pf}_${AD2}"

    mkdir $OF1 2>/dev/null
    mkdir $OF2 2>/dev/null
    
    for f in "$FOLDER"*.vcf.gz;
    do
        echo "file in lettura" $f
        python2 $vcfparsing $f \
           -t tumor \
           -f ${pf} \
           --AD ${AD1} \
           --AAFreq ${AAFreq} \
           --out $OF1 &\
        python2 $vcfparsing $f \
           -t tumor \
           -f ${pf} \
           --AD ${AD2} \
           --AAFreq ${AAFreq} \
           --out $OF2;
    done 
done
