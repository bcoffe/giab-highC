import json
import re
import sys
import os
import shutil
import ntpath
import pybedtools

__author__ = 'Brent Coffey'


def load_defaults():
    config_data = json.loads(open('config.json').read())

    global bed_files_dir
    global output_dir

    bed_files_dir = config_data['bed_files_dir']
    output_dir = config_data['output_dir']


def get_bed_files():
    bed_files = []
    for root, dirs, files in os.walk(bed_files_dir):
        for file_name in files:
            if not file_name.startswith('.') and file_name.endswith(".bed"):
                bed_files.append(os.path.join(root, file_name))
    return bed_files


def intersection(master_file, lab_file):
    try:
        master = pybedtools.BedTool(master_file)
        lab = pybedtools.BedTool(lab_file)
        master.intersect(lab_file).saveas(output_dir + "out_" + ntpath.basename(lab_file))
        print (master + lab).count()

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
    bed_files.remove(master_file)
    print "File 1: " + master_file
    for lab_file in bed_files:
        print "File being intersected with NIST file: " + lab_file
        intersection(master_file, lab_file)


# Not using the command line argument at moment but may later so just including it for now
if __name__ == '__main__':
    main(sys.argv[1:])
