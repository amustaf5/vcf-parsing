import argparse
import sys
import scipy.stats as stats


def computeKS(argv):
    ''' computing Kolmogorov-Smirnov test
    between two given distributions
    '''
    parser = argparse.ArgumentParser(usage='%(prog)s [options] arg1 arg2',
                                     description='Process vcf files.')
    parser.add_argument('data1',
                        type=str,
                        help='list of float value from distibution 1')
    parser.add_argument('data2',
                        type=str,
                        help='list of float value from distibution 2')
    args = parser.parse_args()

    data1_ = list(map(lambda t: float(t.strip()), open(args.data1, 'r')
                      .readlines()))
    data2_ = list(map(lambda t: float(t.strip()), open(args.data2, 'r')
                      .readlines()))

    KSstat_pvalue = stats.ks_2samp(data1_, data2_)

    print(KSstat_pvalue)

    return KSstat_pvalue


if __name__ == "__main__":
    computeKS(sys.argv[1:])
