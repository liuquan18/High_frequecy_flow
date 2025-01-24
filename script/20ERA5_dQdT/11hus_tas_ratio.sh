#!/bin/bash
module load cdo
module load parallel


read_daily_files() {
    local var=$1
    local daily_path=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/${var}_daily_std_mergeyear/
    local daily_file=E5pl00_1D*.nc
    daily_files=($(find $daily_path -name $daily_file -print))
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


# Generate hus daily files
read_daily_files hus 
echo Read daily hus files 
hus_daily_files=("${daily_files[@]}")
# sort the list
hus_daily_files=($(echo ${hus_daily_files[@]} | tr ' ' '\n' | sort -n))

# Generate tas daily files
read_daily_files "tas" 
echo Read daily tas files 
tas_daily_files=("${daily_files[@]}")
# sort the list
tas_daily_files=($(echo ${tas_daily_files[@]} | tr ' ' '\n' | sort -n))


echo calcualte hus/tas ratio 
# replace _ano with _ano_lowlevel
parallel --link --jobs 5 ratio {1} {2} ::: ${hus_daily_files[@]} ::: ${tas_daily_files[@]} 