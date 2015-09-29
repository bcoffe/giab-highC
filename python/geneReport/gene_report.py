import json
import re
import sys
import os

__author__ = 'coffeybd'


def get_genes_from_bed(file_name):
    gene_list = []
    with open(file_name, "r") as fin:
        for line in fin:
            gene_symbol = re.split('\t+', line)[3]
            gene_list.append(gene_symbol)

    return set(gene_list)



def main(argv):
    acmg_1_lab = get_genes_from_bed("../../ui/data/bed/temp/acmg_genes_1_lab.bed")
    acmg_2_lab = get_genes_from_bed("../../ui/data/bed/temp/acmg_genes_2_labs.bed")
    acmg_3_lab = get_genes_from_bed("../../ui/data/bed/temp/acmg_genes_3_labs.bed")

    acmg_1_only = set()
    for item in acmg_1_lab:
        if item not in acmg_2_lab:
            if item not in acmg_3_lab:
                acmg_1_only.add(item)

    acmg_2_max = set()
    for item2 in acmg_2_lab:
        if item2 not in acmg_3_lab:
            acmg_2_max.add(item2)

    acmg_1_list = sorted(list(acmg_1_only))
    acmg_2_list = sorted(list(acmg_2_max))
    acmg_3_list = sorted(list(acmg_3_lab))

    known_1_lab = get_genes_from_bed("../../ui/data/bed/temp/known_genes_1_lab.bed")
    known_2_lab = get_genes_from_bed("../../ui/data/bed/temp/known_genes_2_labs.bed")
    known_3_lab = get_genes_from_bed("../../ui/data/bed/temp/known_genes_3_labs.bed")

    known_1_only = set()
    for item in known_1_lab:
        if item not in known_2_lab:
            if item not in known_3_lab:
                known_1_only.add(item)

    known_2_max = set()
    for item in known_2_lab:
        if item not in known_3_lab:
            known_2_max.add(item)

    known_1_list = sorted(list(known_1_only))
    known_2_list = sorted(list(known_2_max))
    known_3_list = sorted(list(known_3_lab))

    with open("genes.txt", "w") as fout:
        fout.write("ACMG, 1, " + str(len(acmg_1_list)) + ", " + ",".join(acmg_1_list) + "\n")
        fout.write("ACMG, 2, " + str(len(acmg_2_list)) + ", " + ",".join(acmg_2_list) + "\n")
        fout.write("ACMG, 3+, " + str(len(acmg_3_list)) + ", " + ",".join(acmg_3_list) + "\n")
        fout.write("Known, 1, " + str(len(known_1_list)) + ", " + ",".join(known_1_list) + "\n")
        fout.write("Known, 2, " + str(len(known_2_list)) + ", " + ",".join(known_2_list) + "\n")
        fout.write("Known, 3+, " + str(len(known_3_list)) + ", " + ",".join(known_3_list) + "\n")


# Not using the command line argument at moment but may later so just including it for now
if __name__ == '__main__':
    main(sys.argv[1:])
