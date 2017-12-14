#!/bin/bash

FILE=$1
PV=$2
VAL=$3

col=
if [$PV=="GPV"]; then
    col='14';
elif [$PV=="SPV"]; then
    col='15';
fi

awk -v c="$col" -v v="$VAL" -f outvcfcolfilter.awk <(zcat $FILE)
