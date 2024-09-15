#!/bin/bash
# subtract the ensemble mean of the monthly data from the daily data using cdo monsub
module load cdo
module load parallel
var=$1 # zg, ua, va

from_path=/work/ik1017/CMIP6/data/CMIP6/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/ssp585/
to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_global/${var}_MJJAS_last10/
tmp_path=/scratch/m/m300883/${var}_daily_global_noano/

mkdir -p ${to_path} ${tmp_path}

export from_path to_path tmp_path var

# function to merge the daily data
Merge(){
    member=$1

    dailyfile1=$(find ${from_path}r${member}i1p1f1/day/ -name ${var}'_day_MPI-ESM1-2-LR_ssp585_r'${member}'i1p1f1_gn_20750101-20941231.nc')
    dailyfile2=$(find ${from_path}r${member}i1p1f1/day/ -name ${var}'_day_MPI-ESM1-2-LR_ssp585_r'${member}'i1p1f1_gn_20950101-21001231.nc')

    # merge the two daily files
    cdo -O -mergetime -selyear,2091/2094 $dailyfile1 -selyear,2095/2100 $dailyfile2 ${tmp_path}${var}_day_MPI-ESM1-2-LR_ssp585_r${member}i1p1f1_gn_20910101-21001231.nc

}

# define function called Anomaly
Softlink() {

    member=$1
    echo $member

    # merge the daily data
    Merge $member

    # calculate the anomaly
    dailyfile=${tmp_path}${var}_day_MPI-ESM1-2-LR_ssp585_r${member}i1p1f1_gn_20910101-21001231.nc
    tofile=${to_path}${var}_day_MPI-ESM1-2-LR_ssp585_r${member}i1p1f1_gn_20910501-21000931.nc
    # include month Mayb and september for later rolling window
    cdo -sellevel,100000,85000,70000,50000,25000 -selmonth,5/9 -selyear,2091/2100 $dailyfile \
        ${tofile}
}

export -f Merge Softlink

parallel --jobs 10 Softlink ::: {1..50}]