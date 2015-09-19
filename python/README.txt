Executing the run shell script will run both the download python script to retrieve .bed files
and then run the interset python script to peform a 1 way intersection between the NIST file
and the downloaded lab files.

TO RUN:

>./run.sh

NOTE:

The python scripts may be run individually. However, by default the intersection python script
looks for .bed files in the default directory created by download.py. If you want to use a
different directory then change the config.json file in the intersection directory.
