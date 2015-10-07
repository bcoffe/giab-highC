#!/bin/perl

open $in,"<",$ARGV[0];
open $out,">",'/mnt/hgfs/VCF/GIAB/Process/vcfnbed_inter_nomatch.sort.tsv';
print $out "File\tCHR\tPOS\tQUAL\tFILTER\tID\tVariant\tMatches\tGenotype\tDepth\tGenoQual\tRTG Qual\tAVR\tPLoverDP\tNISTfilter\tNISTplatforms\tObservations\n";
ROWS:while ($row = <$in>){
	($file,$chr,$pos,$qual,$filter,$id,$var,$matches,$gt,$DP,$GQ,$RQ,$AVR,$PLoverDP,$NISTfilter,$platforms)=split/\t/,$row;
	($GT1,$GT2)=split/[\/\|]+/,$gt;
	if ($GT1 eq $GT2){next ROWS;}
	chomp $GT1;
	chomp $GT2;
	$position="$chr\t$pos";
	$geno1 = "$GT1\t$GT2";
	$geno2 = "$GT2\t$GT1";
	if ($position eq $prevposition){
		if (($geno1 eq $prevgeno1) || ($geno1 eq $prevgeno2)){
			#print "MATCH!\n$row\n$geno1\t$geno2\n$prevrow\n$prevgeno1\t$prevgeno2\n";
			$prevrow=$row;
		}else{
			print $out "$row$prevrow\n";
			$prevgeno1=$geno1; $prevgeno2=$geno2;$prevrow=$row;
		}
	}else{
		$prevposition=$position; $prevgeno1=$geno1; $prevgeno2=$geno2; $prevrow=$row;
	}
	
}
