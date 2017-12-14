#!/usr/bin/awk -f

BEGIN{}
{if($c<=val) print $0}
END{}
