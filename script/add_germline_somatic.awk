#!/usr/bin/awk -f

# adding germline or somatic string to last column
# col 16 = NORMAL(a) col 17 = TUMOR(b)
# f=$1 
BEGIN{}
{if (!/^#/) {split($16,a,":"); split($17,b,":"); if(a[1]=="0/0" && b[1]=="0/1") {print $0 "\tsomatic"} else{print $0 "\tgermline"}}}
END{}
