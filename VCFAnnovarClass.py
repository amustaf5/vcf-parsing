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
        self.tumor = ("tumor", 10)

        # mapping format ID elements to index
        self.read_depth = ("DP", 2)
        self.variant_depth = ("AD", 4)
        self.allele_freq = ("FREQ", 5)
        # quality filed to filter
        # self.quality = ("BQ", 3)
        self.quality = ("GQ", 1)  # luad

        # mapping info_ID elements to read
        self.gpv = "GPV"
        self.spv = "SPV"
        self.func = "Func.refGene"
        self.gene = "Gene.refGene"
        self.geneDetail = "GeneDetail.refGene"
        self.exonicFunc = "ExonicFunc.refGene"
        self.aaChange = "AAChange.refGene"

        # frequency fields
        self.all_sites = "ALL.sites.2015_08"
        self.gnomAD_genome_ALL = "gnomAD_genome_ALL"
        self.exAC_ALL = "ExAC_ALL"
        self.onet_genome = "1000g2015aug_all"

        # dictionary mapping current vcf annovar file info IDs to index
        self.dic_info = {}

        # index of the colon info (!!!Assuming 8th column)
        self.col_info_index = 7

        # info fields separator
        self.info_separator = ";"

        # null or absent value
        self.null = "."

        # header line of the output file
        self.header = "#CHROM\tPOS\tID\tREF\tALT\t" \
            + "GENE\tFUNC\tEXONIC_FUNC\tTRANSCRIPT\tMUTATION\t" \
            + "GgnomAD_genome_ALL\t1000g2015aug_all\tExAC_ALL\t" \
            + "GPV\tSPV\tALLELE_FREQ\n"

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
        elif tissue_type == self.tumor[0]:
            col = self.tumor[1]
        else:
            # TODO handle error
            print ("incorrect tissue type [normal | tumor]")

        ismutated = False
        selected_column_list = vcf_row[col].split(":")
        # !!!Assuming the Genotype GT is the first field
        genotype = selected_column_list[0]
        regex = "([1]\|[0])|([0](\||\/)[1])"  # matches 0/1, 1|0, 0|1

        if re.match(regex, genotype):
            ismutated = True

        # return also column values to process further
        return ismutated, selected_column_list

    def readInfoValue(self, info_id):
        '''reads the value of corresponding info id in current
        vcf row loaded in the dictionary
        '''
        res = self.dic_info[info_id]

        if info_id == self.aaChange:
            # get the list of the different changes (trascripts)
            transcript_l = re.findall("NM_[0-9]*", res)
            mutation_l = re.findall("p\.[A-Z0-9]*", res)
            # formatting a two column string with multiple values
            # separated by comma "," col transcript and col mutation
            res = ",".join(transcript_l) + "\t" + ",".join(mutation_l)

        return res

    def loadInfoDictionary(self, vcf_row):
        '''reads id and values from info column and creates a dictionary'''
        # clean dictionary each time
        self.dic_info = {}
        # list of info id=values
        info_l = vcf_row[self.col_info_index].split(self.info_separator)
        for field in info_l:
            key_val = field.split("=")
            # if there is a value
            # considering flag type field do not have a value (e.g. SOMATIC)
            if len(key_val) > 1:
                self.dic_info[key_val[0]] = key_val[1]

        return

    def readInfoId(self, vcf_line):
        '''reads the id value from the comment lines'''
        return vcf_line[len("##INFO=<ID="):].split(",")[0]

    def readInfoType(self, vcf_line):
        '''reads the Type of the value from the comment lines'''
        vcf_type = vcf_line[len("##INFO=<ID="):].split(",")[2]
        return vcf_type.split("=")[1]

    def checkFrequency(self, vcf_row, frequency_threshold):
        '''check if the mutation frequency is greater then
        the frequency value given in input
        vcf_row is an array of splitted vcf columns
        '''
        res = False

        # if not filtering take the line anyway
        if frequency_threshold == 0.0:
            res = True
        else:
            # create a list with the three frequncy value considered
            l_freq = []
            f1 = self.readInfoValue(self.gnomAD_genome_ALL)
            f2 = self.readInfoValue(self.onet_genome)
            f3 = self.readInfoValue(self.exAC_ALL)

            # check if there is a point (null value) or a value
            # convert all to float
            try:
                if f1 != self.null:
                    l_freq.append(float(f1))
                if f2 != self.null:
                    l_freq.append(float(f2))
                if f3 != self.null:
                    l_freq.append(float(f3))
            except ValueError:
                print ("error in file: %s") % self.name

            # get the max compare return ture or false
            # possibile to have all empty values
            if len(l_freq) != 0:
                if max(l_freq) < frequency_threshold:
                    res = True

        return res

    def checkGPV(self, vcf_row, gpv_threshold):
        '''check if the germline p-vale is smaller
        then a given threshold
        '''
        res = False
        if gpv_threshold == 0.0:
            res = True
        else:
            # reads the value of GPV from current line (vcf_row)
            gpv_ = self.readInfoValue(self.gpv)
            if gpv_ != self.null:
                if float(gpv_) < gpv_threshold:
                    res = True

        return res

    def checkSPV(self, vcf_row, spv_threshold):
        '''check if the somatic mutation p-vale is smaller
        then a given threshold
        '''
        res = False
        if spv_threshold == 0.0:
            res = True
        else:
            # reads the value of SPV from current line (vcf_row)
            spv_ = self.readInfoValue(self.spv)
            if spv_ != self.null:
                if float(spv_) < spv_threshold:
                    res = True

        return res

    def checkReadDepth(self, format_values, read_depth_arg):
        '''check if the read depth of the sample in the given
        column format_values (normal or tumor) is
        or equal then the given read_depth value
        '''
        res = False
        if read_depth_arg == 0:
            res = True
        else:
            read_depth_ = format_values[self.read_depth[1]]
            if read_depth_ != self.null:
                if int(read_depth_) >= read_depth_arg:
                    res = True

        return res

    def checkVariantDepth(self, format_values, variant_depth_arg):
        '''check if the variant depth of the sample in the given
        column format_values (normal or tumor) is greater
        or equal then the given variant_depth value
        '''
        res = False
        if variant_depth_arg == 0:
            res = True
        else:
            variant_depth_ = format_values[self.variant_depth[1]]
            if variant_depth_ != self.null:
                if int(variant_depth_) >= variant_depth_arg:
                    res = True

        return res

    def checkQuality(self, format_values, quality_threshold):
        '''check if the quality of the sample in the given
        column format_values (normal or tumor) is greater then
        the given quality_threshold
        '''
        res = False
        if quality_threshold == 0:
            res = True
        elif format_values[self.quality[1]].isdigit():
            bq = int(format_values[self.quality[1]])
            if bq > quality_threshold:
                res = True

        return res

    def checkAlleleFreq(self, format_values, allele_freq_threshold):
        '''check if the allele frequnecy of the sample in the given
        column format_values (normal or tumor) is greater then
        the given quality_threshold
        '''
        res = False
        if allele_freq_threshold == 0.0:
            res = True
        else:
            allele_freq_ = format_values[self.allele_freq[1]]
            if allele_freq_ != self.null:
                # converting the allele freq percent string to float
                # removing the '%' symbol
                if float(allele_freq_[:-1]) > allele_freq_threshold:
                    res = True

        return res

    def parsing(self, input_file, output_file, args):
        '''reads the vcf file line by line writing a custom ouput file
        according to the arguments args given
        (return only lines with >= base_quality)
        '''
        # print the pre-defined header to file see def in va class
        output_file.write(self.header)

        for line in input_file:
            # skip other comments and description lines
            if line.startswith('#'):
                continue
            else:
                columns = line.split()
                # check if there is a mutation according to
                # the chosen tissue type [normal|tumor]
                # returns a tuple (boolean, list of values)
                selection = self.mutated(args.tissue_type, columns)

                # if is mutated
                if selection[0]:
                    # values of the selected column
                    format_values = selection[1]

                    # read all the info id=value in self.dic_info
                    self.loadInfoDictionary(columns)

                    # TODO compute the index of base quality
                    # if bq greater then selected bq
                    if self.checkQuality(format_values, args.base_quality) \
                       and self.checkFrequency(columns,
                                               args.mutation_frequency) \
                       and self.checkGPV(columns, args.gpv_threshold) \
                       and self.checkSPV(columns, args.spv_threshold) \
                       and self.checkAlleleFreq(format_values,
                                                args.allele_freq_threshold) \
                       and self.checkReadDepth(format_values,
                                               args.read_depth_arg) \
                       and self.checkVariantDepth(format_values,
                                                  args.variant_depth_arg):

                        # read all the first 5 vcf standard field
                        new_line = columns[:5]
                        # read all the required info field
                        new_line.append(
                            self.readInfoValue(self.gene))
                        new_line.append(
                            self.readInfoValue(self.func))
                        new_line.append(
                            self.readInfoValue(self.exonicFunc))
                        new_line.append(
                            self.readInfoValue(self.aaChange))
                        new_line.append(
                            self.readInfoValue(self.gnomAD_genome_ALL))
                        new_line.append(
                            self.readInfoValue(self.onet_genome))
                        new_line.append(
                            self.readInfoValue(self.exAC_ALL))
                        # non-annovar vcf info fields
                        new_line.append(
                            self.readInfoValue(self.gpv))
                        new_line.append(
                            self.readInfoValue(self.spv))
                        # vcf format field
                        new_line.append(format_values[self.allele_freq[1]])

                        # !!!TEMP TESTING (not showing in output file)
                        # new_line.append(format_values[self.read_depth[1]])
                        # new_line.append(format_values[self.variant_depth[1]])

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
