#!/bin/bash
module load cdo

cdo -ymonmean /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_season_global/ua_Amon_MPI-ESM1-2-LR_HIST_ensmean_185005-185909.nc /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_season_global/ua_Amon_MPI-ESM1-2-LR_HIST_climatology_185005-185909.nc

cdo -ymonmean /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_season_global/ua_Amon_MPI-ESM1-2-LR_HIST_ensmean_209105-210009.nc /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_season_global/ua_Amon_MPI-ESM1-2-LR_HIST_climatology_209105-210009.nc