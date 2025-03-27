#!/bin/bash

module load parallel


uhat_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/ua_hat_daily/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/uhat_daily

mkdir -p $to_dir

find $uhat_dir -name "*.nc" | parallel -j 5 cdo -vertmean -sellevel,85000,87500,90000,92500,95000,97500,100000 {} ${to_dir}/{/}