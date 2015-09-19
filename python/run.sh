#!/bin/bash

printf "**Downloading files from FTP Site....\n\n"
cd download
python download.py

printf "\n**File Download complete\n\n"

printf "**Intersecting NIST Master file with each of the downloaded files\n\n"
cd ../intersection
python intersect.py
