vcf-parsing

script about parsing vcf files

program to filter a vcf-annovar file (.vcf and .gz)
main_vcfannprs.py

usage:

python main_vcfnnprsr.py <vcf_annovar_file.vcf> [options] --out <ouput_directiory/>


options:

-t, --type: 
        [normal | tumor] default= normal

-q, --base_quality:
        int number of the base quality, default= 0

-f, --mutation_frequency:
        float number of the mutation frequency, default= 0.0

--GPV
        float number (exponential notation accepted) of the Germline p-value

--SPV
        float number (exponential notation accepted) of the Somatic p-value

-a, AAFreq
        percentage number (without '%' percentage symbol) of the allele frequency

--out
        path of the directoy where the output file will be saved


example:
python main_vcfnnprsr.py file_name.vcf.gz -t tumor -f 0.60 --GPV 1E-3 -a 50 --out dir/
