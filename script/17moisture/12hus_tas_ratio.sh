#!/bin/bash
moduel load cdo
module load parallel

member=$1

read_daily_files() {
    local var=$1
    local member=$2
    local daily_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_std/r${member}i1p1f1/
    local daily_file=${var}_day_MPI-ESM1-2-LR_rr${member}i1p1f1_gn_*.nc
    daily_files=($(find $daily_path -name $daily_file -print))
}



# Generate hus daily files
read_daily_files "hus" $member
echo Read daily hus files for member $member
hus_daily_files=("${daily_files[@]}")

# Generate tas daily files
read_daily_files "tas" $member
echo Read daily tas files for member $member
tas_daily_files=("${daily_files[@]}")


echo calcualte hus/tas ratio for member $member
# replace _ano with _ano_lowlevel
outfile=${husfile//hus/hus_tas}
cdo -P 10 div $husfile $tasfile $outfile