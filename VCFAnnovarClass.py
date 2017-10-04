import re


class VCFAnnovar(object):
    def __init__(self, name=""):
        self.name = name

        # start tag for the vcf info field
        self.start_info = "##INFO"

        # start-end tag for the info field annovar vcf file
        self.start_annovar_info = "##INFO=<ID=ANNOVAR_DATE,"
        self.end_info = "##INFO=<ID=ALLELE_END,"

        # mapping column to tissue_type selection
        self.normal = ("normal", 9)
        self.primary = ("primary", 10)

        # frequency field to filter (!!!different for each annotation)
        self.frequency_id = ("ALL.sites.2015_08")
        # self.frequency_id = ("ExAC_ALL") # luad

        # quality filed to filter
        self.quality = ("BQ", 3)
        # self.quality = ("GQ", 1) # luad

        # mapping info_ID elements to read
        self.func = "Func.refGene"
        self.gene = "Gene.refGene"
        self.geneDetail = "GeneDetail.refGene"
        self.exonicFunc = "ExonicFunc.refGene"
        self.aaChange = "AAChange.refGene"
        self.all_sites = "ALL.sites.2015_08"

        # dictionary mapping current vcf annovar file info IDs to index
        self.dic_info_id = {}

        # index of the colon info (!!!Assuming 8th column)
        self.col_info_index = 7

        # info fields separator
        self.info_separator = ";"

        # header line of the output file
        self.header = "#CHROM\tPOS\tID\tREF\tALT\t" \
            + "GENE\tFUNC\tEXONIC_FUNC\tAA_CHANGE\n"

    def startInfo(self, vcf_line):
        '''startInfo(self, vcf_line)
        check if the current line starts with annovar info start tag
        '''
        return vcf_line.startswith(self.start_info)

    def endInfo(self, vcf_line):
        '''check if the current line starts with annovar info end tag'''
        return vcf_line.startswith(self.end_info)

    def mutated(self, tissue_type, vcf_row):
        '''check if the current line (vcf_row) has a mutation..
        according to the selected tissue_type
        '''
        col = 0
        if tissue_type == self.normal[0]:
            col = self.normal[1]
        elif tissue_type == self.primary[0]:
            col = self.primary[1]
        else:
            # TODO handle error
            print ("incorrect tissue type [normal | primary]")

        ismutated = False
        selected_column_list = vcf_row[col].split(":")
        # !!!Assuming the Genotype GT is the first field
        genotype = selected_column_list[0]
        regex = "([1]\|[0])|([0](\||\/)[1])"  # matches 0/1, 1|0, 0|1

        if re.match(regex, genotype):
            ismutated = True

        # return also column values to process further
        return ismutated, selected_column_list

    def readInfoValue(self, vcf_row, info_id):
        '''reads the value of corresponding info id in current vcf row
        wich is an array of values(columns)
        '''
        val = vcf_row[self.col_info_index] \
            .split(self.info_separator)[self.dic_info_id[info_id]] \
            .split("=")[1]
        return val

    def readInfoId(self, vcf_line):
        '''reads the id value from the comment lines'''
        return vcf_line[len("##INFO=<ID="):].split(",")[0]

    def parsing(self, input_file, output_file, args):
        '''reads the vcf file line by line writing a custom ouput file
        according to the arguments args given
        (return only lines with >= base_quality)
        '''
        bq = 0
        flag_info = False
        info_count = 0

        # print the pre-defined header to file see def in va class
        output_file.write(self.header)

        for line in input_file:
            # find the vcf info field
            if line.startswith(self.start_info):
                # counting the info fields
                info_count += 1

            if line.startswith(self.start_annovar_info):
                flag_info = True
                continue

            if line.startswith(self.end_info):
                flag_info = False
                continue

            if flag_info:
                # read the info id and write in dic_info_id
                # computing info index = info_count-1
                self.dic_info_id[self.readInfoId(line)] = info_count-1
                continue

            # skip other comments and description lines
            if line.startswith('#'):
                continue
            else:
                columns = line.split()
                # check if there is a mutation according to
                # the chosen tissue type [normal|primary]
                # returns a tuple (boolean, list of values)
                selection = self.mutated(args.tissue_type, columns)

                # if is mutated
                if selection[0]:
                    # values of the selected column
                    values = selection[1]

                    # frequency filtering read value
                    freq = 0
                    try:
                        freq = float(self.readInfoValue(columns,
                                                        self.frequency_id))
                    except ValueError:
                        # assuming value zero for null values "."
                        freq = 0.0

                    # if base quality, 4th value in the column
                    # TODO compute the index of base quality
                    if values[self.quality[1]].isdigit():
                        bq = int(values[self.quality[1]])

                        # if bq greater then selected bq
                        if bq > args.base_quality \
                           and freq > args.mutation_frequency:

                            # read all the first 5 vcf standard field
                            new_line = columns[:5]
                            # read all the required info field
                            new_line.append(
                                self.readInfoValue(columns, self.gene))
                            new_line.append(
                                self.readInfoValue(columns, self.func))
                            new_line.append(
                                self.readInfoValue(columns, self.exonicFunc))
                            new_line.append(
                                self.readInfoValue(columns, self.aaChange))

                            self.writeToFile(output_file, new_line)
                            # of.write(line)
        input_file.close()
        output_file.close()

    def readGene(self, vcf_row):
        '''reads the Gene field in the annovar annotation field'''
        info = vcf_row[7].split(";")[4].split("=")[1]
        return info

    def readFunc(self, vcf_row):
        '''reads the Function field in the annovar annotation field'''
        info = vcf_row[7].split(";")[3].split("=")[1]
        return info

    def readInfo(self, vcf_row, index):
        '''reads the Info field in the annovar annotation field'''
        info = vcf_row[7].split(";")[index].split("=")[1]
        return info

    def writeToFile(self, out_file, vcf_cols):
        line = ""
        for c in vcf_cols:
            line += c + "\t"

        out_file.write(line+"\n")
