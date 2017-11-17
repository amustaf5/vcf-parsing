import re


class VCFAnnovar(object):
    '''class based on onethousand genomes database annovar files'''
    def __init__(self, name=""):
        self.name = name

        # start tag for the vcf info field
        self.start_info = "##INFO"

        # start-end tag for the info field annovar vcf file
        self.start_annovar_info = "##INFO=<ID=ANNOVAR_DATE,"
        self.end_info = "##INFO=<ID=ALLELE_END,"

        # mapping info_ID elements to read
        self.func = "Func.refGene"
        self.gene = "Gene.refGene"
        self.geneDetail = "GeneDetail.refGene"
        self.exonicFunc = "ExonicFunc.refGene"
        self.aaChange = "AAChange.refGene"

        # population frequency fields
        self.gnomAD_genome_ALL = "gnomAD_genome_ALL"
        self.exAC_ALL = "ExAC_ALL"
        self.onet_genome = "1000g2015aug_all"

        # dictionary mapping current vcf annovar file info IDs to index
        self.dic_info = {}

        # index of the colon info (!!!Assuming 8th column)
        self.col_info_index = 7

        # index of the genotype value
        self.col_GT_index = 9

        # info fields separator
        self.info_separator = ";"

        # null or absent value
        self.null = "."

        # output columns separator
        self.col_sep = "\t"  # 4*" "

        # header line of the output file
        self.header = "#CHROM\tPOS\tID\tREF\tALT\t" \
            + "GENE\tFUNC\tEXONIC_FUNC\tTRANSCRIPT\tMUTATION\t" \
            + "GgnomAD_genome_ALL\t1000g2015aug_all\tExAC_ALL\n"

    def readInfoValue(self, info_id, info_index):
        '''reads the value of corresponding info id in current
        vcf row loaded in the dictionary for the corresponding
        mutation (info_index)
        '''
        res = self.dic_info[info_id][info_index]

        # handle the specific case of AAChange field to be splitted in
        # transcript and mutation columns
        if info_id == self.aaChange:
            if res != self.null:
                # get the list of the different changes (trascripts)
                transcript_l = re.findall("NM_[0-9]*", res)
                mutation_l = re.findall("p\.[A-Z0-9]*", res)
                # formatting a two column string with multiple values
                # separated by comma "," col transcript and col mutation
                tmp = ",".join(transcript_l) \
                    + self.col_sep \
                    + ",".join(mutation_l)

                if len(transcript_l) > 0 and len(mutation_l) > 0:
                    res = tmp
                # there is also possibile to have a transcript
                # but not a mutation and viceversa
                elif len(transcript_l) == 0 and len(mutation_l) > 0:
                    res = "not_found" + tmp
                elif len(transcript_l) > 0 and len(mutation_l) == 0:
                    res = tmp + "not_found"
                # checking if the resulting string is empty or better
                # equal to the col separator due to unexpected
                # string values or format as "UNKNOWN" string
                # NB: join of empty list returns empty string
                # elif tmp == self.col_sep:
                else:
                    res = res + self.col_sep + res
            else:
                res = self.null + self.col_sep + self.null

        return res

    def loadInfoDictionary(self, vcf_row):
        '''reads id and values from info column and creates a dictionary
        with a list of value for each key corresponding to each
        annovar date field
        '''
        # clean dictionary each time
        self.dic_info = {}
        # list of info id=values
        info_l = vcf_row[self.col_info_index].split(self.info_separator)
        for field in info_l:
            key_val = field.split("=")
            # if there is a value
            # considering flag type field do not have a value (e.g. SOMATIC)
            if len(key_val) > 1:
                if key_val[0] in self.dic_info:
                    self.dic_info[key_val[0]].append(key_val[1])
                else:
                    self.dic_info[key_val[0]] = [key_val[1]]

        return

    def checkFrequency(self, info_index, frequency_threshold):
        '''check if the mutation frequency is greater then
        the frequency value given in input
        info_index is the index corresponding to the annovar
        info field to read (multiple annovar date fields)
        '''
        res = False

        # if not filtering take the line anyway
        if frequency_threshold == 0.0:
            res = True
        else:
            # create a list with the three frequncy value considered
            l_freq = []
            f1 = self.readInfoValue(self.gnomAD_genome_ALL, info_index)
            f2 = self.readInfoValue(self.onet_genome, info_index)
            f3 = self.readInfoValue(self.exAC_ALL, info_index)

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

    def parsing(self, input_file, output_file, args):
        '''reads the pre-processed vcf file derived by
        1kgenomes chromosome files line by line writing a custom ouput file
        according to the arguments args given
        '''
        # print the pre-defined header to file see def in va class
        output_file.write(self.header)

        for line in input_file:
            # skip comments and description lines
            if line.startswith('#'):
                continue
            else:
                columns = line.split()

                # reading the gt value from the column considering that
                # some columns may have additional information separated by ":"
                GT = columns[self.col_GT_index].split(":")[0]

                # read all the info id=value in self.dic_info
                self.loadInfoDictionary(columns)

                # considering multiple GT values corresponding
                # to multiple annovar fields
                for gt_i in set(GT.split("|")):
                    gt_i = int(gt_i)
                    # if there is a mutation
                    if gt_i > 0:
                        gt_i = gt_i - 1
                        # filtering population frequency
                        if self.checkFrequency(gt_i, args.pop_frequency):
                            # read all the first 4 vcf standard field
                            new_line = columns[:4]
                            # read the corresponding ALT field
                            new_line.append(columns[4].split(",")[gt_i])
                            # read all the required info field
                            new_line.append(
                                self.readInfoValue(self.gene, gt_i))
                            new_line.append(
                                self.readInfoValue(self.func, gt_i))
                            new_line.append(
                                self.readInfoValue(self.exonicFunc, gt_i))
                            new_line.append(
                                self.readInfoValue(self.aaChange, gt_i))
                            new_line.append(
                                self.readInfoValue(self.gnomAD_genome_ALL, gt_i))
                            new_line.append(
                                self.readInfoValue(self.onet_genome, gt_i))
                            new_line.append(
                                self.readInfoValue(self.exAC_ALL, gt_i))

                            self.writeToFile(output_file, new_line)
        input_file.close()
        output_file.close()

    def writeToFile(self, out_file, vcf_cols):
        line = ""
        for c in vcf_cols:
            line += c + self.col_sep

        out_file.write(line+"\n")
