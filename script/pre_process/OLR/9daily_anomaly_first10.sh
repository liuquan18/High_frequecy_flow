#!/bin/bash
module load cdo
module load parallel

base_dir=/work/ik1017/CMIP6/data/CMIP6/CMIP/MPI-M/MPI-ESM1-2-LR/historical/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/first10_OLR_daily_ano/
export to_dir
export base_dir


# define the function
Anomaly() {
    member=$1
    infile=$(find ${base_dir}r${member}i1p1f1/day/ -name 'rlut_day_MPI-ESM1-2-LR_historical_r'${member}'i1p1f1_gn_18500101-18691231.nc')
    month_ens=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_season_global/rlut_Amon_MPI-ESM1-2-LR_HIST_ensmean_185005-185909.nc
    outfile=${to_dir}$(basename ${infile} | sed 's/18500101-18691231.nc/18500501-18590930_ano.nc/')

    # include month Mayb and september for later rolling window
    cdo -monsub -selyear,1850/1859 -selmon,5/9 -sellonlatbox,-180,180,-30,30 ${infile} -sellonlatbox,-180,180,-30,30 ${month_ens} ${outfile}
}


export -f Anomaly

parallel --jobs 10 Anomaly ::: {1..50}