#!/bin/bash

var=$1

var_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/${var}_daily_std_mergeyear/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/moisture_variability_stat/
tmp_dir=/scratch/m/m300883/ERA5/percentile/

mkdir -p $tmp_dir


daily_files=($(find $var_dir -name "*.nc" -print))

# mergetime
cdo -P 10 -mergetime [ ${daily_files[@]} ] ${tmp_dir}${var}_daily_std_mergeyear.nc

infile=${tmp_dir}${var}_daily_std_mergeyear.nc
outfile=${to_dir}${var}_temporal_percentile.nc

# temporal percentile
cdo timpctl,90 $infile -timmin $infile -timmax $infile $outfile