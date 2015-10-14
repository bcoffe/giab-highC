import sys
import json
import pybedtools

__author__ = 'brentcoffey'

def perform_intersection ():
        exons = pybedtools.BedTool(exons_file)
        nist = pybedtools.BedTool(nist_file)

        print "Subtracting/Removing Nist Regions from Gene Exons file"
        print "This make take a few minutes....."
        #delta = exons - nist #.intersect(nist)
        exons.subtract(nist).saveas(output_dir + "exons_minus_nist.bed")
        #delta.saveas(output_dir + "exons_minus_nist.bed")

        print "Delta saved as " + output_dir + "exons_minus_nist.bed"


def load_defaults():
    config_data = json.loads(open('data/config.json').read())

    global exons_file
    global nist_file
    global output_dir

    exons_file = config_data['exons_file']
    nist_file = config_data['nist_file']
    output_dir = config_data['output_dir']


def main(argv):
    load_defaults()
    perform_intersection()

#"nist_file" : "../../ui/data/bed/converted_NIST_GIAB_High_confidence_SNPs_indels_v_2_18.bed",
# Not using the command line argument at moment but may later so just including it for now
if __name__ == '__main__':
    main(sys.argv[1:])