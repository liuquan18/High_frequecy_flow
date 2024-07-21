#!/bin/bash

module load cdo
module load parallel

# define path
period=last10
path_to_input_files=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily_global/zg_MJJAS_ano_${period}/
path_to_output_files=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily_global/zg_mermean_${period}/


# use find and parallel to calculate the meridional mean of the zg anomaly with cdo mermean
find ${path_to_input_files} -name "*.nc" | parallel --jobs 20 cdo -mermean -sellonlatbox,-180,180,40,60 {} ${path_to_output_files}{/}