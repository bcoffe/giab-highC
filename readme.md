## Synopsis

Establish high-confidence SNP, indel, and homozygous reference genotype calls in close to 100 % of as many clinically-tested regions as possible.

## Code Example

Coming Soon...

## Motivation

The current Genome in a Bottle high-confidence calls include only ~77% of the genome, including ~77% of clinically important genes that are commonly tested by NGS.

## Installation

Coming Soon...

## API Reference

To run all the scripts you must have NodeJS installed and in your path.
NOTE: This has only been tested on Mac OS X and have an internet connection

This command will run all the scripts and load the data into IGV on both a web page and in the Java IGV from broad.

./run.sh

NOTE: It does take a few minutes to run because all the files are downloaded from ftp servers and then intersected.
When re-running script, you must first kill the local web server that was running in background.

use this command to find local web server:

ps -aux | grep npm

Then look for process number (e.g., 32556) and then use the kill command, replacing {process number} with the number you found.

kill -9 {process number}

## Tests

Coming Soon...

## Contributors

In Alphabetical Order -- Coffey, Brent: George, Kevin: Hitz, Jordon: Rivero, Juan

## License

Apache
