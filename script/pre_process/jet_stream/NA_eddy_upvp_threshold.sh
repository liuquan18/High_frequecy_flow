#!/bin/bash
module load cdo

period=$1

from_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_${period}/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_threshold/
tmp_dir=/scratch/
mkdir -p ${to_dir}

all_files=$(ls ${from_dir}*.nc)

cdo -ensmean -apply,timstd [ ${all_files[@]} ] ${to_dir}NA_eddy_upvp_${period}_threshold.nc