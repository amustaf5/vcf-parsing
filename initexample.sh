#!/bin/bash

#table_annovar.pl example/ex1.avinput humandb/ -buildver hg19 -out myanno -remove -protocol refGene,cytoBand,exac03,avsnp147,dbnsfp30a -operation gx,r,f,f,f -nastring . -csvout -polish -xref example/gene_xref.txt

VCFIN=$1
DB=$2

table_annovar.pl "$VCFIN" "$DB" -buildver hg19 -out myanno -remove -protocol refGene,AFR.sites.2015_08,ALL.sites.2015_08,AMR.sites.2015_08,EAS.sites.2015_08,EUR.sites.2015_08,SAS.sites.2015_08 -operation g,f,f,f,f,f,f -nastring . -vcfinput
