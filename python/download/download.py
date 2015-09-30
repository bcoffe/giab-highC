import ftplib
import shutil
import json
import gzip
import os
import sys

__author__ = 'Brent Coffey'

# This method is modified from http://stackoverflow.com/questions/2605119/downloading-a-directory-tree-with-ftplib
def download_files(ftp_connection, path, extension):
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
            download_files(ftp_connection, path + "/" + file + "/", extension)
        # If this except is called that means we have a file not a directory so lets save it if its a bed file
        except ftplib.error_perm:
            # Only download bed files
            if file.endswith(extension):
                ftp_connection.retrbinary('RETR %s' % file, open(bed_files_dir+file,"wb").write)
                print file + " downloaded"
                if file.endswith(".gz"):
                    with gzip.open(bed_files_dir+file, 'rb') as f:
                        file_content = f.read()
                        with open("../../ui/data/bed/PlatinumConfRegions8.bed", "w+") as fout:
                            fout.write(file_content)


def load_defaults():
    config_data = json.loads(open('config.json').read())

    global bed_files_dir
    global ftp_site
    global base_dir
    global platinum_site
    global platinum_base_dir

    bed_files_dir = config_data['bed_files_dir']
    ftp_site = config_data['ftp_site']
    base_dir = config_data['base_dir']
    platinum_site = config_data['platinum_site']
    platinum_base_dir = config_data['platinum_base_dir']


def create_download_dir():
    if os.path.exists(bed_files_dir):
        shutil.rmtree(bed_files_dir)
        os.makedirs(bed_files_dir)
    else:
        os.makedirs(bed_files_dir)


def get_bed_files(site, dir, extension):
    ftp_connection = ftplib.FTP(site)
    ftp_connection.login()
    ftp_connection.cwd(dir)
    download_files(ftp_connection, dir, extension)


def main(argv):
    load_defaults()
    create_download_dir()
    get_bed_files(ftp_site, base_dir, '.bed')
    get_bed_files(platinum_site, platinum_base_dir, '.bed.gz')


# Not using the command line argument at moment but may later so just including it for now
if __name__ == '__main__':
    main(sys.argv[1:])
