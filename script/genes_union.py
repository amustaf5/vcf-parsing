#!/usr/bin/python

import sys

def create_dic(filename):
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


def genes_union(args):
    '''
    modificare script per intersection renderlo piu generico
    takes input two files containing two columns one
    list of genes whith germline mutation or list of genes
    with somatic mutation plus a counting column
    '''
    sep = "\t"
    f_mutgenes_germline = args[0]
    f_mutgenes_somatic = args[1]

    d_germ = {}
    d_soma = {}
    d_union = {}
 
    d_germ, n_germ = create_dic(f_mutgenes_germline)
    d_soma, n_soma = create_dic(f_mutgenes_somatic)

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
        
        
        #print k, " ".join((str[j] for j in l1)), " ".join((str[j] for j in l2))
        print k, sep.join(list(map(str, l1))), sep.join(list(map(str, l2))) 

    return d_union


if __name__ == "__main__":
    genes_union(sys.argv[1:])
