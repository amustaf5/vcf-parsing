#!/bin/bash

exonic_func="synonymous_SNV"

for i in $(ls data/pathogenic/otg/005/*.out.gz);
do 
    a=$(zcat $i | awk -v ef="$exonic_func" '!/^#/{if($8!=ef && $8!="." && tolower($8)!="unknown") print $6}' | sort -u | wc -l)
    b=$(zcat $i | awk -v ef="$exonic_func" '!/^#/{if($8!=ef && $8!="." && tolower($8)!="unknown") print $6}'| wc -l)
    echo $(basename $i .out.gz) $a $b \
        >> hist_1kg_mutation_tumor_005_5_pred.txt 
done

for i in $(ls myout/otg/005/split/*.out.gz);
do 
    a=$(zcat $i | awk -v ef="$exonic_func" '!/^#/{if($8!=ef && $8!="." && tolower($8)!="unknown") print $6}' | sort -u | wc -l)
    b=$(zcat $i | awk -v ef="$exonic_func" '!/^#/{if($8!=ef && $8!="." && tolower($8)!="unknown") print $6}'| wc -l)
    echo $(basename $i .out.gz) $a $b \
        >> hist_1kg_mutation_tumor_005_5_nofilter.txt 
done

#for i in $(ls data/pathogenic/tcga_sg/005_5/*.out.gz);
#do 
#    a=$(zcat $i | awk -v ef="$exonic_func" '!/^#/{if($8!=ef && $8!="." && tolower($8)!="unknown") print $6}' | sort -u | wc -l)
#    b=$(zcat $i | awk -v ef="$exonic_func" '!/^#/{if($8!=ef && $8!="." && tolower($8)!="unknown") print $6}'| wc -l)
#    echo $(basename $i .vcf.all.Tumor.hc.filter.annovar.hg38_multianno.vcf.gz.out.gz) $a $b \
#        >> TEST_hist_mutation_tumor_005_5_pred.txt 

#    a=$(zcat $i | awk -v ef="$exonic_func" -v mt="somatic" -f scripts/select_mutation.awk | sort -u | wc -l)
#    b=$(zcat $i | awk -v ef="$exonic_func" -v mt="somatic" -f scripts/select_mutation.awk | wc -l)
#    echo $(basename $i .vcf.all.Tumor.hc.filter.annovar.hg38_multianno.vcf.gz.out.gz) $a $b \
#        >> hist_mutation_somatic_005_5_pred.txt 
#
#    c=$(zcat $i | awk -v ef="$exonic_func" -v mt="germline" -f scripts/select_mutation.awk | sort -u | wc -l)
#    d=$(zcat $i | awk -v ef="$exonic_func" -v mt="germline" -f scripts/select_mutation.awk | wc -l)
#    echo $(basename $i .vcf.all.Tumor.hc.filter.annovar.hg38_multianno.vcf.gz.out.gz) $c $d \
#        >> hist_mutation_germline_005_5_pred.txt 
#done 
#
#for i in $(ls myout/tcga_sg/0.005_5/*.out.gz);
#do 
#    a=$(zcat $i | awk -v ef="$exonic_func" '!/^#/{if($8!=ef && $8!="." && tolower($8)!="unknown") print $6}' | sort -u | wc -l)
#    b=$(zcat $i | awk -v ef="$exonic_func" '!/^#/{if($8!=ef && $8!="." && tolower($8)!="unknown") print $6}'| wc -l)
#    echo $(basename $i .vcf.all.Tumor.hc.filter.annovar.hg38_multianno.vcf.gz.out.gz) $a $b \
#        >> TEST_hist_mutation_tumor_005_5_nofilter.txt 

#    a=$(zcat $i | awk -v ef="$exonic_func" -v mt="somatic" -f scripts/select_mutation.awk | sort -u | wc -l)
#    b=$(zcat $i | awk -v ef="$exonic_func" -v mt="somatic" -f scripts/select_mutation.awk | wc -l)
#    echo $(basename $i .vcf.all.Tumor.hc.filter.annovar.hg38_multianno.vcf.gz.out.gz) $a $b \
#        >> hist_mutation_somatic_005_5_nofilter.txt
#
#    c=$(zcat $i | awk -v ef="$exonic_func" -v mt="germline" -f scripts/select_mutation.awk | sort -u | wc -l)
#    d=$(zcat $i | awk -v ef="$exonic_func" -v mt="germline" -f scripts/select_mutation.awk | wc -l)
#    echo $(basename $i .vcf.all.Tumor.hc.filter.annovar.hg38_multianno.vcf.gz.out.gz) $c $d \
#        >> hist_mutation_germline_005_5_nofilter.txt 
#done 
