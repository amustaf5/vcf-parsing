#!/usr/bin/python

import sys
from os import path
import ranking_zero as zero
import ranking_common_genes as comm


def computingCorrelationMatrices(args):
    '''takes in input two file containing paths each experiment file
    to compare computing three different correlation coefficents
    returns a matrix in csv format composed by two columns
    one computed adding zeros the other considering only common genes
    in order to have comparable series of numbers (same dimension)
    '''

    list_file_exp1 = list(map(lambda t: t.strip(), open(args[0], 'r').readlines()))
    list_file_exp2 = list(map(lambda t: t.strip(), open(args[1], 'r').readlines()))
    index = int(args[2])

    # chek if the two experiment file list are same in length
    n_experiments = len(list_file_exp1)

    table = {}

    for i in range(n_experiments):
        path_exp1 = path.normpath(list_file_exp1[i])
        path_exp2 = path.normpath(list_file_exp2[i])

        key_i = "_".join(path.dirname(path_exp1).split("/")[-2:])

        # computing the correlation coefficent
        # considering only common genes and adding zero values
        # in order to have same array size
        z_coeff = zero.computeCorrelation(path_exp1, path_exp2, index)
        c_coeff = comm.computeCorrelation(path_exp1, path_exp2, index)

        table[key_i] = (z_coeff, c_coeff)

    out_fn = "cc_"
    out_fn += "_".join(list_file_exp1[0].split("/")[-2:]).split(".")[0] + ".csv"
    printMatrixToCSV(table, out_fn)


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
    matrix = "#EXP,SPEARMAN ZERO,SPEARMAN COMMON," \
        + "KENDALLTAU ZERO,KENDALLTAU COMMON," \
        + "PEARSON ZERO,PEARSON COMMON\n"

    for i in d.keys():
        c = d[i]
        matrix += sep.join([i,
                           str(c[0][0]),
                           str(c[1][0]),
                           str(c[0][1]),
                           str(c[1][1]),
                           str(c[0][2]),
                           str(c[1][2])])
        matrix += "\n"

    f = open(csv_file, 'w')
    f.write(matrix)
    f.close()

    return matrix


if __name__ == "__main__":
    computingCorrelationMatrices(sys.argv[1:])
