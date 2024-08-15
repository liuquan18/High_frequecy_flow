#!/bin/bash

module load cdo
module load parallel

# define function to merge time
merge(){
    member=$1
    infile1=/scratch/m/m300883/OLR/list1/rlut_day_MPI-ESM1-2-LR_ssp585_r${member}i1p1f1_gn_20750101-20941231.nc
    infile2=/scratch/m/m300883/OLR/list2/rlut_day_MPI-ESM1-2-LR_ssp585_r${member}i1p1f1_gn_20950101-21001231.nc

    savedir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/OLR_daily_anomaly/last10_OLR_daily_ano/
    # cdo meregetime
    outfile=rlut_day_MPI-ESM1-2-LR_ssp585_r${member}i1p1f1_gn_20910501-21000931_ano.nc
    
    cdo -selyear,2091/2100 -mergetime ${infile1} ${infile2} ${savedir}${outfile}
}

export -f merge

parallel --jobs 20 merge ::: {1..50}