#!/bin/bash
#Only show positions where there is low confidence, filter out variant calls, create tab file
awk '(NF > 3){n=split($4,files,","); if (n < 3) print $1"\t"$3"\t"$4}' vcfnbed_scored.sort.bed | grep "vc" | cut -f1,2 > vcfnbed_lowconf.tab

#Use vcftools to isolate only the sites we want
files=( ../VCF/phasing_annotated-with-PHQ_NA12878.sort.vcf.gz ../VCF/NISTIntegratedCalls_14datasets_131103_allcall_UGHapMerge_HetHomVarPASS_VQSRv2.19_2mindatasets_5minYesNoRatio_all_nouncert_excludesimplerep_excludesegdups_excludedecoy_excludeRepSeqSTRs_noCNVs.sort.vcf.gz ../VCF/NA12878.sort.vcf.gz ); for f in ${files[@]}; do name=${f##*/}; vcftools --gzvcf $f --positions vcfnbed_lowconf.tab --recode --recode-INFO-all --stdout | bgzip -c> ${name%.sort*}_lowconf.vcf.gz; done

#Each file has its own data so each file was sorted separately.
bcftools query -f '%CHROM\t%POS\t%QUAL\t%FILTER\t%ID\t%TYPE\t[%TGT]\n' NA12878_lowconf.vcf.gz |awk '{print "Platinum\t"$0}'>> vcfnbed_lowconf.tsv

bcftools query -f '%CHROM\t%POS\t%QUAL\t%FILTER\t%ID\t%TYPE\t[%TGT\t%DP\t%GQ\t%RQ]\t%INFO/AVR\n' phasing_annotated-with-PHQ_NA12878_lowconf.vcf.gz |awk '{print "RTG\t"$0}'>> vcfnbed_lowconf.tsv

bcftools query -f '%CHROM\t%POS\t%QUAL\t%FILTER\t%ID\t%TYPE\t[%TGT\t%DP\t%GQ]\t \t \t%INFO/PLminsumOverDP\t%INFO/filter\t%INFO/platforms\n' NISTIntegratedCalls_14datasets_131103_allcall_UGHapMerge_HetHomVarPASS_VQSRv2.19_2mindatasets_5minYesNoRatio_all_nouncert_excludesimplerep_excludesegdups_excludedecoy_excludeRepSeqSTRs_noCNVs_lowconf.vcf.gz|awk '{print "GIAB\t"$0}'>> vcfnbed_lowconf.tsv

#Sort by chromosome and then position (for uniformity's sake) and remove repeat reads (RTG has exact repeats)
sort -k2,2d -k3,3n vcfnbed_lowconf.tsv |uniq > vcfnbed_lowconf.sort.tsv

#Separate files by quality
awk '{if ($4 >= 200 || $4 = 0) print $0}' vcfnbed_lowconf.sort.tsv > vcfnbed_lowconf_highqual.sort.tsv
awk '{if ($4 < 200) print $0}' vcfnbed_lowconf.sort.tsv > vcfnbed_lowconf_lowqual.sort.tsv 

##Create file comparing disagreeing variant calls
#Example of annotating vcf files to contain intersect data
grep "vc" vcfnbed_scored.sort.bed | cut -f1,3,4 > vcfnbed_anno
vcf-sort vcfnbed_anno > vcfnbed_anno.sort
bgzip vcfnbed_anno.sort
tabix -s 1 -b 2 vcfnbed_anno.sort.gz
zcat NISTIntegratedCalls_14datasets_131103_allcall_UGHapMerge_HetHomVarPASS_VQSRv2.19_2mindatasets_5minYesNoRatio_all_nouncert_excludesimplerep_excludesegdups_excludedecoy_excludeRepSeqSTRs_noCNVs.sort.vcf.gz | vcf-annotate -a ../Process/vcfnbed_anno.sort.gz -d key=INFO,ID=INTER,Number=A,Type=String,Description="All intersecting files at this position" -c CHROM,POS,INFO/INTER |bgzip -c> NISTIntegratedCalls_14datasets_131103_allcall_UGHapMerge_HetHomVarPASS_VQSRv2.19_2mindatasets_5minYesNoRatio_all_nouncert_excludesimplerep_excludesegdups_excludedecoy_excludeRepSeqSTRs_noCNVs_anno.sort.vcf.gz

#Pull quality info from each file
bcftools query -f '%CHROM\t%POS\t%QUAL\t%FILTER\t%ID\t%TYPE\t%INFO/INTER\t[%TGT\t%DP\t%GQ\t \t \t]%INFO/PLminsumOverDP\t%INFO/filter\t%INFO/platforms\n' NISTIntegratedCalls_14datasets_131103_allcall_UGHapMerge_HetHomVarPASS_VQSRv2.19_2mindatasets_5minYesNoRatio_all_nouncert_excludesimplerep_excludesegdups_excludedecoy_excludeRepSeqSTRs_noCNVs_anno.sort.vcf.gz | awk '{print "GIAB\t"$0}' >> ../Process/vcfnbed_inter.tsv

bcftools query -f '%CHROM\t%POS\t%QUAL\t%FILTER\t%ID\t%TYPE\t%INFO/INTER\t[%TGT\t%DP\t%GQ\t%RQ]\t%INFO/AVR\n' phasing_annotated-with-PHQ_NA12878_anno.sort.vcf.gz |awk '{print "RTG\t"$0}' >> ../Process/vcfnbed_inter.tsv

bcftools query -f '%CHROM\t%POS\t%QUAL\t%FILTER\t%ID\t%TYPE\t%INFO/INTER\t[%TGT]\n' NA12878_anno.sort.vcf.gz |awk '{print "Platinum\t"$0}' >> ../Process/vcfnbed_inter.tsv

#Sort and remove repeats
sort -k2,2d -k3,3n ../Process/vcfnbed_inter.tsv |uniq > ../Process/vcfnbed_inter.sort.tsv

#Compare by chr and pos, and then by genotype
perl ~/Documents/giab/vcfnbed.pl vcfnbed_inter.sort.tsv
