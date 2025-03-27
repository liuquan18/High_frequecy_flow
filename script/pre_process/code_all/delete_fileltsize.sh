#!/bin/bash

target_dir="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/vke_daily"
min_size=564678000  # bytes
         
echo "Checking files in $target_dir"

# Find and remove files smaller than min_size bytes
find "$target_dir" -type f -size -"${min_size}"c -exec rm -v {} \;