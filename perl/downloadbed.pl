#!/bin/perl

use LWP::Simple;
use Archive::Tar;

# todo: put in a config file
$dir = 'bed/';#fill in wherever you want to save your bed file
$newbed = 'GeT-RM.bed';
$page = 'ftp://ftp.ncbi.nlm.nih.gov/variation/get-rm/current/exome_capture_reagents/';
$webpage = get("$page");
#Assign colors to each file
my @colors= qw(255,0,0 255,255,0 102,204,0 0,128,255 128,128,128 255,128,0 127,0,255 0,0,0 255,0,127 153,255,204 255,204,153 178,255,102 51,255,153 102,0,51);
my @colorsx3 = (@colors,@colors,@colors);
my $col = 0;

#Create combined bed file
# todo: this assumes directory already exist
open $out,">","$dir$newbed";
print $out 'track name="GeT-RM regions for NA12878" description="',$page,'" gffTags=on itemRgb=on',"\n";

#Get list of folders/companies
GET_FOLDERS:foreach my $folder (split("\n", $webpage)){
	@folders = split/2014 /,$folder;
	print $folders[1],"\n";
	if ($folders[1] =~ /tmp/){next GET_FOLDERS;}
	$comp = get("$page$folders[1]");
	#Get list of bed files
	foreach my $file (split("\n",$comp)){
		@files = split/2014 /,$file unless ($file =~ /NA19240/g);
		@filename = split/converted_|\.bed/,$files[1];
		$bedfile = get ("$page$folders[1]/$files[1]");
		$color = $colorsx3[$col];
		# Why are we concatenating bed files and not doing an intersect?
		#Read in bed files and process each line to put in final format
		foreach my $line (split("\n",$bedfile)){
			if ($line =~ /^chr/){
				($chr,$start,$end)=split/\t/,$line;
				print $out "$line\t$filename[1]\t1000\t-\t$start\t$end\t$color\n";
			}
		}
		++$col;
	}
}
close $out;
#IGV and bedtools will usually not process files unless sorted.  This code in the terminal 
#will sort the file by chromosome and then start position
print STDERR "bedtools sort -i $dir$newbed > $dir\sorted_$newbed\n";
print STDERR "bgzip $dir\sorted_$newbed\n";