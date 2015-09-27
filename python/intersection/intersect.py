import json
import re
import sys
import os
import shutil
import pybedtools

__author__ = 'Brent Coffey'


def load_defaults():
    config_data = json.loads(open('data/config.json').read())

    global bed_files_dir
    global output_dir
    global genes_file
    global sorted_bed_dir

    bed_files_dir = config_data['bed_files_dir']
    output_dir = config_data['output_dir']
    genes_file = config_data['genes_file']
    sorted_bed_dir = config_data['sorted_bed_dir']


def exome_sequence(file_name):
    return re.search("\wExome\w", file_name, re.IGNORECASE)


def nist_sequence(file_name):
    return re.search("\wNIST\w", file_name, re.IGNORECASE)

def na19240(file_name):
    return re.search("\w19240\w", file_name, re.IGNORECASE)

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
    for root, dirs, files in os.walk(bed_files_dir):
        for file_name in files:
            full_path_name = os.path.join(root, file_name)
            if not file_name.startswith('.') \
                    and file_name.endswith(".bed") \
                    and not empty_file(full_path_name)\
                    and not exome_sequence(full_path_name)\
                    and not nist_sequence(full_path_name)\
                    and not na19240(full_path_name):
                sorted = pybedtools.BedTool(full_path_name).sort()
                sorted.saveas(sorted_bed_dir + file_name)
                sorted_bed_file_paths.append(sorted_bed_dir + file_name)

    return sorted_bed_file_paths


def intersection(bed_file_paths):
    print "Intersecting files....this may take some time...."
    try:
        x = pybedtools.BedTool()
        x.multi_intersect(i=bed_file_paths).saveas(output_dir + "all_labs_multi_intersect.bed")

        print "All Done.."
        print "Created Output File: " + output_dir + "all_labs_multi_intersect.bed"

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

    print(sorted_bed_file_paths)

    intersection(sorted_bed_file_paths)


# Not using the command line argument at moment but may later so just including it for now
if __name__ == '__main__':
    main(sys.argv[1:])
