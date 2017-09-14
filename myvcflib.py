import sys
import re

def mutated(tissue_type, vcf_row):
    col = 0
    ismutated = False

    if tissue_type = "normal":
        col = 10
    elif tissue_type = "primary":
        col = 11
    else:
        #TODO
        #propagate error 

    genotype = vcf_row[col].split(":")[0]
    regex = "([1]\|[0])|([0](\||\/)[1])" #matches 0/1, 1|0, 0|1
    
    if re.match(regex, genotype):
        ismutated = True
#TODO return also column values to process further
    return ismutated

