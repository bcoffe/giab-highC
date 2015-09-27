#!/bin/bash

printf "**Downloading files from FTP Site....\n\n"
cd python/download
python download.py

printf "\n**File Download complete\n\n"

printf "**Intersecting files (ignoring exome files)\n\n"
cd ../intersection
python intersect.py

printf "**Loading Tracks into IGV\n\n"
cd ../../IGV_2.3.60
./igv.sh
