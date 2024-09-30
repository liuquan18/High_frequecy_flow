#!/bin/bash

module load cdo
module load parallel

period=$1

non_std_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_${period}/
std_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_${period}_std/
tmp_path=/scratch/m/m300883/NA_eddy_upvp_${period}/

mkdir -p ${std_path} ${tmp_path}

export std_path non_std_path tmp_path

# function to standarize

standarize(){
    infile=$1
    # basename without .nc
    fname=$(basename ${infile%.nc})
    outfile=${std_path}${fname}.nc

    mean_file=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_threshold/NA_eddy_upvp_first10_mean.nc
    std_file=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_threshold/NA_eddy_upvp_first10_std.nc

    cdo -P 10 -O -ydaysub ${infile} ${mean_file} ${tmp_path}${fname}.nc
    cdo -P 10 -O -ydaydiv ${tmp_path}${fname}.nc ${std_file} ${outfile}
}

export -f standarize
# parallel standarize in to_dir
find ${non_std_path} -name "*.nc" | parallel --jobs 10 standarize