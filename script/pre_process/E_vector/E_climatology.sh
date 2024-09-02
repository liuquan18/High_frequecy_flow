#!/bin/bash

# bandpass filter 2-12 days with cdo
module load cdo
module load parallel

period=$1 # first10, last10
frequency=$2 # prime, prime_veryhigh, prime_intermedia
component=$3 # E_M, E_N

# E_M and E_N path
E_com_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${component}_daily_global/${component}_MJJAS_ano_${period}_${frequency}/

to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_climatology/${component}_climatology_${period}_${frequency}/

mkdir -p ${to_path}


# function to calculate E
E_c_files=$(find ${E_com_path} -name ${component}_*.nc)

cdo -ensmean -apply,-timmean [ $E_c_files ] ${to_path}${component}_climatology_${period}_${frequency}.nc