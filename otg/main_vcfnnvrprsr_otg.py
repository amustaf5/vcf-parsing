import argparse
import sys
import gzip
from os.path import basename, join

import VCFAnnovarClass


def vcfnnvrprsr(argv):
    parser = argparse.ArgumentParser(usage='%(prog)s [options] arg1 arg2',
                                     description='Process vcf files.')
    parser.add_argument('vcf_file',
                        type=str,
                        help='vcf input file')
    parser.add_argument('-f',
                        '--pop_frequency',
                        type=float,
                        dest='pop_frequency',
                        action='store',
                        default=0.0,
                        help='filter population frequency [float]')
    parser.add_argument('--append',
                        action='store_true',
                        help='append to the existing output file')
    parser.add_argument('--out',
                        type=str,
                        dest='out_dir',
                        action='store',
                        default='.',
                        help='path of the output folder')

    args = parser.parse_args()

    # initiate the VCFAnnovar class object
    va = VCFAnnovarClass.VCFAnnovar(args.vcf_file)

    suffix = ".out"
    outfname = join(args.out_dir, basename(args.vcf_file).split(".")[0] + suffix)

    if args.vcf_file.endswith(".gz"):
        with gzip.open(args.vcf_file, 'rb') as f:
            if args.out_dir == "STD":
                va.parsingSTD(f, args)
            elif args.append:
                with gzip.open(outfname + ".gz", 'ab') as of:
                    va.parsing(f, of, args)
            else:
                with gzip.open(outfname + ".gz", 'wb') as of:
                    va.parsing(f, of, args)

    elif args.vcf_file.endswith(".vcf"):
        with open(args.vcf_file, 'r') as f:
            if args.out_dir == "STD":
                va.parsingSTD(f, args)
            elif args.append:
                with open(outfname, 'a') as of:
                    va.parsing(f, of, args)
            else:
                with open(outfname, 'w') as of:
                    va.parsing(f, of, args)
    else:
        print ("unknown file format")


if __name__ == "__main__":
    vcfnnvrprsr(sys.argv[1:])
