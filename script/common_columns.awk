#!/usr/bin/awk -f

BEGIN{
    OFS="\t";
    split(cols,c,",")
}
if(NR==FNR){a[$1$2$3$4];next}{if($1$2$4$5 in a) print $0}
END{}
