#!/bin/bash

FOLDER=$7
OUTF=$8

if [ ! -d "$OUTF" ]; then
    mkdir $OUTF;
fi

base_quality=
sstatus=
while getopts q:s:t: opt
do
    case $opt in
        q)  printf "option -q triggered \n"
            base_quality="$OPTARG";;
        s)  printf "option -s triggered \n"
            sstatus="$OPTARG";;
        t)  TYPESEL="$OPTARG";;
        ?)  printf "usage -t -q ..." $0
            exit 2;;
    esac       
done

col=
case $TYPESEL in
    normal)  col='10';;
    primary) col='11';;
    *) echo "tipo errato"
esac

for f in "$FOLDER"*;
do
    of=${OUTF}${f##*/}.out;
    awk -v c="$col" -v bq="$base_quality" -f basequality.awk $f > vcf.tmp;

    if [ ! -z ${sstatus+x} ]; then
        awk -v c="$col" -v ss="$sstatus" -f germorsomatic.awk vcf.tmp > $of;
    fi
done

rm vcf.tmp
