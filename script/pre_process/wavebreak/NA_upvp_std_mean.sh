#!/bin/bash
# bandpass filter 2-12 days with cdo
module load cdo
module load parallel

period=first10


wb_index_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_${period}/

to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_threshold/


mkdir -p ${to_path}

files=$(find ${wb_index_path} -name wb_index_*.nc)


cdo -P 10 -ensmean -apply,ydaystd [ ${files} ] ${to_path}NA_eddy_upvp_${period}_std.nc
cdo -P 10 -ensmean -apply,ydaymean [ ${files} ] ${to_path}NA_eddy_upvp_${period}_mean.nc