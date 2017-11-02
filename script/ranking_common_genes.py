#!/usr/bin/python

import sys
from scipy import stats
from collections import OrderedDict


def commonGenes(file_exp1, file_exp2, index=3):
    '''takes in input two file from two different experiments
    find the common genes in both the files (since
    each experiment due to different parameters give different
    gene lists) and returns two ordered dict (obj) keeping the original order
    with the common genes plus the rank value of each
    '''
    d_exp1 = {}
    d_exp2 = {}

    for line in open(file_exp1, 'r'):
        g = line.split()
        d_exp1[g[0]] = int(g[index])

    for line in open(file_exp2, 'r'):
        g = line.split()
        d_exp2[g[0]] = int(g[index])

    # compute the intersection of the keys of the two dictionay (common values)
    keys_common = set(d_exp1.keys()).intersection(d_exp2.keys())

    # compute dictionary with common keys and original value for each exp
    out_exp1 = {}
    out_exp2 = {}
    for k in keys_common:
        out_exp1[k] = d_exp1[k]
        out_exp2[k] = d_exp2[k]

    # sorting each dicrionary by value
    out_exp1 = OrderedDict(sorted(out_exp1.items(),
                                  key=lambda t: t[1],
                                  reverse=True))
    out_exp2 = OrderedDict(sorted(out_exp2.items(),
                                  key=lambda t: t[1],
                                  reverse=True))

    return out_exp1, out_exp2


def ranking(args):
    '''takes input two files of the gene counting
    with 4 columns: [1]Gene, [2]n of germline mutations,
    [3]n of tumor mutations, [4]difference tumor - germline
    for different experiments (also two generic number sequence)
    '''

    d_exp1, d_exp2 = commonGenes(args[0], args[1])

    x = list(d_exp1.values())
    y = list(d_exp2.values())

    rho, pval = stats.spearmanr(x, y)
    tau, pval_k = stats.kendalltau(x, y)
    pcc, pval_p = stats.pearsonr(x, y)

    print ("==>spearman")
    print (rho, pval)
    print ("==>kendalltau")
    print (tau, pval_k)
    print ("==>pearson")
    print (pcc, pval_p)


def computeCorrelation(f_exp1, f_exp2, index=3):
    '''takes input two files of gene counting
    for different experiments and returns the three correlation coefficents
    '''

    d_exp1, d_exp2 = commonGenes(f_exp1, f_exp2, index)

    x = list(d_exp1.values())
    y = list(d_exp2.values())

    rho, pval = stats.spearmanr(x, y)
    tau, pval_k = stats.kendalltau(x, y)
    pcc, pval_p = stats.pearsonr(x, y)

    return rho, tau, pcc


if __name__ == "__main__":
    ranking(sys.argv[1:])
