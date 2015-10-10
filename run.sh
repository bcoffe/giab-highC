#!/bin/bash

printf "**Downloading files from FTP Site....\n\n"
cd python/download
python download.py

printf "\n**File Download complete\n\n"

printf "**Intersecting files (ignoring exome files)\n\n"
cd ../intersection
python intersect.py

printf "**Replacing UCSC Gene Name with Gene Symbols"

printf "**Generating Gene Lists\n\n"
cd ../geneReport
python gene_report.py

printf "**Loading Tracks into IGV\n\n"
cd ../../IGV_2.3.60
./igv.sh &

printf "**Starting Local Web Server\n\n"
printf "**NOTE: Must have NodeJS installed or this will fail"

cd ../ui
npm start &

sleep 4
printf "**Opening IGV in Browser"
printf "**Only tested on Mac OS X"
open 'http://localhost:8000'
