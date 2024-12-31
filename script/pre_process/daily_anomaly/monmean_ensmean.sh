#!/bin/bash

module load cdo
module load parallel

decade=$1 # 1850, node
var=$2


base_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily/
to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_monthly_ensmean/
mkdir -p $to_path

file_name=${var}_day_MPI-ESM1-2-LR_r*_gn_${decade}*.nc
out_name=${var}_monmean_ensmean_${decade}05_$((${decade}+9))09.nc


# Save the find command output to first_ens_list
first_ens_list=($(find $base_path -name $file_name -print))


cdo -P 16 -ensmean -apply,ymonmean [ ${first_ens_list[@]} ] $to_path${out_name}
