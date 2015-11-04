#!/bin/perl

use Vcf;
use List::MoreUtils qw(uniq);

@files=@ARGV;
@files2=@ARGV;
chomp @files;
@chroms=(1..22,X,Y,M);
foreach $file (@files){
	if ($file =~ /(.*\/)*(.+)\.sort\.vcf.*/g){$jack = $2;}
	push (@sample_names,$jack);
	$vcf = Vcf->new(file=>"$file");
	$vcf->parse_header();
	@snheaders = split/\n/,$vcf->format_header();
	foreach $header (@snheaders){
		if ($header =~ /(##INFO=<ID=.+Number=).+/){
			$info_header = $1;
			if ($info_header ~~ @IDs){}else{
				push @IDs,$info_header;
				chomp $header;
				push @allheaders,$header;
			}
		}elsif($header =~ /(##FORMAT=<ID=.+Number=).+/){
			$format_header = $1;
			if ($format_header ~~ @IDs){}else{
				push @IDs,$format_header;
				chomp $header;
				push @allheaders,$header;
			}
		}
	}
}
$name="";
$samples=join("\t",@sample_names); $date = qx{date};
print "##fileformat=VCFv4.1\n##FILTER=<ID=PASS,Description=\"All filters passed\">\n##fileDate=$date##source=JHITZ\n##reference=hg19\n";
foreach $header (@allheaders){print "$header\n";}
print "##contig=<ID=1,length=249250621>\n##contig=<ID=2,length=243199373>\n";
print "##contig=<ID=3,length=198022430>\n##contig=<ID=4,length=191154276>\n##contig=<ID=5,length=180915260>\n##contig=<ID=6,length=171115067>\n";
print "##contig=<ID=7,length=159138663>\n##contig=<ID=8,length=146364022>\n##contig=<ID=9,length=141213431>\n##contig=<ID=10,length=135534747>\n##contig=<ID=11,length=135006516>\n";
print "##contig=<ID=12,length=133851895>\n##contig=<ID=13,length=115169878>\n##contig=<ID=14,length=107349540>\n##contig=<ID=15,length=102531392>\n";
print "##contig=<ID=16,length=90354753>\n##contig=<ID=17,length=81195210>\n##contig=<ID=18,length=78077248>\n##contig=<ID=19,length=59128983>\n";
print "##contig=<ID=20,length=63025520>\n##contig=<ID=21,length=48129895>\n##contig=<ID=22,length=51304566>\n##contig=<ID=X,length=155270560>\n";
print "##contig=<ID=M,length=16569>\n##contig=<ID=Y,length=59373566>\n";
print "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t$samples\n";
foreach $c (@chroms){
	%hash=();
foreach $file (@files2){
	if ($file =~ /(.*\/)*(.+)\.sort\.vcf.*/g){$name = $2;}
	$vcf = Vcf->new(file=>"$file", region=>$c);
	$vcf->parse_header();
	while ($x = $vcf->next_data_array()){
		@alts = split/,/,$$x[4];
		$geno{0}=$$x[3];
		$i = 1;
		foreach $al (@alts){
			$geno{$i}=$al;++$i;
			push(@{$hash{$$x[0]}{$$x[1]}{$$x[3]}{ALT}},$al);
		}
		@uniq_alts= uniq @{$hash{$$x[0]}{$$x[1]}{$$x[3]}{ALT}};
		@{$hash{$$x[0]}{$$x[1]}{$$x[3]}{ALT}} = @uniq_alts;
		@SAMPLE=split/:/,$$x[9];
		($GT1,$GT2)=split/[\/\|]+/,$SAMPLE[0];
		$hash{$$x[0]}{$$x[1]}{$$x[3]}{SAMPLE}{$name}{TGT}="$geno{$GT1}\/$geno{$GT2}";
		push(@{$hash{$$x[0]}{$$x[1]}{$$x[3]}{QUAL}},$$x[5]);
		#push(@{$hash{$$x[0]}{$$x[1]}{$$x[3]}{SAMPLE}{$name}{FILTER}},"$name($$x[6])");
		@INFORMs=split/;/,$$x[7];
		foreach $INFORM (@INFORMs){push(@{$hash{$$x[0]}{$$x[1]}{$$x[3]}{INFO}},"$name:$INFORM");}
		@FORMAT=split/:/,$$x[8]; 
		for ($k = 1; $k <= $#FORMAT; ++$k){
			$hash{$$x[0]}{$$x[1]}{$$x[3]}{SAMPLE}{$name}{$FORMAT[$k]}=$SAMPLE[$k];
		}		
	}
}


foreach $chr (@chroms){
	@positions = sort {$a <=> $b} keys %{$hash{$chr}};
	foreach $pos (@positions){
		@formats=(); %geno=();
		foreach $ref (keys %{$hash{$chr}{$pos}}){
			$format_field="GT";
			$alt=join(',',@{$hash{$chr}{$pos}{$ref}{ALT}});
			$sum =0; $total=0;
			foreach $qual (@{$hash{$chr}{$pos}{$ref}{QUAL}}){$sum += $qual; ++$total;}
			if ($total > 0){$avgqual = $sum / $total;}else{$avgqual='.';}
			$info = join(';',@{$hash{$chr}{$pos}{$ref}{INFO}});
			print "$chr\t$pos\t\.\t$ref\t$alt\t$avgqual\t\.\t$info\t";
			foreach $sample (sort keys %{$hash{$chr}{$pos}{$ref}{SAMPLE}}){
				foreach $format (keys %{$hash{$chr}{$pos}{$ref}{SAMPLE}{$sample}}){
					push (@formats,$format);
					@uniq_formats=uniq @formats; 
					@formats = @uniq_formats;
				}
				
			}
			foreach $format (@formats){$format_field = $format_field . ":$format";}
			print "$format_field";
			foreach $sample (split/\t/,$samples){
				if (defined $hash{$chr}{$pos}{$ref}{SAMPLE}{$sample}{TGT}){
					($GT1,$GT2)=split/[\/\|]+/,$hash{$chr}{$pos}{$ref}{SAMPLE}{$sample}{TGT};
				}else{$GT1='.';$GT2='.';}
				$geno{$ref}= "0"; $i = 1;$geno{'.'}='.';
				foreach $alter (split/,/,$alt){$geno{$alter}=$i; ++$i;}
				$sample_field="$geno{$GT1}\/$geno{$GT2}";
				if (defined $hash{$chr}{$pos}{$ref}{SAMPLE}{$sample}){
					@formt = split/:/,$format_field;
					foreach $form (@formt[1..$#formt]){
						if (defined $hash{$chr}{$pos}{$ref}{SAMPLE}{$sample}{$form}){
							$sample_field = $sample_field . ":$hash{$chr}{$pos}{$ref}{SAMPLE}{$sample}{$form}";
						}else{
							$sample_field = $sample_field . ':.';
						}
					}
				}
				print "\t$sample_field";
			}
			
		} print "\n";
	}
}}
