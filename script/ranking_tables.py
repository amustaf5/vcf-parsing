#!/usr/bin/python

import sys
from os import path
import ranking_zero as zero
import ranking_common_genes as comm


def computingCorrelationMatrices(args):
    '''takes in input all the directiories of each experiment
    to compare computing three different correlation coefficent
    returns six matrices in csv format composed by two triangular
    matrices put togheter one computed adding zeros the other
    considering only common genes in order to have comparable
    series of numbers (same dimension)
    '''
    n_experiments = len(args)
    file_nonsyn = "nonsyn_union_genes.txt"
    file_allbutsyn = "allbutsyn_union_genes.txt"

    # tables key=(type_exp, exp1, exp2) value=correlation coefficient
    nonsyn_spearman = {}
    nonsyn_kendalltau = {}
    nonsyn_pearson = {}
    allbutsyn_spearman = {}
    allbutsyn_kendalltau = {}
    allbutsyn_pearson = {}

    for i in range(n_experiments):
        for j in range(i+1, n_experiments):
            path_exp1 = args[i]
            path_exp2 = args[j]

            # partial keys of each dictionary
            key_i = path.basename(path.normpath(path_exp1))
            key_j = path.basename(path.normpath(path_exp2))

            # two different keys for different methods of computing
            # correlation in order to have all the value on the same
            # matrix, since they are two triangular matrix
            # (each comparison is made once)
            k_zero = (key_i, key_j)
            k_comm = (key_j, key_i)

            # NONSYN
            # taking the path of files containg the ranking for each experiment
            f_nonsyn_exp1 = path.join(path_exp1, file_nonsyn)
            f_nonsyn_exp2 = path.join(path_exp2, file_nonsyn)

            # computing the correlation coefficent for non syn experiment
            # considering only common genes and adding zero values
            # in order to have same array size
            z_coeff = zero.computeCorrelation(f_nonsyn_exp1, f_nonsyn_exp2)
            c_coeff = comm.computeCorrelation(f_nonsyn_exp1, f_nonsyn_exp2)

            # adding values to matrices
            nonsyn_spearman[k_zero] = z_coeff[0]
            nonsyn_kendalltau[k_zero] = z_coeff[1]
            nonsyn_pearson[k_zero] = z_coeff[2]

            nonsyn_spearman[k_comm] = c_coeff[0]
            nonsyn_kendalltau[k_comm] = c_coeff[1]
            nonsyn_pearson[k_comm] = c_coeff[2]

            z_coeff = 0
            c_coeff = 0

            # ALLBUTSYN
            f_allbutsyn_exp1 = path.join(path_exp1, file_allbutsyn)
            f_allbutsyn_exp2 = path.join(path_exp2, file_allbutsyn)

            z_coeff = zero.computeCorrelation(f_allbutsyn_exp1,
                                              f_allbutsyn_exp2)
            c_coeff = comm.computeCorrelation(f_allbutsyn_exp1,
                                              f_allbutsyn_exp2)

            # adding values to matrices as dictionary
            allbutsyn_spearman[k_zero] = z_coeff[0]
            allbutsyn_kendalltau[k_zero] = z_coeff[1]
            allbutsyn_pearson[k_zero] = z_coeff[2]

            allbutsyn_spearman[k_comm] = c_coeff[0]
            allbutsyn_kendalltau[k_comm] = c_coeff[1]
            allbutsyn_pearson[k_comm] = c_coeff[2]

            z_coeff = 0
            c_coeff = 0

    # printMatrix(allbutsyn_spearman)
    # printMatrix(allbutsyn_pearson)
    printMatrixToCSV(nonsyn_spearman, "nonsyn_spearman.csv")
    printMatrixToCSV(nonsyn_kendalltau, "nonsyn_kendalltau.csv")
    printMatrixToCSV(nonsyn_pearson, "nonsyn_pearson.csv")
    printMatrixToCSV(allbutsyn_spearman, "allbutsyn_spearman.csv")
    printMatrixToCSV(allbutsyn_kendalltau, "allbutsyn_kendalltau.csv")
    printMatrixToCSV(allbutsyn_pearson, "allbutsyn_pearson.csv")


def printMatrix(d):
    matrix = " "
    d_keys = set(map(lambda x: x[0], d.keys()))

    # header of the matrix
    matrix += " ".join(d_keys) + "\n"
    for i in d_keys:
        row = i
        for j in d_keys:
            row += " " + str(d.get((i, j), "/"))
        matrix += row + "\n"
    
    print(matrix)
    return matrix


def printMatrixToCSV(d, csv_file, sep=","):
    matrix = sep
    d_keys = set(map(lambda x: x[0], d.keys()))

    # header of the matrix
    matrix += sep.join(d_keys) + "\n"
    for i in d_keys:
        row = i
        for j in d_keys:
            row += sep + str(d.get((i, j), "/"))
        matrix += row + "\n"

    f = open(csv_file, 'w')
    f.write(matrix)
    f.close()

    return matrix


if __name__ == "__main__":
    computingCorrelationMatrices(sys.argv[1:])
