#!/bin/bash

files=( "$@" )
chroms=( {1..22} X Y M )
bed=".bed"
vcf=".vcf"
for f in ${files[@]}
do
echo "Cleaning up $f"
if [[ $f == *".gz" ]]
then
    if [[ $f == *".bed.gz" ]]
    then
	bgzip -d $f
	sed -i 's/chr//' ${f%.gz} || { echo "removing chr did not work" 1>&2; exit;}
	sed -i 's/MT/M/' ${f%.gz} || { echo "replacing MT did not work" 1>&2; exit;}
	for n in ${chroms[@]}
	do
	    grep -v "track" ${f%.gz} |awk -v chr=$n '{where=match($1, chr); if (where) print $0}' >> temp.bed || { echo "selecting $n chromosome did not work" 1>&2; exit;}
	done
	bedtools sort -i temp.bed |bgzip -c> ${f%$bed*}.sort.bed || { echo "sort did not work" 1>&2; exit;}
	bgzip ${f%$bed*}.sort.bed
	rm temp.bed
	end="${f%$bed*}.sort.bed.gz"
    elif [[ $f == *".vcf.gz" ]]
    then
	zcat $f | sed 's/chr//' > temp.vcf || { echo "removing chr did not work" 1>&2; exit;}
	sed -i 's/MT/M/' temp.vcf || { echo "replacing MT did not work" 1>&2; exit;}
	sed -i 's/Flag/String/g' temp.vcf || { echo "replacing Flag did not work" 1>&2; exit;}
	grep "#" temp.vcf > ${f%$vcf*}.vcf
	for n in ${chroms[@]}
	do
	   grep -v "#" temp.vcf| awk -v chr=$n '{where=match($1, chr); if (where) print $0}' >> ${f%$vcf*}.vcf || { echo "selecting $n chromosome did not work" 1>&2; exit;}
	done
	vcf-sort -c ${f%$vcf*}.vcf > ${f%$vcf*}.sort.vcf
	bgzip ${f%$vcf*}.sort.vcf
	tabix ${f%$vcf*}.sort.vcf.gz
	rm temp.vcf
	end="${f%$vcf*}.sort.vcf.gz"
     else
	echo "File type not recognized"
     fi

else
    if [[ $f == *".bed" ]]
    then
	sed -i 's/chr//' $f || { echo "removing chr did not work" 1>&2; exit;}
	sed -i 's/MT/M/' $f || { echo "replacing MT did not work" 1>&2; exit;}
	for n in ${chroms[@]}
	do
	    grep -v "track" $f | awk -v chr=$n '{ where=match($1, chr); if (where) print $0}'>> temp.bed || { echo "selecting $n chromosome did not work" 1>&2; exit;}
	done
	bedtools sort -i temp.bed > sort.bed
	mv sort.bed ${f%$bed}.sort.bed
	end="${f%$bed}.sort.bed"
    elif [[ $f == *".vcf" ]]
    then
	sed -i 's/chr//' $f || { echo "removing chr did not work" 1>&2; exit;}
	sed -i 's/MT/M/' $f || { echo "replacing MT did not work" 1>&2; exit;}
	sed -i 's/Flag/String/g' $f || { echo "replacing Flab did not work" 1>&2; exit;}
	grep "#" $f > ${f%$vcf}_temp.vcf
	for n in ${chroms[@]}
	do
	   grep -v "#" $f | awk -v chr=$n '{ where=match($1, chr); if (where) print $0}' >> ${f%$vcf}_temp.vcf || { echo "selecting $n chromosome did not work" 1>&2; exit;}
	done
	vcf-sort ${f%$vcf}_temp.vcf > ${f%$vcf}_sort.vcf 
	mv ${f%$vcf}_sort.vcf ${f%$vcf}.vcf
	end="${f%$vcf}.vcf"
    else
	echo "File type not recognized"
    fi
fi
echo "Finished with $end"
done
