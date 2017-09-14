#!/usr/bin/awk -f

BEGIN{}
{split($c, a, ":"); if (a[5] == ss) print $0;}
END{}


