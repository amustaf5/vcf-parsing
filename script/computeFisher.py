import argparse
import sys
import scipy.stats as stats
import numpy as np
from os.path import basename, join


def computeFisher(argv):
    ''' computing one-tailed (=greater) fisher test
    in order to give significance to
    only large numbers (significant mutations)
    '''
    parser = argparse.ArgumentParser(usage='%(prog)s [options] arg1 arg2',
                                     description='Process vcf files.')
    parser.add_argument('gene_count_file',
                        type=str,
                        help='gene counting file with five columns: \
                        GENE_NAME | NORMAL | NORMAL NON-MUT | TUMOR | TUMOR NON-MUT')
    parser.add_argument('--cohort_size',
                        type=int,
                        dest='cohort_size',
                        action='store',
                        default=2504,
                        help='total number of the individuals in the cohort')
    parser.add_argument('--std',
                        action='store_true',
                        help='print to the standard output')
    parser.add_argument('--out',
                        type=str,
                        dest='out_dir',
                        action='store',
                        default='.',
                        help='path of the output folder')

    args = parser.parse_args()

    suffix = "_fsh.txt"
    outfname = join(args.out_dir,
                    basename(args.gene_count_file).split(".")[0] + suffix)

    with open(args.gene_count_file, 'r') as f:
        if args.std:
            # printing to the standard output
            for line in f:
                columns = map(int, line.split()[1:])
                # contingency table
                # [[mut normal, mut tumor], [non-mut normal, non-mut tumor]]
                ctable = [[columns[2] + 1, columns[0] + 1],
                          [columns[3] + 1, columns[1] + 1]]
                oddsratio, pvalue = stats.fisher_exact(ctable,
                                                       alternative='greater')
                print('{:s}\t{:f}\t{:f}'
                      .format(line.strip(),
                              oddsratio,
                              -1*np.log(pvalue)/np.log(10)))

                # try:
                # print('{:s}\t{:d}\t{:d}\t{:d}\t{:d}\t{:f}\t{:f}'
                #      .format(line.split()[0],
                #              ctable[0][0]-1,
                #              ctable[0][1]-1,
                #              ctable[1][0]-1,
                #              ctable[1][1]-1,
                #              oddsratio,
                #              -1*np.log(pvalue)/np.log(10)))
                # except:
                #    print >> sys.stdr, line

        else:
            # printing to ouput file
            of = open(outfname, 'w')
            for line in f:
                columns = map(int, line.split()[1:])
                # contingency table
                # [[mut tumor, mut normal], [non-mut tumor, non-mut normal]]
                ctable = [[columns[0] + 1, columns[1] + 1],
                          [args.cohort_size - columns[0] + 1,
                           args.cohort_size - columns[1] + 1]]
                oddsratio, pvalue = stats.fisher_exact(ctable,
                                                       alternative='greater')

                of.write('{:s}\t{:.4e}\t{:.4e}\n'
                         .format(line.strip(),
                                 oddsratio,
                                 pvalue))

            f.close()
            of.close()


if __name__ == "__main__":
    computeFisher(sys.argv[1:])
