#!/bin/perl

#From terminal: bedtools multiinter -names converted_*.bed -g converted_*.bed > multiinter
open $in,"<","/dir/multiinter";
open $bed1,">","/mnt/hgfs/VCF/GIAB/GeT-RM/bed_onetest.bed";
print $bed1 'track name="Only 1 test coverage" gffTags=on visibility=2\n';
open $bed2,">","/mnt/hgfs/VCF/GIAB/GeT-RM/bed_twotest.bed";
print $bed2 'track name="< 3 test coverage" gffTags=on visibility=2\n';
open $bed3,">","/mnt/hgfs/VCF/GIAB/GeT-RM/bed_3test.bed";
print $bed3 'track name="> 2 test coverage" gffTags=on visibility=2',"\n";
while ($row=<$in>){
	@tests=();
	($chr,$start,$end,$hits,$match,$rest)=split/\t/,$row;
	if ($chr =~ /chr(\d+)/){
		$chrom = $1;
		@matches=split/,/,$match;
		foreach $hit (@matches){
			if ($hit =~ /converted\_(.+)\.bed/){
				$test = $1;
				push @tests,$test;
			}
		}
		if ($hits == 1){
			print $bed1 "$chrom\t$start\t$end\t$test\n";
		}elsif ($hits < 3){
			$note=join('|',@tests);
			#print $bed2 "$chrom\t$start\t$end\t$note\n";
		}elsif ($hits > 2){
			$note=join('|',@tests);
			print $bed3 "$chrom\t$start\t$end\t$note\n";
		}
	}
}
close $bed1;
close $bed2;
close $bed3;
