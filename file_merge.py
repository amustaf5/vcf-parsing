#!/usr/bin/python

import sys


def file_merge(args):
    '''takes input two files containing n columns
    a comma separated string of key cols file1 and 2
    '''
    file_one = args[0]
    file_two = args[1]
    keys_one = args[2]
    keys_two = args[3]

    d_germ = {}
    d_tumor = {}
    d_union = {}

    for line in open(f_mutgenes_germline, 'r'):
        e = line.split()
        d_germ[e[0]] = int(e[1])

    for line in open(f_mutgenes_tumor, 'r'):
        e = line.split()
        d_tumor[e[0]] = int(e[1])

    # compute the union of the keys of the two dictionaryes
    keys_union = set(d_germ.keys()).union(d_tumor.keys())

    # for each keys create entry in d_union with sum of
    # the values of germline and tumor genes if present
    # else assign zero
    for k in keys_union:
        d_union[k] = d_germ.get(k, 0), d_tumor.get(k, 0)
        print (k, d_union[k][0], d_union[k][1])

    return d_union


if __name__ == "__main__":
    genes_union(sys.argv[1:])
