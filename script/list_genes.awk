#!/usr/bin/awk -f

BEGIN{}
{if ($8==ef && $NF==mt) print $6;}
END{}
