#!/bin/bash
# subtract the ensemble mean of the monthly data from the daily data using cdo monsub
module load cdo
module load parallel
var=$1 # zg, ua, va

from_path=/pool/data/CMIP6/data/CMIP/MPI-M/MPI-ESM1-2-LR/historical/
to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_global/

mkdir -p ${to_path}

export from_path
export to_path
export var

# define function called Anomaly
Anomaly() {

    member=$1
    echo $member

    dailyfile=$(find ${from_path}r${member}i1p1f1/day/${var}/gn/ -name ${var}_day_MPI-ESM1-2-LR_historical_r${member}i1p1f1_gn_18500101-18691231.nc)
    monthlyfile=$(find /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_season_global/ -name ${var}_*_185005-185909.nc)
    anomalyfile=${to_path}${var}_day_MPI-ESM1-2-LR_historical_r${member}i1p1f1_gn_18500501-18590931_ano.nc
    # include month Mayb and september for later rolling window
    cdo -monsub -sellevel,100000,85000,70000,50000,25000 -selmonth,5/9 -selyear,1850/1859 $dailyfile \
        -sellevel,100000,85000,70000,50000,25000 $monthlyfile \
        ${anomalyfile}
}

export -f Anomaly
parallel --jobs 20 Anomaly ::: {1..50}