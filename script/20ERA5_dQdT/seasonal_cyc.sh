#!/bin/bash

zg_sesonal_dir=/work/mh0033/m300883/Tel_MMLE/data/ERA5/zg/
monthly_files=($(find $zg_sesonal_dir -name "*.grb" -print))
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_monthly_stat/

# seasonal cycle
cdo -f nc -P 10 -setgridtype,regular -divc,9.80665 -ymonmean -selmon,5/9 -mergetime -apply,sellevel,50000 [ $monthly_files ] ${to_dir}zg_50000_seasonal_cyc_05_09.nc

# trend
cdo -f nc -P 10 -trend -mergetime -apply,"-selmon,5 -sellevel,50000 -divc,9.80665" [ $monthly_files ] ${to_dir}zg_50000_trend_05_a.nc ${to_dir}zg_50000_trend_05_b.nc
cdo -f nc -P 10 -trend -mergetime -apply,"-selmon,6 -sellevel,50000 -divc,9.80665" [ $monthly_files ] ${to_dir}zg_50000_trend_06_a.nc ${to_dir}zg_50000_trend_06_b.nc
cdo -f nc -P 10 -trend -mergetime -apply,"-selmon,7 -sellevel,50000 -divc,9.80665" [ $monthly_files ] ${to_dir}zg_50000_trend_07_a.nc ${to_dir}zg_50000_trend_07_b.nc
cdo -f nc -P 10 -trend -mergetime -apply,"-selmon,8 -sellevel,50000 -divc,9.80665" [ $monthly_files ] ${to_dir}zg_50000_trend_08_a.nc ${to_dir}zg_50000_trend_08_b.nc
cdo -f nc -P 10 -trend -mergetime -apply,"-selmon,9 -sellevel,50000 -divc,9.80665" [ $monthly_files ] ${to_dir}zg_50000_trend_09_a.nc ${to_dir}zg_50000_trend_09_b.nc

# merge trends
