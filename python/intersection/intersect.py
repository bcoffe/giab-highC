import json
import re
import sys
import os
import shutil
import ntpath
import pybedtools

__author__ = 'Brent Coffey'


def load_defaults():
    config_data = json.loads(open('data/config.json').read())

    global bed_files_dir
    global output_dir
    global genes_file

    bed_files_dir = config_data['bed_files_dir']
    output_dir = config_data['output_dir']
    genes_file = config_data['genes_file']


def get_bed_files():
    bed_files = []
    for root, dirs, files in os.walk(bed_files_dir):
        for file_name in files:
            if not file_name.startswith('.') and file_name.endswith(".bed"):
                bed_files.append(os.path.join(root, file_name))
    return bed_files


def intersection(master_file, choices, all_bed_files):
    try:
        bed_files = []
        for choice in choices:
            bed_files.append(pybedtools.BedTool(all_bed_files[int(choice)-1]))

        if len(choices) < 3:
            bed_files[0].intersect(bed_files[1]).saveas(output_dir + "out_intersect_" +
                                                        ntpath.basename(all_bed_files[int(choices[0])-1]) + "_" +
                                                        ntpath.basename(all_bed_files[int(choices[1])-1]))
        else:
            bed_files[0].intersect(bed_files[1], b=[bed_files[2]]).saveas(output_dir + "out_intersect_" +
                                                        ntpath.basename(all_bed_files[int(choices[0])-1]) + "_" +
                                                        ntpath.basename(all_bed_files[int(choices[1])-1]) + "_" +
                                                        ntpath.basename(all_bed_files[int(choices[2])-1]))

    except pybedtools.helpers.BEDToolsError:
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
    bed_files = get_bed_files()

    master_file = get_master_file(bed_files)

    # Uncomment this later...as we will want to compare the labs to this NIST file
    # for now we are just going to treat it like any other lab for testing purposes.
    #bed_files.remove(master_file)
    
    i = 1
    print "Choose 2 or 3 files to intersect by separating with comma: (ex: 1,2,3)"
    print "NOTE: You must pick at least 2 files"
    for lab_file in bed_files:
        print "(" + str(i) + ") " + ntpath.basename(lab_file)
        i += 1

    choices = list(input("Choices > "))

    if len(choices) > 3 or len(choices) < 2:
        print "Error... You must pick at least 2 files and no more than 3"
    else:
        intersection(master_file, choices, bed_files)


# Not using the command line argument at moment but may later so just including it for now
if __name__ == '__main__':
    main(sys.argv[1:])
