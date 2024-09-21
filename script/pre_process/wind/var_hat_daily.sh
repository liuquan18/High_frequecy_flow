#!/bin/bash

# bandpass filter 2-12 days with cdo
module load cdo
module load parallel

var=$1 # zg, ua, va
period=$2 # first10, last10

from_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_global/${var}_MJJAS_${period}/
to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_global/${var}_MJJAS_${period}_hat/
tmp_dir=/scratch/m/m300883/${var}/bandpass/


mkdir -p ${to_path} ${tmp_dir}

export from_path to_path tmp_dir var


# function to band filter
Low_pass_filter(){
    infile=$1
    # basename without .nc
    fname=$(basename ${infile%.nc})
    outfile=${to_path}${fname}.nc

    # split years
    cdo -P 10 -splityear -del29feb ${infile} ${tmp_dir}${fname}_year
    # band filter, keep above 12 days 
    year_files=$(ls ${tmp_dir}${fname}_year*)
    cdo -O -P 10 -mergetime -apply,lowpass,30.5 [ ${year_files} ] ${outfile}
    # remove temporary files
    rm ${tmp_dir}${fname}_year*
}

export -f Low_pass_filter
# parallel band filter in to_dir
parallel --jobs 20 Low_pass_filter ::: ${from_path}*.nc
