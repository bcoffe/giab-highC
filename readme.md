## Synopsis

This is a collection of quick scripts and 3rd party libraries that were used to create a work flow to aid in establishing which regions of NA12878 we had high-confidence in NGS ability to make accurate variant calls. This is an academic project and soley for the purpose of aiding open source research.

## Code Example

The main code is in the Python directory. These scripts are the heart of the workflow. IGV and UI simply display results in graphical IGVs.

## Motivation

The current Genome in a Bottle high-confidence calls include only ~77% of the genome, including ~77% of clinically important genes that are commonly tested by NGS.

## Installation

Coming Soon...

## API Reference

To run all the scripts you must have NodeJS, Java 6 or higher, python, and pybedtools installed and in your path.
NOTE: This has only been tested on Mac OS X and have an internet connection. This also assumes both Python 2.7.x and the following modules are installed (pip may be used to install most of these):

1. pybedtools
2. mysql connector (NOTE: Not installed from pip, dowload from Mysql Site)
3. shutil
4. ftplib
5. gzip
6. re
7. os
8. json
9. sys

This command will run all the scripts and load the data into IGV on both a web page and in the Java IGV from broad.

./run.sh

NOTE: It does take a few minutes to run because all the files are downloaded from ftp servers and then intersected.
When re-running script, you must first kill the local web server that was running in background.

use this command to find local web server:

ps -aux | grep node

Then look for process number (e.g., 32556) and then use the kill command, replacing {process number} with the number you found.

kill -9 {process number}

## Tests

Coming Soon...

## Contributors

In Alphabetical Order -- Coffey, Brent: George, Kevin: Hitz, Jordan: Rivero, Juan

## License

Apache
