#!/bin/bash

#printf "**Downloading files from FTP Site....\n\n"
#cd python/download
#python download.py

printf "\n**File Download complete\n\n"

printf "**Intersecting files (ignoring exome files)\n\n"
cd python/intersection
python intersect.py

printf "**Generating Gene Lists\n\n"
cd ../geneReport
python gene_report.py

printf "**Replacing UCSC Gene Name with Gene Symbols is no longer requried\n\n"

printf "**Making Database connection to UCSC to get Exons for ACMG Genes\n"
printf "**By default only getting exons for ACMG Genes that were tested by 1, 2, or 3+ labs**\n"
printf "NOTE: This default can be changed with a one line change to the code to either remove a lab or to include knownGenes\n\n"
cd ../getExons
python get_exons.py

printf "**Removing any region that is NIST 2.19 from the above exons\n\n"
cd ../removeNISTRegions
python remove_nist_regions.py

printf "**Loading Tracks into IGV\n\n"
cd ../../IGV_2.3.60
./igv.sh &

# Section below is for creating a web based report
# printf "**Starting Local Web Server\n\n"
# printf "**NOTE: Must have NodeJS installed or this will fail"

# cd ../ui
# npm start &

# sleep 4
# printf "**Opening IGV in Browser"
# printf "**Only tested on Mac OS X"
# open 'http://localhost:8000'
