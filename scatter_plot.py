#!/usr/bin/python

import sys
import matplotlib.pyplot as plt

f1 = open(sys.argv[1])
pos1 = int(sys.argv[2])-1
f2 = open(sys.argv[3])
pos2 = int(sys.argv[4])-1

x = []
for line in f1:
    n = float(line.rstrip().split()[pos1])
    x.append(n)

y = []
for line in f2:
    n = float(line.rstrip().split()[pos2])
    y.append(n)

if len(x) > len(y):
    x = x[:len(y)]
if len(x) < len(y):
    y = y[:len(x)]

fig, ax = plt.subplots()

ax.scatter(x, y)

plt.draw()
plt.show()
