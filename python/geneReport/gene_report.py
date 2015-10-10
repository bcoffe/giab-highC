import re
import sys
import os
import shutil
import json

__author__ = 'coffeybd'



def get_genes_from_bed(file_name):
    gene_list = []
    with open(file_name, "r") as fin:
        for line in fin:
            gene_symbol = re.split('\t+', line)[3]
            gene_list.append(gene_symbol)

    return set(gene_list)

def create_output_dir():
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)
    else:
        os.makedirs(output_dir)


def main(argv):
    global output_dir
    output_dir = "../../ui/data/json"

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

    create_output_dir()

    with open(output_dir +"/genes.json", "w") as fout:
        acmg1_dict = { "intersect" : "acmg", "lab_agree":"1", "gene_count": str(len(acmg_1_list)), "genes": acmg_1_list}
        acmg2_dict = { "intersect" : "acmg", "lab_agree":"2", "gene_count": str(len(acmg_2_list)), "genes": acmg_2_list}
        acmg3_dict = { "intersect" : "acmg", "lab_agree":"3+", "gene_count": str(len(acmg_3_list)), "genes": acmg_3_list}

        known1_dict = { "intersect" : "KnownGene", "lab_agree":"1", "gene_count": str(len(known_1_list)), "genes": known_1_list}
        known2_dict = { "intersect" : "KnownGene", "lab_agree":"2", "gene_count": str(len(known_2_list)), "genes": known_2_list}
        known3_dict = { "intersect" : "KnownGene", "lab_agree":"3+", "gene_count": str(len(known_3_list)), "genes": known_3_list}
        intersect_list = [acmg1_dict, acmg2_dict, acmg3_dict, known1_dict, known2_dict, known3_dict]
        gene_dict = {"intersects" : intersect_list}

        fout.write(json.dumps(gene_dict,indent=4, sort_keys=True))

    print "Created: " + output_dir + "/genes.json"


# Not using the command line argument at moment but may later so just including it for now
if __name__ == '__main__':
    main(sys.argv[1:])
