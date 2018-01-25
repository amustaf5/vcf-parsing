#!/bin/bash

GENOME1=$1
GENOME2=$2
RANK=$3
TYPEMUT=$4

./scripts/scoring_genes.sh $GENOME1 $RANK $TYPEMUT | awk '{print $NF}' > series_1.tmp
./scripts/scoring_genes.sh $GENOME2 $RANK $TYPEMUT | awk '{print $NF}' > series_2.tmp

python scripts/computeKS.py series_1.tmp series_2.tmp



