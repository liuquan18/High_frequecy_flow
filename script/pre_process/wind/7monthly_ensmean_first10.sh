#!/bin/bash

module load cdo
module load parallel    

var=$1 # zg, ua, va
# define base path
base_path=/work/ik1017/CMIP6/data/CMIP6/CMIP/MPI-M/MPI-ESM1-2-LR/historical/
to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_season_global/

mkdir -p ${to_path}

export base_path
export to_path


# Create file lists with ensemble members ranging from 1 to 50
for member in {1..50}; do
    # Use find to resolve the wildcard into real paths
    files=$(find ${base_path}r${member}i1p1f1/Amon/${var}/gn/ -name ${var}_Amon_MPI-ESM1-2-LR_historical_r${member}i1p1f1_gn_185001-186912.nc)
    for file in $files; do
        file_list+="$file "
    done
done

# Remove the trailing space
file_list=$(echo $file_list | sed 's/ $//')

cdo -selmon,5/9 -ensmean -apply,-selyear,1850/1859 [ "${file_list[@]}" ] ${to_path}"${var}_Amon_MPI-ESM1-2-LR_HIST_ensmean_185005-185909.nc"