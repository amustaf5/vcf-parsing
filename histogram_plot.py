#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

f = open(sys.argv[1])
pos = int(sys.argv[2])-1
nbin = int(sys.argv[3])

v = []
for line in f:
    n = float(line.rstrip().split()[pos])
    v.append(n)

fig, ax = plt.subplots()

n, bins, patches = ax.hist(v, nbin)


fig.tight_layout()
plt.show()

#print hist

