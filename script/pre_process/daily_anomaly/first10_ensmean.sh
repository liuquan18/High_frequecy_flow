#!/bin/bash

module load cdo
module load parallel

base_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vt_daily/
file_name=vt_day_MPI-ESM1-2-LR_r*_gn_18500501-18590930.nc

# Save the find command output to first_ens_list
first_ens_list=($(find $base_path -name $file_name -print))


cdo -ensmean -apply,ymonmean [ ${first_ens_list[@]} ] /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/vt_monthly_ensmean/first10_vt_monthly_ymonmean_ensmean.nc