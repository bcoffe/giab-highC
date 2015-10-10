import json
import getopt
import re
import sys
import mysql.connector
import os

__author__ = 'brentcoffey'

def build_gene_list():
    gene_list = []
    with open(genes_file, 'r') as fin:
        data = json.load(fin)
        for lab in labs:
            for intersect in data["intersects"]:
                if acmg_flag and intersect["intersect"].lower() == "acmg" and intersect["lab_agree"] == lab:
                        gene_list += intersect["genes"]
                if known_gene_flag and intersect["intersect"].lower() == "KnownGene" and intersect["lab_agree"] == lab:
                        gene_list += intersect["genes"]

    return ", ".join("'" + gene + "'" for gene in gene_list)


def connect_to_ucsc():
    genes = build_gene_list()

    print "Getting Exons for Genes: " + genes
    print "Connecting to UCSC to get Exons...."

    cnx = mysql.connector.connect(user='genome',
                                  host='genome-mysql.cse.ucsc.edu',
                                  database='hg19')
    cursor = cnx.cursor()
    query = ("SELECT kg.chrom AS chromosome, kg.exonStarts As start, kg.exonEnds As end, x.geneSymbol as gene_symbol, " +
             "0 AS 'score', kg.strand AS strand FROM knownGene kg, kgXref x " +
             "WHERE x.geneSymbol IN ( " + genes + " ) AND kg.name = x.kgID ORDER BY chromosome, start;")

    cursor.execute(query)
    write_bed_file (cursor)
    cnx.close()


def write_bed_file(cursor):
    print "Writing Exons to BED file..."
    with open(output_file, 'w') as fout:
        for(chromosome, start, end, gene_symbol, score, strand) in cursor:
            # the :-1 is chopping off the trailing ',' that is in the database for these blocks.
            # I'm then splitting the blocks by comma
            start_list = start[:-1].split(",")
            end_list = end[:-1].split(",")
            #Pairing start of exon with end of exon and printing in bed format
            for idx, start_pos in enumerate(start_list):
                fout.write("{}\t{}\t{}\t{}\t{}\t{}\t204,102,0\n".format(chromosome, start_pos, end_list[idx], gene_symbol, score, strand))
    print "Bed File: " + output_file + " created"

def load_defaults():
    config_data = json.loads(open('data/config.json').read())

    global genes_file
    global output_file

    genes_file = config_data['genes_file']
    output_file = config_data['output_file']


def get_cli(argv):
    global known_gene_flag
    global acmg_flag
    global labs

    known_gene_flag = False
    acmg_flag = True
    labs = ['3+']

    # try:
    #     opts, args = getopt.getopt(argv, 'l')
    # except getopt.GetoptError:
    #     print "get_exons.py -l <labs_in_agreement> -a <acmg_genes> -k <known_genes>"
    #     sys.exit(2)
    #
    # for opt, arg in opts:
    #     if opt == '-h':
    #         print "get_exons.py -l <labs_in_agreement> -a <acmg_genes> -k <known_genes>"
    #         sys.exit()
    #     elif opt in ("-l"):
    #         print arg
    #         # if ',' in arg:
    #         #     labs = arg.split(",")
    #         # else:
    #         #     labs = [arg]
    #     elif opt in '-a':
    #         acmg_flag = True
    #     elif opt in '-k':
    #         known_gene_flag = True


def main(argv):
    load_defaults()
    get_cli(argv)
    connect_to_ucsc()

    # dictionary = load_lookup_data()
    # convert_ucsc_names(dictionary)


# Not using the command line argument at moment but may later so just including it for now
if __name__ == '__main__':
    main(sys.argv[1:])