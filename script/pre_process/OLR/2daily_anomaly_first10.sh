#!/bin/bash
module load cdo
module load parallel

# first10 years
daily_list=$(cat /work/mh0033/m300883/High_frequecy_flow/script/pre_process/OLR/first10_daily_files.csv)
savedir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/first10_OLR_daily_ano/

export savedir

# define the function
Anomaly() {

    infile=$1
    month_ens=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_season_global/OLR_monthly_ensmean_185005-185909.nc

    # include month Mayb and september for later rolling window
    cdo -monsub -selyear,1850/1859 -selmon,5/9 -sellonlatbox,-180,80,-30,30 ${infile} -sellonlatbox,-180,80,-30,30 ${month_ens} ${savedir}$(basename ${infile} .nc)_ano.nc
}


export -f Anomaly
parallel --jobs 10 Anomaly ::: ${daily_list}