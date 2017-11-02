#!/usr/bin/python

import sys
from scipy import stats


def ranking(args):
    '''takes input two files of gene counting
    for different experiments (also two generic number sequence)
    '''
    x_ = list(map(int, open(args[0], 'r').readlines()))
    y_ = list(map(int, open(args[1], 'r').readlines()))

    x, y = normalize(x_, y_)

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

    # taking the column at index of each row of the input file
    x_ = list(map(lambda t: int(t.split()[index]),
                  open(f_exp1, 'r').readlines()))
    y_ = list(map(lambda t: int(t.split()[index]),
                  open(f_exp2, 'r').readlines()))

    x, y = normalize(x_, y_)

    rho, pval = stats.spearmanr(x, y)
    tau, pval_k = stats.kendalltau(x, y)
    pcc, pval_p = stats.pearsonr(x, y)

    return rho, tau, pcc


def normalize(list_a, list_b):
    '''add number of zero in order to have two vectors of same size'''
    len_a = len(list_a)
    len_b = len(list_b)

    if len_a > len_b:
        list_b.extend([0] * (len_a - len_b))
    elif len_a < len_b:
        list_a.extend([0] * (len_b - len_a))

    return list_a, list_b


if __name__ == "__main__":
    ranking(sys.argv[1:])
