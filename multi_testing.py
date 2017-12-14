#!/usr/bin/python

import sys
from os.path import join, exists
from os import listdir, mkdir

import main_vcfnnvrprsr as vp


def test_1():
    l_args = []
    pop_frequency_list = [0.5, 1, 5]
    allele_freq = 5
    variant_depth = 5

    for f in pop_frequency_list:
        arg = ["<file_name>",
               "-t", "tumor",
               "-f", f,
               "--AD", variant_depth,
               "--AAFreq", allele_freq]
    l_args.append(arg)
    return l_args


def multi_testing(argv):
    # directiory of input data vcf or vcf.gz files
    input_data = argv[0]
    output_path = argv[1]

    args_list = test_1()

    for a in args_list:
        # creating an output folder with parameters names-values
        out_dir_name = "_".join(map(str, a[1:])).replace("-", "")
        out = join(output_path, out_dir_name)
        if not exists(out):
            mkdir(out)
        # adding to the parametr list the output folder
        a.append("--out")
        a.append(out)

        # for each vcf file in the data directory
        for vcf_file in listdir(input_data):
            # assigning as first parameter name of file to parse
            a[0] = vcf_file
            '''NOT WORKING how to pass parameters by code?'''
            vp.vcfnnvrprsr(a)


if __name__ == "__main__":
    multi_testing(sys.argv[1:])
