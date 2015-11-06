#!/bin/bash

files=( "$@" )
chroms=( {1..22} X Y M )
for f in ${files[@]}
do
echo "Cleaning up $f"
if [[ $f == *".gz" ]]
then
    bgzip -d $f
fi
sed -i 's/chr//' ${f%.gz} || { echo "removing chr did not work" 1>&2; exit;}
sed -i 's/MT/M/' ${f%.gz} || { echo "replacing MT did not work" 1>&2; exit;}
if [[ ${f%.gz} == *".vcf" ]]
then
    sed -i 's/Flag/String/g' ${f%.gz} || { echo "replacing Flag did not work" 1>&2; exit;}
    grep "#" ${f%.gz} > temp.vcf
    for n in ${chroms[@]}
    do
	awk -v chr=$n '{if ($1 == chr) print $0}' ${f%.gz} >> temp.vcf || { echo "selecting $n chromosome did not work" 1>&2; exit;}
    done
    vcf-sort -c temp.vcf > ${f%.vcf*}.sort.vcf
    bgzip ${f%.vcf*}.sort.vcf
    tabix ${f%.vcf*}.sort.vcf.gz
    rm temp.vcf
    rm ${f%.vcf*}.vcf
    end="${f%.vcf*}.sort.vcf.gz"
elif [[ ${f%.gz} == *".bed" ]]
then
    for n in ${chroms[@]}
    do
	awk -v chr=$n '{if ($1 == chr) print $0}' ${f%.gz} >> temp.bed || { echo "selecting $n chromosome did not work" 1>&2; exit;}
    done
    bedtools sort -i temp.bed > ${f%.bed*}.sort.bed || { echo "sort did not work" 1>&2; exit;}
    bgzip ${f%.bed*}.sort.bed || { echo "bgzip did not work" 1>&2; exit;}
    rm ${f%.gz}
    rm temp.bed
    end="${f%.bed*}.sort.bed.gz"
else
    echo "File type not recognized"
fi
echo "Finished with $end"
done
