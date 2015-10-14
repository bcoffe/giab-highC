import json
import re
import sys
import os
from os import path
import shutil
import pybedtools
import ntpath

__author__ = 'Brent Coffey'


def load_defaults():
    config_data = json.loads(open('data/config.json').read())

    global bed_files_dir
    global output_dir
    global genes_file
    global sorted_bed_dir
    global static_bed_file

    bed_files_dir = config_data['bed_files_dir']
    output_dir = config_data['output_dir']
    genes_file = config_data['genes_file']
    sorted_bed_dir = config_data['sorted_bed_dir']
    static_bed_file = config_data['static_bed_file']


def exome_sequence(file_name):
    return re.search(".Exome.", file_name, re.IGNORECASE) \
           or re.search(".GPS_WUSTL_Sure_Select_All_Exon.", file_name, re.IGNORECASE) \
           or re.search(".UCSF_WES_Agilent.", file_name, re.IGNORECASE) \
           or re.search(".GPS_WUSTL_SureSelect_Exon", file_name, re.IGNORECASE) \
           or re.search(".HSPH_Xprize", file_name, re.IGNORECASE)\
           or re.search("ConfidentRegion.", file_name, re.IGNORECASE)


def nist_sequence(file_name):
    return re.search("\wNIST\w", file_name, re.IGNORECASE)

def na19240(file_name):
    return re.search("\w19240", file_name, re.IGNORECASE)

def empty_file(file_name):
    file_size = os.stat(file_name).st_size
    return os.stat(file_name).st_size == 0


def created_sorted_dir():
    if os.path.exists(sorted_bed_dir):
        shutil.rmtree(sorted_bed_dir)
        os.makedirs(sorted_bed_dir)
    else:
        os.makedirs(sorted_bed_dir)

def get_sorted_bed_file_paths():
    sorted_bed_file_paths = []
    files = os.listdir(bed_files_dir)
    for file_name in files:
        full_path_name = os.path.join(bed_files_dir, file_name)
        if not file_name.startswith('.') \
                and file_name.endswith(".bed") \
                and not empty_file(full_path_name)\
                and not exome_sequence(full_path_name)\
                and not nist_sequence(full_path_name)\
                and not na19240(full_path_name):
            sorted = pybedtools.BedTool(full_path_name).sort()
            sorted.saveas(sorted_bed_dir + file_name)
            sorted_bed_file_paths.append(sorted_bed_dir + file_name)

    sorted =pybedtools.BedTool(static_bed_file).sort()
    sorted.saveas(sorted_bed_dir + ntpath.basename(static_bed_file))
    sorted_bed_file_paths.append(sorted_bed_dir + ntpath.basename(static_bed_file))
    return sorted_bed_file_paths


def intersection(bed_file_paths):
    pattern = re.compile("^.+?\t.+?\t.+?\t.*?([0-9]+)")
    print "Intersecting files....this may take some time...."
    try:
        print '\n'.join(bed_file_paths)
        x = pybedtools.BedTool()
        x.multi_intersect(i=bed_file_paths).saveas(output_dir + "all_labs_multi_intersect.bed")

        one_lab = open(output_dir + "1lab.bed", 'w')
        two_lab = open(output_dir + "2lab.bed", 'w')
        three_lab = open(output_dir + "3_or_more_lab.bed", 'w')

        with open(output_dir + "all_labs_multi_intersect.bed",'r') as f:
            for line in f:
                labs_confident = pattern.match(line)
                if labs_confident is not None:
                    num_labs = int(labs_confident.group(1))
                    if num_labs == 1:
                        one_lab.write(line)
                    elif num_labs == 2:
                        two_lab.write(line)
                    else:
                        three_lab.write(line)

        one_lab.close()
        two_lab.close()
        three_lab.close()

        print "Created Output File: " + output_dir + "all_labs_multi_intersect.bed"
        print "Now intersecting Output file with known genes"
        known_genes = pybedtools.BedTool("../../ui/data/bed/known_gene_symbols_hg19.bed")
        acmg_genes = pybedtools.BedTool("../../ui/data/bed/ACMG_56genesHg19.bed")

        platinum8 = pybedtools.BedTool("../../ui/data/bed/PlatinumConfRegions8.bed")
        nist = pybedtools.BedTool("../../ui/data/bed/converted_NIST_GIAB_High_confidence_SNPs_indels_v_2_18.bed")

        all_labs = pybedtools.BedTool(output_dir + "all_labs_multi_intersect.bed")
        lab1 = pybedtools.BedTool(output_dir + "1lab.bed")
        lab2 = pybedtools.BedTool(output_dir + "2lab.bed")
        lab3 = pybedtools.BedTool(output_dir + "3_or_more_lab.bed")

        print "Intersecting Known genes with all"
        known_genes.intersect(all_labs).saveas(output_dir+"known_genes_all_labs.bed")
        print "Intersecting ACMG genes with all"
        acmg_genes.intersect(all_labs).saveas(output_dir+"acmg_genes_all_labs.bed")
        print "Intersection Platinum 8 with all"
        platinum8.intersect(all_labs).saveas(output_dir+"plat8_all_labs.bed")
        print "Intersection NIST 8 with all"
        nist.intersect(all_labs).saveas(output_dir+"NIST_all_labs.bed")

        print "Intersecting Known genes with 1 Lab"
        known_genes.intersect(lab1).saveas(output_dir+"known_genes_1_lab.bed")
        print "Intersecting ACMG genes with 1 Lab"
        acmg_genes.intersect(lab1).saveas(output_dir+"acmg_genes_1_lab.bed")
        print "Intersection Platinum 8 with 1 Lab"
        platinum8.intersect(lab1).saveas(output_dir+"plat8_1_lab.bed")
        print "Intersection NIST 8 with 1 Lab"
        nist.intersect(lab1).saveas(output_dir+"nist_1_lab.bed")

        print "Intersecting Known genes with 2 Labs"
        known_genes.intersect(lab2).saveas(output_dir+"known_genes_2_labs.bed")
        print "Intersecting ACMG genes with 2 Labs"
        acmg_genes.intersect(lab2).saveas(output_dir+"acmg_genes_2_labs.bed")
        print "Intersection Platinum 8 with 2 Labs"
        platinum8.intersect(lab2).saveas(output_dir+"plat8_2_labs.bed")
        print "Intersection NIST 8 with 2 Labs"
        nist.intersect(lab2).saveas(output_dir+"nist_2_labs.bed")

        print "Intersecting Known genes with 3 or more Labs"
        known_genes.intersect(lab3).saveas(output_dir+"known_genes_3_labs.bed")
        print "Intersecting ACMG genes with 3 or more Labs"
        acmg_genes.intersect(lab3).saveas(output_dir+"acmg_genes_3_labs.bed")
        print "Intersection Platinum 8 with 3 Labs"
        platinum8.intersect(lab3).saveas(output_dir+"plat8_3_labs.bed")
        print "Intersection NIST 8 with 3 Labs"
        nist.intersect(lab3).saveas(output_dir+"nist_3_labs.bed")

        print "All Done..."

    except pybedtools.helpers.BEDToolsError:
        print sys.exc_type
        print sys.exc_info()
        print sys.exc_traceback
        print sys.exc_value
        print "Hmm....something is wrong with the file, is it a valid bed file?"
        print "Ignoring file and moving on to next file..."


def create_output_dir():
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)
    else:
        os.makedirs(output_dir)


# Main file that all the labs will be intersected against
# todo: make robust. Currently assumes 1 and only one file will match.
def get_master_file(bed_files):
    return bed_files[int([i for i, item in enumerate(bed_files) if re.search("\wNIST\w", item)][0])]


def main(argv):
    load_defaults()
    create_output_dir()
    created_sorted_dir()
    sorted_bed_file_paths = get_sorted_bed_file_paths()

    intersection(sorted_bed_file_paths)


# Not using the command line argument at moment but may later so just including it for now
if __name__ == '__main__':
    main(sys.argv[1:])
