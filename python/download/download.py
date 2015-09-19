import ftplib
import shutil
import json
import os
import sys

__author__ = 'Brent Coffey'

# This method is modified from http://stackoverflow.com/questions/2605119/downloading-a-directory-tree-with-ftplib
def downloadFiles(ftp_connection, path):
    try:
        ftp_connection.cwd(path)

    except ftplib.error_perm:
        #invalid entry (ensure input form: "/dir/folder/something/")
        print "error: could not change to "+ path
        sys.exit("ending session")

    #list children:
    filelist=ftp_connection.nlst()

    for file in filelist:
        try:
            # This will check if file is folder:
            ftp_connection.cwd(path + "/" + file + "/")
            # If this is a folder go into it
            downloadFiles(ftp_connection, path + "/" + file + "/")
        # If this except is called that means we have a file not a directory so lets save it if its a bed file
        except ftplib.error_perm:
            # Only download bed files
            if file.endswith('.bed'):
                ftp_connection.retrbinary('RETR %s' % file, open(bed_files_dir+file,"wb").write)
                print file + " downloaded"


def load_defaults():
    config_data = json.loads(open('config.json').read())

    global bed_files_dir
    global ftp_site
    global base_dir

    bed_files_dir = config_data['bed_files_dir']
    ftp_site = config_data['ftp_site']
    base_dir = config_data['base_dir']


def create_download_dir():
    if os.path.exists(bed_files_dir):
        shutil.rmtree(bed_files_dir)
    else:
        os.makedirs(bed_files_dir)


def get_bed_files():
    ftp_connection = ftplib.FTP(ftp_site)
    ftp_connection.login()
    ftp_connection.cwd(base_dir)
    downloadFiles(ftp_connection, base_dir)


def main(argv):
    load_defaults()
    create_download_dir()
    get_bed_files()
    print bed_files_dir


# Not using the command line argument at moment but may later so just including it for now
if __name__ == '__main__':
    main(sys.argv[1:])
