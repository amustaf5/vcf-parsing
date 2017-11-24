#!/usr/bin/python

import sys
import gzip
from os.path import basename, join


def checkFrequency(freq_list, freq_threshold, null_value="."):
    '''check if the mutation frequency is greater then
    the frequency value given in input
    '''
    res = False

    # if not filtering take the line anyway
    if freq_threshold == 0.0:
        res = True
    else:
        l_freq = []
        # check if there is a point (null value) or a value
        # convert all to float
        if freq_list[0] != null_value:
            l_freq.append(float(freq_list[0]))
        if freq_list[1] != null_value:
            l_freq.append(float(freq_list[1]))
        if freq_list[2] != null_value:
            l_freq.append(float(freq_list[2]))

        # get the max compare return ture or false
        # possibile to have all empty values
        if len(l_freq) != 0:
            if max(l_freq) < freq_threshold:
                res = True

    return res


in_file = sys.argv[1]
freq = float(sys.argv[2])
out_dir = sys.argv[3]

out_file = join(out_dir, basename(in_file))

with gzip.open(in_file, 'rb') as f:
    with gzip.open(out_file, 'wb') as of:
        for line in f:
            if line.startswith("#"):
                continue
            cols = line.strip().split()
            # get three values of freq from proper columns
            freq_list = [cols[10], cols[11], cols[12]]

            if checkFrequency(freq_list, freq):
                of.write(line)

        f.close()
        of.close()
