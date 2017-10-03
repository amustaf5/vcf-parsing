import argparse
import sys

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

    # open the vcf file
    # read line by line
    # return only lines with >= base_quality
    bq = 0
    flag_info = False
    info_count = 0

    with open(args.vcf_file, 'r') as f:
        with open(outfname, 'w') as of:
            # print the pre-defined header to file see def in va class
            of.write(va.header)

            for line in f:
                # find the vcf info field
                if line.startswith(va.start_info):
                    # counting the info fields
                    info_count += 1

                if line.startswith(va.start_annovar_info):
                    flag_info = True
                    continue

                if line.startswith(va.end_info):
                    flag_info = False
                    continue

                if flag_info:
                    # read the info id and write in dic_info_id
                    # computing info index = info_count-1
                    va.dic_info_id[va.readInfoId(line)] = info_count-1
                    continue

                # skip other comments and description lines
                if line.startswith('#'):
                    continue
                else:
                    columns = line.split()
                    # check if there is a mutation according to
                    # the chosen tissue type [normal|primary]
                    # returns a tuple (boolean, list of values)
                    selection = va.mutated(args.tissue_type, columns)

                    # if is mutated
                    if selection[0]:
                        # values of the selected column
                        values = selection[1]

                        # if base quality, 4th value in the column
                        # TODO compute the index of base quality
                        if values[3].isdigit():
                            bq = int(values[3])

                            # if bq greater then selected bq
                            if bq > args.base_quality:
                                # read all the first 5 vcf standard field
                                new_line = columns[:5]
                                # read all the required info field
                                new_line.append(
                                    va.readInfoValue(columns, va.gene))
                                new_line.append(
                                    va.readInfoValue(columns, va.func))
                                new_line.append(
                                    va.readInfoValue(columns, va.exonicFunc))
                                new_line.append(
                                    va.readInfoValue(columns, va.aaChange))

                                va.writeToFile(of, new_line)
                                # of.write(line)
            f.close()
            of.close()


if __name__ == "__main__":
    main(sys.argv[1:])
