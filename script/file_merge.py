#!/usr/bin/python

import argparse
import sys


def create_dic_zero(filename):
    '''create a dictionary using the first
    column value as key and other columns as values
    '''
    d = {}
    lines = open(filename, 'r').readlines()
    n = len(lines[0].split())
    for line in lines:
        e = line.split()
        if len(e) != n:
            print >> sys.stderr, "WARNING: wrong number of columns", line
            continue
        d[e[0]] = e[1:]
    return d, n-1


def create_dic(filename, keys_index):
    '''create a dictionary using as key a combination
    of given columns and as value a range of cols
    or all the columns that are not the key
    '''
    d = {}
    lines = open(filename, 'r').readlines()
    n = len(lines[0].split())
    for line in lines:
        e = line.split()
        if len(e) != n:
            print >> sys.stderr, "WARNING: wrong number of columns", line
            continue
        keys_cols_list = list(map(lambda i: int(i)-1, keys_index.split(",")))
        k = "_".join(list(map(lambda t: e[t], keys_cols_list)))
        # taking as value only columns that are not also keys
        v = list(map(lambda j: e[j], set(range(len(e))).difference(keys_cols_list)))
        d[k] = v
    return d, n-len(keys_cols_list)


def genes_union(file_one, file_two, keys_one, keys_two, sep="\t"):
    '''
    modificare script per intersection renderlo piu generico
    takes input two files containing two columns one
    list of genes whith germline mutation or list of genes
    with somatic mutation plus a counting column
    '''

    f_mutgenes_germline = file_one
    f_mutgenes_somatic = file_two

    d_germ = {}
    d_soma = {}
    d_union = {}

    if keys_one == "0" and keys_two == "0":
        d_germ, n_germ = create_dic_zero(f_mutgenes_germline)
        d_soma, n_soma = create_dic_zero(f_mutgenes_somatic)
    else:
        d_germ, n_germ = create_dic(f_mutgenes_germline, keys_one)
        d_soma, n_soma = create_dic(f_mutgenes_somatic, keys_two)

    # compute the union of the keys of the two dictionaryes
    keys_union = set(d_germ.keys()).union(d_soma.keys())

    # for each keys create enty in d_union with sum of
    # the values of germline and somatic genes if present
    # else assign zero
    for k in keys_union:
        # d_union[k] = d_germ.get(k, 0) + d_soma.get(k, 0)
        l1 = d_germ.get(k, [])
        if len(l1) != n_germ:
            l1 = n_germ * [0]

        l2 = d_soma.get(k, [])
        if len(l2) != n_soma:
            l2 = n_soma * [0]

        # print k, " ".join((str[j] for j in l1)), " ".join((str[j] for j in l2))
        print(k.replace("_", sep),
              sep.join(list(map(str, l1))), sep.join(list(map(str, l2))))

    return d_union


def intersect(file_one, file_two, keys_one, keys_two, sep="\t"):
    '''
    takes input two files containing N columns tab separated
    gives output one file resulting by the intersection
    of the commmon keys of the two files
    '''

    d_one = {}
    d_two = {}
    d_intersect = {}

    n_one = 0
    n_two = 0

    if keys_one == "0" and keys_two == "0":
        d_one, n_one = create_dic_zero(file_one)
        d_two, n_two = create_dic_zero(file_two)
    else:
        d_one, n_one = create_dic(file_one, keys_one)
        d_two, n_two = create_dic(file_two, keys_two)

    # compute the intersect of the keys of the two dictionaryes
    keys_intersect = set(d_one.keys()).intersection(d_two.keys())

    # for each keys create enty in d_intersect
    for k in keys_intersect:
        l1 = d_one.get(k, [])
        if len(l1) != n_one:
            l1 = n_one * [0]

        l2 = d_two.get(k, [])
        if len(l2) != n_two:
            l2 = n_two * [0]

        print(k.replace("_", sep),
              sep.join(list(map(str, l1))), sep.join(list(map(str, l2))))

    return d_intersect


def file_merge(argv):
    '''takes input two files containing n columns
    a comma separated string of key cols file1 and 2
    '''
    parser = argparse.ArgumentParser(usage='%(prog)s [options] arg1 arg2',
                                     description='files union or intersect')
    parser.add_argument('file_one',
                        type=str,
                        help='first input file')
    parser.add_argument('file_two',
                        type=str,
                        help='secont input file')
    parser.add_argument('-k1',
                        '--keys_one',
                        type=str,
                        dest='keys_one',
                        action='store',
                        default="0",
                        help=('list of cols index starting from 1'
                              'as keys comma separated'))
    parser.add_argument('-k2',
                        '--keys_two',
                        type=str,
                        dest='keys_two',
                        action='store',
                        default="0",
                        help=('list of cols index starting from 1'
                              'as keys comma separated'))
    parser.add_argument('-i',
                        '--intersect',
                        action='store_true',
                        help='append to the existing output file')
    parser.add_argument('-u',
                        '--union',
                        action='store_true',
                        help='append to the existing output file')

    args = parser.parse_args()

    if args.union:
        genes_union(args.file_one, args.file_two, args.keys_one, args.keys_two)

    if args.intersect:
        intersect(args.file_one, args.file_two, args.keys_one, args.keys_two)


if __name__ == "__main__":
    file_merge(sys.argv[1:])
