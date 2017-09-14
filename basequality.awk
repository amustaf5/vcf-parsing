#!/usr/bin/awk -f

BEGIN{}
{if (!/^#/) split($c, a, ":"); if (a[4] > bq) print $0;}
END{}
