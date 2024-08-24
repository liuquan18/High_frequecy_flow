#!/bin/bash

# bandpass filter 2-12 days with cdo
module load cdo
module load parallel

period=$1 # first10, last10
frequency=$2 # prime, prime_veryhigh, prime_intermedia

# u prime and v prime path
uprime_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_ano_${period}_${frequency}/
vprime_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_MJJAS_ano_${period}_${frequency}/

to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/momenturm_fluxes/momenturm_fluxes_${frequency}_${period}/

mkdir -p ${to_path}

export uprime_path vprime_path to_path

# function to calculate high frequency momentum fluxes
Momentum(){
    member=$1
    ufile=$(find ${uprime_path} -name ua_*r${member}i1p1f1_gn_*.nc)
    vifle=$(find ${vprime_path} -name va_*r${member}i1p1f1_gn_*.nc)
    # basename without .nc
    ufname=$(basename ${ufile%.nc})
    vfname=$(basename ${vfile%.nc})
    outfile=${to_path}momentum_fluxes_${ufname:3}.nc

    cdo -O -P 10 -mul ${ufile} ${vfile} ${outfile}
}

export -f Momentum

# parallel Momentum for all members

parallel --jobs 10 Momentum ::: {1..50}