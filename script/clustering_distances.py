#!/usr/bin/python

import argparse
import sys


def create_dic(filename):
    '''create a dictionary using the first
    column value as key and other columns as values
    '''
    d = {}
    lines = open(filename, 'r').readlines()

    for line in lines:
        e = line.split()
        d[e[0]] = e[1:]

    return d


def computeJaccardIndex(file_one, file_two):
    '''
    compute the Jaccard index of the two set of genes (keys) given in input
    as files
    '''
    d_one = {}
    d_two = {}

    d_one = create_dic(file_one)
    d_two = create_dic(file_two)

    index = 0.0

    # if both sets are empty the index is 1
    if len(d_one) == 0 and len(d_two) == 0:
        index = 1

    else:
        # compute the intersection of the keys of the two dictionaryes
        keys_intersect = set(d_one.keys()).intersection(d_two.keys())

        # compute the union of the keys of the two dictionaryes
        keys_union = set(d_one.keys()).union(d_two.keys())

        # compute the jaccard index
        index = float(len(keys_intersect))/float(len(keys_union))

        # print for debugging reason
        # print "jaccard index= ", index, "n_intersection= ", len(keys_intersect), "n_union= ", len(keys_union)

    return index


def distance(index):
    '''
    distance function computing a distance
    '''
    return 1-index


def clustering(argv):
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
    parser.add_argument('--distance',
                        action='store_true',
                        help='print the distance based on jaccard index')

    args = parser.parse_args()

    jacind = computeJaccardIndex(args.file_one, args.file_two)
    if args.distance:
        print distance(jacind)
    else:
        print jacind


if __name__ == "__main__":
    clustering(sys.argv[1:])
