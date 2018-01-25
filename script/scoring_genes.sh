#!/bin/bash

GENOME=$1 # genome file of an individual extracted from vcf files and filtered
RANK=$2 # ranking file with genes and a score
TYPEMUT=$3 # type of mutation to select in an individual somatic|germline|tumor

exonic_func="synonymous_SNV"

if [ "$TYPEMUT" == "tumor" ]; then
    zcat $GENOME | awk -v ef="$exonic_func" '!/^#/{if($8!=ef && $8!="." && tolower($8)!="unknown") print $6}' | sort -u > genesel.tmp
else    
    zcat $GENOME | awk -v ef="$exonic_func" -v mt="$TYPEMUT" -f scripts/select_mutation.awk | sort -u > genesel.tmp 
fi
python scripts/file_merge.py genesel.tmp $RANK -k1 0 -k2 0 --intersect

rm genesel.tmp

