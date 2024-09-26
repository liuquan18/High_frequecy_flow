#!/bin/bash
module load cdo
module load parallel

period=$1
var=E_N # upvp

basedir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/E_N_MJJAS_${period}_prime/
to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/NA_eddy_upvp_${period}/

mkdir -p ${to_path} ${tmp_dir}

export basedir to_path var tmp_dir

infile=*_r*i1p1f1_gn_*.nc
# selelct the region of interest based on Coumou's paper
find $basedir -name $infile | parallel --jobs 10 --eta cdo -fldmean -sellonlatbox,-100,-10,30,60 -vertmean -sellevel,100000,85000,70000 {} ${to_path}{/}