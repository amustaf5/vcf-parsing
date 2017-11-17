#!/bin/bash

for i in `cat ~/thesis/data/1kgenomes/toy/chr_files.in`;do awk 'FNR==NR{list[$1]=$2;next}!/^#/{for(p in list) {split($p, sp, ":"); if(sp[1]!="0|0" && sp[1]!="0" && sp[1]!=".") {print $1, $p > "tmp"list[p]".tmp"}}}' <(echo "10 HG00096") <(zcat -f "$i"); for j in `ls *.tmp`;do echo $j; head -n3 $j; done; done;
