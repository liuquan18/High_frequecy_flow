#!/bin/bash
module load cdo
module load parallel

member=$1

read_daily_files() {
    local var=$1
    local member=$2
    local daily_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily/r${member}i1p1f1/
    daily_files=($(find $daily_path -name *.nc -print))
}

ratio(){
    local husfile=$1
    local tasfile=$2
    local outfile=${husfile//hus/hus_tas}
    echo "Calculating ratio for $husfile and $tasfile"
    cdo -P 10 -div -mulc,1000 $husfile $tasfile $outfile # change from kg/kg to g/kg
}

export -f ratio 
export -f read_daily_files

# mkdir to path
mkdir -p /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_tas_prime_daily/r${member}i1p1f1/


# Generate hus daily files
read_daily_files hus_prime $member
echo Read daily hus files for member $member
hus_daily_files=("${daily_files[@]}")
# sort the list
hus_daily_files=($(echo ${hus_daily_files[@]} | tr ' ' '\n' | sort -n))

# Generate tas daily files
read_daily_files tas_prime $member
echo Read daily tas files for member $member
tas_daily_files=("${daily_files[@]}")
# sort the list
tas_daily_files=($(echo ${tas_daily_files[@]} | tr ' ' '\n' | sort -n))


echo calcualte hus/tas ratio for member $member
# replace _ano with _ano_lowlevel
parallel --link --jobs 5 ratio {1} {2} ::: ${hus_daily_files[@]} ::: ${tas_daily_files[@]} 