#!/bin/bash

module load parallel


dir=$1
to_dir=${dir}_t

mkdir -p $to_dir

find $dir -name "*.nc" | parallel -j 10 cdo -r -copy {} ${to_dir}/{/}