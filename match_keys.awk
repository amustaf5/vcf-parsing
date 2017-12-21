#!/usr/bin/awk -f

BEGIN{
    OFS="\t";
    split(cols1,c1,",");
    split(cols2,c2,",");
}
{
    if(NR==FNR){
        key1 = ""
        for(i in c1){
            if (length(key1)==0){
                key1 = $c1[i]
            }
            else{
                key1 = key1"_"$c1[i]
            }
        }
        a[key1]=$0;
    }
    else{
        key2 = ""
        for(i in c2){
            if (length(key2)==0){
                key2 = $c2[i]
            }
            else{
                key2 = key2"_"$c2[i]
            }
        }
        b[key2]=$0;
        if(key2 in a){
            print $0
        }
    }
}
END{}

