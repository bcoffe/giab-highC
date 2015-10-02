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
	awk -v chr=$n '{where=match($1, chr); if (where) print $0}' ${f%.gz} >> temp.vcf || { echo "selecting $n chromosome did not work" 1>&2; exit;}
    done
    vcf-sort -c temp.vcf > ${f%.vcf.gz}.sort.vcf
    bgzip ${f%.vcf.gz}.sort.vcf
    tabix ${f%.vcf.gz}.sort.vcf.gz
    rm temp.vcf
    rm ${f%.gz}.vcf
elif [[ ${f%.gz} == *".bed" ]]
then
    for n in ${chroms[@]}
    do
	awk -v chr=$n '{where=match($1, chr); if (where) print $0}' ${f%.gz} | bedtools sort -i | bgzip -c> ${f%.bed}.sort.bed.gz || { echo "selecting $n chromosome did not work" 1>&2; exit;}
    done
    rm ${f%.gz}
    end="${f%$bed*}.sort.bed.gz"
else
    echo "File type not recognized"
fi
echo "Finished with $end"
done