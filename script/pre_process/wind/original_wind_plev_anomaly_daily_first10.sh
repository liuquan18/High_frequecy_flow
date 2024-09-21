#!/bin/bash
# softlink the data to new location
module load cdo
module load parallel
var=$1 # zg, ua, va

from_path=/pool/data/CMIP6/data/CMIP/MPI-M/MPI-ESM1-2-LR/historical/
to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_global/${var}_MJJAS_first10/

mkdir -p ${to_path}

export from_path
export to_path
export var

# define function called Anomaly
Softlink() {

    member=$1
    echo $member

    dailyfile=$(find ${from_path}r${member}i1p1f1/day/${var}/gn/ -name ${var}_day_MPI-ESM1-2-LR_historical_r${member}i1p1f1_gn_18500101-18691231.nc)
    
    # select the first 10 years
    tofile=${to_path}${var}_day_MPI-ESM1-2-LR_historical_r${member}i1p1f1_gn_18500501-18590931.nc
    cdo -sellevel,100000,85000,70000,50000,25000 -selmonth,5/9 -selyear,1850/1859 $dailyfile \
        ${tofile}   

}

export -f Softlink
parallel --jobs 10 Softlink ::: {1..50}