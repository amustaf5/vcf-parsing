import argparse
import sys
import gzip

import VCFAnnovarClass


def main(argv):
    parser = argparse.ArgumentParser(usage='%(prog)s [options] arg1 arg2',
                                     description='Process vcf files.')
    parser.add_argument('vcf_file',
                        type=str,
                        help='vcf input file')
    parser.add_argument('-t',
                        '--type',
                        type=str,
                        dest='tissue_type',
                        action='store',
                        default="normal",
                        help='selct type of tissue [normal|primary]')
    parser.add_argument('-q',
                        '--base_quality',
                        type=int,
                        dest='base_quality',
                        action='store',
                        default=0,
                        help='filter base quality [int]')

    args = parser.parse_args()

    # initiate the VCFAnnovar class object
    va = VCFAnnovarClass.VCFAnnovar(args.vcf_file)

    # create a output file name
    suffix = "_%s_bq%d.out" % (args.tissue_type, args.base_quality)
    outfname = args.vcf_file.split(".vcf")[0] + suffix

    if args.vcf_file.endswith(".gz"):
        with gzip.open(args.vcf_file, 'rb') as f:
            with gzip.open(outfname + ".gz", 'wb') as of:
                va.parsing(f, of, args)

    elif args.vcf_file.endswith(".vcf"):
        with open(args.vcf_file, 'r') as f:
            with open(outfname, 'w') as of:
                va.parsing(f, of, args)
    else:
        print ("unknown file format")


if __name__ == "__main__":
    main(sys.argv[1:])
