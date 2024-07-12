#!/bin/bash

# Array to store file paths
declare -a file_list
variable="zg"

# Loop through realizations r1 to r50
for r in {1..50}; do
    # If file1 is found, add it to the list
    file="/scratch/m/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_season_global/${variable}_Amon_MPI-ESM1-2-LR_ssp585_r${r}i1p1f1_gn_209101-210012.nc"
    if [ -n "$file" ]; then
        file_list+=("$file")
    fi

done


# Print the file list
# printf "%s\n" "${file_list[@]}"

# Optionally, save the list to a file
# printf "%s\n" "${file_list[@]}" > file_list.txt

# Use the list with cdo ensmean
cdo  -O -selmonth,5/9 -ensmean -apply,-selyear,2091/2100 [ "${file_list[@]}" ] /work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_season_global/zg_month_ensmean_2091_2100.nc