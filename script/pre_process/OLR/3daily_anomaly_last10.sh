#!/bin/bash
module load cdo
module load parallel

# lists
daily_list1=$(cat /work/mh0033/m300883/High_frequecy_flow/script/pre_process/OLR/last10_month_files1.csv)
month_ens1=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_season_global/OLR_monthly_ensmean_207505-209409.nc
savedir1=/scratch/m/m300883/OLR/list1/

daily_list2=$(cat /work/mh0033/m300883/High_frequecy_flow/script/pre_process/OLR/last10_month_files2.csv)
month_ens2=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_season_global/OLR_monthly_ensmean_209505-210009.nc
savedir2=/scratch/m/m300883/OLR/list2/

export daily_list1 month_ens1 savedir1 daily_list2 month_ens2 savedir2

# save
savedir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/last10_OLR_daily_ano/
export savedir

# define the function
Anomaly() {

    infile=$1
    monthfile=$2
    savedir=$3
    # include month Mayb and september for later rolling window
    cdo -monsub -selmon,5/9 -sellonlatbox,-180,80,-30,30 ${infile} -sellonlatbox,-180,80,-30,30 ${monthfile} ${savedir}$(basename ${infile} .nc)_ano.nc
}

export -f Anomaly
parallel --jobs 20 Anomaly ::: ${daily_list1} ::: ${month_ens1} ::: ${savedir1}

parallel --jobs 20 Anomaly ::: ${daily_list2} ::: ${month_ens2} ::: ${savedir2}


# define function to merge time
merge(){
    infile1=$1
    infile2=$2
    
    # cdo meregetime
    cdo -selyear,2091/2100 -mergetime ${infile1} ${infile2} ${savedir} ${savedir}$(basename ${infile1} | sed 's/20750101-20941231_ano.nc/20910501-21000931_ano.nc/')
}

export -f merge
parallel --jobs 20 merge ::: ${savedir1}*_ano.nc ::: ${savedir2}*_ano.nc