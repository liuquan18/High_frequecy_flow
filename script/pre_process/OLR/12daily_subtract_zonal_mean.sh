#!/bin/bash
module load cdo
module load parallel

period=$1

daily_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/${period}_OLR_daily_ano/

to_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/${period}_OLR_daily_ano_subzonalmean/


export daily_dir to_dir

sub_zonal_mean() {
    infile=$1
    fname=$(basename ${infile%.nc})
    outfile=${to_dir}${fname}_subzonalmean.nc
    cdo -P 10 -sub ${infile} -enlarge,${infile} -zonmean ${infile} ${outfile}
}

export -f sub_zonal_mean

parallel --jobs 10 sub_zonal_mean ::: ${daily_dir}*.nc