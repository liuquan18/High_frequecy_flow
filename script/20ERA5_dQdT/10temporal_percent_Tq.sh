#!/bin/bash

var=$1

var_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/${var}_daily_std_mergeyear/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/moisture_variability_stat/


daily_files=($(find $var_dir -name "*.nc" -print))

cdo -P 10 -timpctl,1 -mergetime [ ${daily_files[@]} ] ${to_dir}${var}_daily_std_mergeyear_timmean.nc