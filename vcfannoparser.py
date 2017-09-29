import argparse
import sys
import os

import myvcflib

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
    parser.add_argument('-t', '--type', type=str, dest='tissue_type', action='store', default="normal", help='selct type of tissue [normal|primary]')
    parser.add_argument('-q', '--base_quality', type=int, dest='base_quality', action='store', default=0, help='filter base quality [int]')
   
    args = parser.parse_args()
    #print 'base quality: %d', args.base_quality

    #create a output file name
    suffix = "_%s_bq%d.out" % (args.tissue_type, args.base_quality)
    outfname = args.vcf_file.split(".vcf")[0] + suffix

    #open the vcf file
    #read line by line
    #return only lines with >= base_quality 
    bq = 0
    with open(args.vcf_file, 'r') as f:
        with open(outfname, 'w') as of:
            of.write("#CHROM\tPOS\tID\tREF\tALT\tGENE\tFUNC\tEXONIC_FUNC\tAA_CHANGE\n")

            for line in f:
                #skip comment and description lines
                if line.startswith('#'):
                    continue
                else:
                    columns = line.split()
                    #check if there is a mutation according to the chosen tissue type [normal|primary]
                    selection = myvcflib.mutated(args.tissue_type, columns) #returns a tuple (boolean, list of values)
                                        
                    #if is mutated
                    if selection[0]:
                        #values of the selected column
                        values = selection[1]

                        #if base quality, 4th value in the column
                        #TODO compute the index of base quality
                        if values[3].isdigit():
                            bq = int(values[3])

                            if bq > args.base_quality:
                                gene = myvcflib.readGene(columns)
                                func = myvcflib.readInfo(columns, 3)
                                exonicf = myvcflib.readInfo(columns, 6)
                                aachange = myvcflib.readInfo(columns, 7)

                                new_line = columns[:5]
                                new_line.append(gene)
                                new_line.append(func)
                                new_line.append(exonicf)
                                new_line.append(aachange)

                                myvcflib.writeToFile(of, new_line)
                                #of.write(line)
            f.close()
            of.close()
            
if __name__=="__main__":
    main(sys.argv[1:])

