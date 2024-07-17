#!/bin/bash

# for first10 years
base_path="/pool/data/CMIP6/data/CMIP/MPI-M/MPI-ESM1-2-LR/historical"
variable="zg"
timespan="185001-186912"

# Array to store file paths
declare -a file_list

# Loop through realizations r1 to r50
for r in {1..50}; do
    # Use find to locate the file, accounting for different version dates
    file=$(find "$base_path/r${r}i1p1f1/Amon/$variable/gn" -name "${variable}_Amon_MPI-ESM1-2-LR_historical_r${r}i1p1f1_gn_${timespan}.nc")
    
    # If file is found, add it to the list
    if [ -n "$file" ]; then
        file_list+=("$file")
    fi
done

# Print the file list
# printf "%s\n" "${file_list[@]}"

# Optionally, save the list to a file
# printf "%s\n" "${file_list[@]}" > file_list.txt

# Use the list with cdo ensmean
cdo -O -selmonth,5/9 -ensmean -apply,-selyear,1850/1859 [ "${file_list[@]}" ] /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_season_global/zg_month_ensmean_1850_1859.nc