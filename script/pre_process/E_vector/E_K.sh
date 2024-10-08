#!/bin/bash

# bandpass filter 2-12 days with cdo
module load cdo
module load parallel

period=$1 # first10, last10
frequency=$2 # prime, prime_veryhigh, prime_intermedia

# u prime and v prime path
uprime_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_ano_${period}_${frequency}/
vprime_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_MJJAS_ano_${period}_${frequency}/

to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_K_daily_global/E_K_MJJAS_ano_${period}_${frequency}/
# mf: momentum fluxes

mkdir -p ${to_path}

export uprime_path vprime_path to_path

K_component(){

    member=$1
    ufile=$(find ${uprime_path} -name ua_*r${member}i1p1f1_gn_*.nc)
    vfile=$(find ${vprime_path} -name va_*r${member}i1p1f1_gn_*.nc)

    # basename without .nc
    ufname=$(basename ${ufile%.nc})
    outfile=${to_path}E_K_${ufname:3}.nc

    cdo -O -P 10 -divc,2 -add -mul ${ufile} ${ufile} -mul ${vfile} ${vfile} ${outfile}
}

export -f K_component

# parallel K_component for all members
parallel --jobs 10 K_component ::: {1..50}