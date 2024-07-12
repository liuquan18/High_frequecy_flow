#!/bin/bash

module load cdo

month=$1
echo "Ensemble mean for month ${month}"

FROM=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/zg_${month}/
TO=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/season/zg_${month}_ensmean/
mkdir -p ${TO}

cdo ensmean ${FROM}*.nc ${TO}zg_Amon_MPI-ESM1-2-LR_HIST_ssp585_ensmean_${month}.nc