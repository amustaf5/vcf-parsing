import argparse
import sys
import os

#    parser = optparse.OptionParser("usage: %prog [options] arg1 arg2")
#    parser.add_option("-H", "--host", dest="hostname",
#                      default="127.0.0.1", type="string",
#                      help="specify hostname to run on")
#    parser.add_option("-p", "--port", dest="portnum", default=80,
#                      type="int", help="port number to run on")
#
#    (options, args) = parser.parse_args()
#    if len(args) != 2:
#        parser.error("incorrect number of arguments")
#    hostname = options.hostname
#    portnum = options.portnum
    

def main(argv):
    parser = argparse.ArgumentParser(usage='%(prog)s [options] arg1 arg2', description='Process vcf files.')
    parser.add_argument('vcf_file', type=str, help='vcf input file')
    parser.add_argument('-q', '--base_quality', type=int, dest='base_quality', action='store', default=0, help='filter base quality')
    
    args = parser.parse_args()
    print 'base quality: %d', args.base_quality

    #open the vcf file
    #read line by line
    #return only lines with >= base_quality 
    bq = 0
    with open(args.vcf_file, 'r') as f:
        with open(args.vcf_file + '_out', 'w') as of:

            for line in f:
                if line.startswith('#'):
                    continue
                else:
                    columns = line.split()
                    #taking temporary the 10th column = normal tissue
                    #values of the normal column
                    values = columns[9].split(':')

                    #if base quality, 4th value in the column
                    if values[3].isdigit():
                        bq = int(values[3])

                        if bq > args.base_quality:
                            of.write(line)
            f.close()
            of.close()
            
if __name__=="__main__":
    main(sys.argv[1:])

