import sys
import re

def mutated(tissue_type, vcf_row):
    col = 0
    ismutated = False

    if tissue_type == "normal":
        col = 9
    elif tissue_type == "primary":
        col = 10
    #else:
        #TODO
        #propagate error 

    selected_column_list = vcf_row[col].split(":")
    genotype = selected_column_list[0]
    regex = "([1]\|[0])|([0](\||\/)[1])" #matches 0/1, 1|0, 0|1
    
    if re.match(regex, genotype):
        ismutated = True
    #TODO return also column values to process further

    return ismutated, selected_column_list

#
# reads the Gene field in the annovar annotation field
#
def readGene(vcf_row):
    info = vcf_row[7].split(";")[4].split("=")[1]
    return info
#
# reads the Function field in the annovar annotation field
#
def readFunc(vcf_row):
    info = vcf_row[7].split(";")[3].split("=")[1]
    return info

#
# reads the Info field in the annovar annotation field
#
def readInfo(vcf_row, index):
    info = vcf_row[7].split(";")[index].split("=")[1]
    return info


def writeToFile(out_file, vcf_cols):
    line = ""
    for c in vcf_cols:
        line += c + "\t"

    out_file.write(line+"\n")

    

