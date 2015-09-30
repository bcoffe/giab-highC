This is the heart of the scripts. Each of these python scripts may be run individually; however, they do build on each other. For example, one must have downloaded the BED files before the intersection can run. And Genes can not be extracted until intersection has run. By default the intersection python script
looks for .bed files in the default directory created by download.py. If you want to use a
different directory then change the config.json file in the intersection directory.

This will 

1. Download files
1a. Ignore Exome files
2. Perform multi intersection
2a. Creates 4 multi intersection files (1, 2, 3 or more lab, and full file)
2b. Creates 6 intersection files where each of 2a (1,2,3+) are intersected with KnownGenes and ACMG Gene BED files
3. Gene list are extracted from the files created in 2b
3. Loads the files into both IGV desktop and Genoverse Web application
3a. A local web server is started to show Genoverse Web application.

NOTE:

Hit Go to create index files for IGV when/if prompted.

