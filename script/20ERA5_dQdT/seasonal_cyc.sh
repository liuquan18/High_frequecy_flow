#!/bin/bash

zg_sesonal_dir=/work/mh0033/m300883/Tel_MMLE/data/ERA5/zg/
monthly_files=($(find $zg_sesonal_dir -name "*.grb" -print))
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_monthly/

cdo -P 10 -ymonmean -selmon,5/9 -mergetime -apply,sellevel,50000 [ $monthly_files ] ${to_dir}zg_50000_seasonal_cyc_05_09.nc