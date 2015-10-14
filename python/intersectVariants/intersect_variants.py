import json
import sys
import os
import shutil
import pybedtools


__author__ = 'Brent Coffey'


def load_defaults():
    config_data = json.loads(open('data/config.json').read())

    global vcf_files_dir
    global exon_minus_nist_file
    global output_dir
    global static_vcf_file

    vcf_files_dir = config_data['vcf_files_dir']
    output_dir = config_data['output_dir']
    exon_minus_nist_file = config_data['exon_minus_nist_file']
    static_vcf_file = config_data['static_vcf_file']


def get_vcf_bed_file_paths():
    vcf_file_paths = []
    files = os.listdir(vcf_files_dir)
    for file_name in files:
        full_path_name = os.path.join(vcf_files_dir, file_name)
        if not file_name.startswith('.') \
                and file_name.endswith(".vcf"):
            vcf_file_paths.append(full_path_name)

    vcf_file_paths.append(static_vcf_file)
    return vcf_file_paths


def intersection(bed_file_paths):
    try:
        print '\n'.join(bed_file_paths)
        print "\nMulti-Intersecting files....this may take some time....\n\n"

        x = pybedtools.BedTool()
        multi_vcf_bed = x.multi_intersect(i=bed_file_paths).saveas(output_dir + "labs_VCF_multi_intersect.bed")

        print "\nIntersecting multiintersect output with exons_minus_nist.bed....this may take some time....\n\n"

        x_minus_nist = pybedtools.BedTool(exon_minus_nist_file)
        x_minus_nist.intersect(multi_vcf_bed).saveas(output_dir + "exons_minus_nist_labs_multi_intersect.bed")

        print "All Done..."

    except pybedtools.helpers.BEDToolsError:
        print sys.exc_type
        print sys.exc_info()
        print sys.exc_traceback
        print sys.exc_value
        print "Hmm....something is wrong with the file, is it a valid bed file?"
        print "Ignoring file and moving on to next file..."


def main(argv):
    load_defaults()
    vcf_file_paths = get_vcf_bed_file_paths()

    intersection(vcf_file_paths)


# Not using the command line argument at moment but may later so just including it for now
if __name__ == '__main__':
    main(sys.argv[1:])
