import argparse
import sys
import gzip
from os import mkdir
from os.path import join, isdir
from multiprocessing import Pool

import VCFAnnovarClass


def vcfnnvrprsr(argv):
    parser = argparse.ArgumentParser(usage='%(prog)s [options] arg1 arg2',
                                     description='Process vcf files.')
    parser.add_argument('vcf_file',
                        type=str,
                        help='file containing a list of paths of vcf input chromosomes file')
    parser.add_argument('-f',
                        '--pop_frequency',
                        type=float,
                        dest='pop_frequency',
                        action='store',
                        default=0.0,
                        help='filter population frequency [float]')
    parser.add_argument('--out',
                        type=str,
                        dest='out_dir',
                        action='store',
                        default='.',
                        help='path of the output folder')

    args = parser.parse_args()

    # initiate the VCFAnnovar class object
    va = VCFAnnovarClass.VCFAnnovar()

    # takes in input a list of path of vcf chr file
    # split in two part
    chr_file_list = open(args.vcf_file, 'r').readlines()

    pt1_dir = join(args.out_dir, "pt1")
    pt2_dir = join(args.out_dir, "pt2")

    # create two folder in out_dir
    if not isdir(pt1_dir):
        mkdir(pt1_dir)
    if not isdir(pt2_dir):
        mkdir(pt2_dir)

    # parallelize
    TASKS = \
        [(execparsing, (va,
                        chr_file_list[:len(chr_file_list)/2],
                        pt1_dir,
                        args.pop_frequency)),
         (execparsing, (va,
                        chr_file_list[len(chr_file_list)/2:],
                        pt2_dir,
                        args.pop_frequency))]

    pool = Pool(processes=2)
    pool.map(calculatestar, TASKS)


def calculate(func, args):
    result = func(*args)


def calculatestar(args):
    return calculate(*args)


def execparsing(va, vcf_file_list, out_dir, pop_frequency):
    for f in vcf_file_list:
        vcf_file = f.strip()
        if vcf_file.endswith(".gz"):
            with gzip.open(vcf_file, 'rb') as f:
                va.parsingChr(f, out_dir, pop_frequency)

        elif vcf_file.endswith(".vcf"):
            with open(vcf_file, 'r') as f:
                va.parsingChr(f, out_dir, pop_frequency)
        else:
            print ("unknown file format")


if __name__ == "__main__":
    vcfnnvrprsr(sys.argv[1:])
