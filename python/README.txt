Executing the run shell script will run both the download python script to retrieve .bed files
and then run the interset python script to peform a 1 way intersection between the NIST file
and the downloaded lab files.

TO RUN:

Go up a directory and then  make sure run.sh is executable by doing this:

>chmod +x run.sh

then...

>./run.sh

NOTE:

The python scripts may be run individually. However, by default the intersection python script
looks for .bed files in the default directory created by download.py. If you want to use a
different directory then change the config.json file in the intersection directory.

This will 

1. Download files
1a. Ignore Exome files
2. Perform multi intersection
2a. Creates 4 multi intersection files (1, 2, 3 or more lab, and full file)
3. Loads 1,2, and 3 into IGV from command line

NOTE:

Hit Go to create index files for IGV when/if prompted.

