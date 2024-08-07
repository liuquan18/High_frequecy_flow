#!/bin/bash
# subtract the ensemble mean of the monthly data from the daily data using cdo monsub
# by doing which a long-term trend and seasonal cycle are removed
module load cdo
module load parallel

# define function called Anomaly
Anomaly() {

    member=$1
    echo $member
    # include month Mayb and september for later rolling window
    cdo -monsub -sellevel,100000,85000,70000,50000,25000 -sellonlatbox,-90,40,20,80 -selmonth,5,6,7,8,9 -selyear,1850/1859 \
        /pool/data/CMIP6/data/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r${member}i1p1f1/day/zg/gn/v????????/zg_day_MPI-ESM1-2-LR_historical_r${member}i1p1f1_gn_18500101-18691231.nc \
        /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/zg_MJJAS_ensmean/zg_Amon_MPI-ESM1-2-LR_HIST_ssp585_ensmean_MJJAS.nc \
        /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/daily/zg_MJJAS_ano_first10/zg_day_MPI-ESM1-2-LR_historical_r${member}i1p1f1_gn_18500601-18590831_ano.nc
}

export -f Anomaly
parallel --jobs 20 Anomaly ::: {1..50}