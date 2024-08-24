#!/bin/bash

# bandpass filter 2-12 days with cdo
module load cdo
module load parallel

var=$1 # zg, ua, va
period=$2 # first10, last10

from_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_global/${var}_MJJAS_ano_${period}/
to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_global/${var}_MJJAS_ano_${period}_prime_veryhigh/
tmp_dir=/scratch/m/m300883/${var}/bandpass/


mkdir -p ${to_path} ${tmp_dir}

export from_path to_path tmp_dir var


# function to band filter
band_filter(){
    infile=$1
    # basename without .nc
    fname=$(basename ${infile%.nc})
    outfile=${to_path}${fname}.nc

    # split years
    cdo -P 10 -splityear -del29feb ${infile} ${tmp_dir}${fname}_year
    # band filter, keep 2-5 days 
    year_files=$(ls ${tmp_dir}${fname}_year*)
    cdo -O -P 10 -mergetime -apply,bandpass,73,182.5 [ ${year_files} ] ${outfile}
    # remove temporary files
    rm ${tmp_dir}${fname}_year*
}

export -f band_filter
# parallel band filter in to_dir
parallel --jobs 10 band_filter ::: ${from_path}*.nc
