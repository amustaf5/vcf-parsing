#!usr/bin/awk -f

BEGIN{} 
{
    if(FNR==NR){pz_list[$1]=$2;next}
    if(!/^#/){
        for(pz_i in pz_list){
            split($pz_i, sp, ":");
            if (sp[1] != "0|0" && sp[1] != "0" && sp[1] != "."){
                printf("%s %s %s %s %s %s %s %s %s %s\n", 
                $1, $2, $3, $4, $5, $6, $7, $8, $9, $pz_i) >> out"/"pz_list[pz_i]".tmp.vcf"
            }
        }
    } 
}
END{}
