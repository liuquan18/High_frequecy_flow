#!/bin/bash
# subtract the ensemble mean of the monthly data from the daily data using cdo monsub
module load cdo
module load parallel

# define function called Anomaly
Anomaly() {

    member=$1
    echo $member

    # mergetime of daily data for the last 10 years
    cdo -O -sellevel,100000,85000,70000,50000,25000 -selmonth,5,6,7,8,9 -selyear,2091/2100 -mergetime /pool/data/CMIP6/data/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/ssp585/r${member}i1p1f1/day/zg/gn/v????????/zg_day_MPI-ESM1-2-LR_ssp585_r${member}i1p1f1_gn_20750101-20941231.nc /pool/data/CMIP6/data/ScenarioMIP/MPI-M/MPI-ESM1-2-LR/ssp585/r${member}i1p1f1/day/zg/gn/v????????/zg_day_MPI-ESM1-2-LR_ssp585_r${member}i1p1f1_gn_20950101-21001231.nc /scratch/m/m300883/MPI_GE_CMIP6/daily_ssp585/zg_day_MPI-ESM1-2-LR_ssp585_r${member}i1p1f1_gn_20750101-21001231.nc

    # anomaly
    cdo -monsub /scratch/m/m300883/MPI_GE_CMIP6/daily_ssp585/zg_day_MPI-ESM1-2-LR_ssp585_r${member}i1p1f1_gn_20750101-21001231.nc\
        -sellevel,100000,85000,70000,50000,25000 /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_season_global/zg_month_ensmean_2091_2100.nc\
        /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily_global/zg_MJJAS_ano_last10/zg_day_MPI-ESM1-2-LR_ssp585_r${member}i1p1f1_gn_20910501-21000931_ano.nc
}

export -f Anomaly
parallel --jobs 20 Anomaly ::: {1..50}