#!/bin/bash

TCGA_DIR=$1
OTG_DIR=$2
N=$3
OF=$4

repeat=10

for ((i=1; i<=$repeat; i++))
do
    out=${OF}$i
    mkdir $out
    . scripts/bootstrap.sh $TCGA_DIR $OTG_DIR $N $out
done 
