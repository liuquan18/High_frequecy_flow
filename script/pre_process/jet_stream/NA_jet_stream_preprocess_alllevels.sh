#!/bin/bash

# The resulting field is then zonally averaged over a\
# longitudinal sector (0–60 W for the North Atlantic),\
# neglecting windspoleward of 75 and equatorward of 15 .

# The resulting field is then low-pass filtered to remove variability on time scales shorter than 10 days.
module load cdo
module load parallel


period=$1
var=ua #zonal wind

basedir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_global/${var}_MJJAS_${period}/
to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/NA_jet_stream/jet_stream_allplev_${period}/
tmp_dir=/scratch/m/m300883/${var}/jet_stream_allplev/
tmp_mean_dir=/scratch/m/m300883/${var}/jet_stream_mean_allplev/

mkdir -p ${to_path} ${tmp_dir} ${tmp_mean_dir}

export basedir to_path var tmp_dir tmp_mean_dir

# function to band filter
Lowpass(){
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


Jetstream(){
    member=$1
    echo $member

    dailyfile=$(find ${basedir} -name ${var}_day*r${member}i1p1f1*.nc)

    filename=$(basename $dailyfile)
    # replace $var with jet_stream
    filename=${filename/$var/jet_stream}

    cdo -zonmean -sellonlatbox,-60,0,15,75 $dailyfile ${tmp_mean_dir}${filename}

    Lowpass ${tmp_mean_dir}${filename} 
}

export -f Jetstream Lowpass

parallel --jobs 10 Jetstream ::: {1..50}