#!/usr/bin/python

import sys


def genes_union(args):
    '''thakes input two files containing two columns one
    list of genes whith germline mutation or list of genes
    with tumor mutation plus a counting column
    '''
    f_mutgenes_germline = args[0]
    f_mutgenes_tumor = args[1]

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
