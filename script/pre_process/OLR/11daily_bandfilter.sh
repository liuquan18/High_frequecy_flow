#!/bin/bash

# defind the path of the data
var=$1
tmp_dir="/scratch/m/m300883/OLR/bandpass/"
if [ $var == "first_OLR" ]; then
    echo "Processing OLR data of first10 years"
    base_dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/"
    from_dir=$base_dir"first10_OLR_daily_ano/"
    to_dir=$base_dir"first10_OLR_daily_ano_bandfilter/"

elif [ $var == "last_OLR" ]; then
    echo "Processing OLR data of last10 years"
    base_dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/"
    from_dir=$base_dir"last10_OLR_daily_ano/"
    to_dir=$base_dir"last10_OLR_daily_ano_bandfilter/"

elif [ $var == "first_zg" ]; then
    echo "Processing ZG data of first10 years"
    base_dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/daily/"
    from_dir=$base_dir"zg_MJJAS_ano_first10/"
    to_dir=$base_dir"zg_MJJAS_ano_first10_bandfilter/"

elif [ $var == "last_zg" ]; then
    echo "Processing ZG data of last10 years"
    base_dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/daily/"
    from_dir=$base_dir"zg_MJJAS_ano_last10/"
    to_dir=$base_dir"zg_MJJAS_ano_last10_bandfilter/"

else
    echo "Invalid input"
    exit 1

fi

export from_dir to_dir

# function to band filter
band_filter(){
    infile=$1
    # basename without .nc
    fname=$(basename ${infile%.nc})
    outfile=${to_dir}${fname}.nc

    # split years
    cdo -P 10 -splityear ${infile} ${tmp_dir}${fname}_year
    # band filter, keep 2-8 days 
    year_files=$(ls ${tmp_dir}${fname}_year*)
    cdo -O -P 10 -mergetime -apply,bandpass,45.625,182.5 [ ${year_files} ] ${outfile}
    # remove temporary files
    rm ${tmp_dir}${fname}_year*
}

export -f band_filter

# parallel band filter in to_dir
parallel --jobs 10 band_filter ::: ${from_dir}*.nc