import ftplib
import shutil
import json
import gzip
import os
import sys

__author__ = 'Brent Coffey'

def chromosome (s):
    if s[:1] == '#':
        return False
    else:
        return True


# This method is modified from http://stackoverflow.com/questions/2605119/downloading-a-directory-tree-with-ftplib
def download_files(ftp_connection, path, extension, write_dir):
    try:
        ftp_connection.cwd(path)

    except ftplib.error_perm:
        #invalid entry (ensure input form: "/dir/folder/something/")
        print "error: could not change to "+ path
        sys.exit("ending session")

    #list children:
    file_list=ftp_connection.nlst()

    for file in file_list:
        try:
            # This will check if file is folder:
            ftp_connection.cwd(path + "/" + file + "/")
            # If this is a folder go into it
            download_files(ftp_connection, path + "/" + file + "/", extension, write_dir)
        # If this except is called that means we have a file not a directory so lets save it if its a bed file
        except ftplib.error_perm:
            # Only files with given extension
            if file.endswith(extension):
                ftp_connection.retrbinary('RETR %s' % file, open(write_dir+file,"wb").write)
                print file + " downloaded"
                if file.endswith(".gz"):
                        # and not re.search(".BI.", file, re.IGNORECASE)\
                        # and not re.search (".NIST_NA12878.", file, re.IGNORECASE):
                    print file + " unzipping.....this can take a few minutes...please wait"
                    with gzip.open(write_dir+file, 'rb') as fin:

                        file_name_no_extension = os.path.splitext(file)[0]
                        if extension == ".vcf.gz":
                            print file_name_no_extension + " is being copied to /vcf"
                            with open("vcf/"+file_name_no_extension, "w+") as fout:
                                for line in fin:
                                    if chromosome(line):
                                        line = 'chr' + line
                                    fout.write(line)
                        else:
                            with open("bed/"+file_name_no_extension, "w+") as fout:
                                for line in fin:
                                    fout.write(line)



def load_defaults():
    config_data = json.loads(open('config.json').read())

    global bed_files_dir
    global ftp_site
    global base_dir
    global platinum_site
    global platinum_base_dir
    global vcf_lab_dir
    global vcf_gz_files_dir

    bed_files_dir = config_data['bed_files_dir']
    ftp_site = config_data['ftp_site']
    base_dir = config_data['base_dir']
    platinum_site = config_data['platinum_site']
    platinum_base_dir = config_data['platinum_base_dir']
    vcf_lab_dir = config_data['vcf_lab_dir']
    vcf_gz_files_dir = config_data['vcf_gz_files_dir']


def create_download_dir(write_dir):
    if os.path.exists(write_dir):
        shutil.rmtree(write_dir)
        os.makedirs(write_dir)
    else:
        os.makedirs(write_dir)


def get_files(site, dir, extension, write_dir):
    ftp_connection = ftplib.FTP(site)
    ftp_connection.login()
    ftp_connection.cwd(dir)
    download_files(ftp_connection, dir, extension, write_dir)


def main(argv):
    load_defaults()
    create_download_dir(bed_files_dir)
    create_download_dir(vcf_gz_files_dir)
    get_files(ftp_site, base_dir, '.bed', bed_files_dir)
    get_files(ftp_site, vcf_lab_dir, '.vcf.gz', vcf_gz_files_dir)
    get_files(platinum_site, platinum_base_dir, '.bed.gz', bed_files_dir)


# Not using the command line argument at moment but may later so just including it for now
if __name__ == '__main__':
    main(sys.argv[1:])
