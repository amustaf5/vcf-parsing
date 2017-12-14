#!/usr/bin/python

import sys
import os


def build_table(args):
    '''takes input a list of folders of each experiment containing
    the tree files of the GT counting for each mutation type
    germline somatic and their union
    '''

    header = "PF\tAD\tAF\t0/0-0/1\t0/1-0/1\t0/1-1/1\t1/1-0/1"

    table_germ = header + "\n"
    table_soma = header + "\n"
    table_unio = header + "\n"

    for i in range(len(args)):
        row = ""
        path = args[i][:-1].split("/")
        param = path[len(path)-1].split("_")
        row = "\t".join(param) + "\t5%\t"

        f_germ = os.path.join(args[i], "germline_GT_count.txt")
        f_soma = os.path.join(args[i], "somatic_GT_count.txt")
        f_unio = os.path.join(args[i], "union_GT_count.txt")

        row_g = row
        for line in open(f_germ, 'r'):
            row_g += line.strip().split()[0] + "\t"
        table_germ += row_g + "\n"

        row_s = row
        for line in open(f_soma, 'r'):
            row_s += line.strip().split()[0] + "\t"
        table_soma += row_g + "\n"

        row_u = row
        for line in open(f_unio, 'r'):
            row_u += line.strip().split()[0] + "\t"
        table_unio += row_u + "\n"

    tables = "==> germline\n" + table_germ \
        + "\n==> somatic\n" + table_soma \
        + "\n==> union\n" + table_unio
    open("gt_table.txt", 'w').writelines(tables)


if __name__ == "__main__":
    build_table(sys.argv[1:])
