import json
import getopt
import re
import sys
import os

__author__ = 'coffeybd'


def load_defaults():
    config_data = json.loads(open('data/config.json').read())

    global output_dir
    global ucsc_lookup_file

    output_dir = config_data['output_dir']
    ucsc_lookup_file = config_data['ucsc_lookup_file']


def get_cli(argv):
    try:
        opts, args = getopt.getopt(argv, "f:")
    except getopt.GetoptError:
        print "convert.py -f  <input_file>"
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print "convert.py -f <input_file>"
            sys.exit()
        elif opt in ("-f"):
            global input_file
            input_file = arg


def load_lookup_data():
    with open(ucsc_lookup_file) as file:
        dictionary = dict(line.rstrip().split(None, 1) for line in file)

    return dictionary


def convert_ucsc_names(dictionary):
    key_pattern = re.compile("uc[0-9]{3}[a-z]{3}.[0-9]+")
    replace_pattern = re.compile("uc[0-9]{3}[a-z]{3}.\w+")
    with open(output_dir + "known_gene_symbols_hg19.bed", 'w') as fout:
        with open(input_file) as fin:
            i = 1
            for line in fin:
                key = key_pattern.search(line)
                if key is not None:
                    print str(i) + ": matched: " + key.group(0)
                    i += 1
                    value_to_substitute = dictionary[key.group(0)]
                    value_to_replace = replace_pattern.search(line).group(0)
                    fout.write(re.sub(value_to_replace, value_to_substitute, line))
                else:
                    print "NOT FOUND"
                    print line

    print "File Created: " + output_dir + "known_gene_symbols_hg19.bed"


def main(argv):
    load_defaults()
    get_cli(argv)
    dictionary = load_lookup_data()
    convert_ucsc_names(dictionary)


# Not using the command line argument at moment but may later so just including it for now
if __name__ == '__main__':
    main(sys.argv[1:])