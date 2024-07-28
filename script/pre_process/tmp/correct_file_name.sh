#!/bin/bash

# define function called rename

# Directory containing the files
DIR="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily_global/zg_mermean_first10"

# Loop through files ending with "0831_ano.nc"
# for file in "$DIR"/*0831_ano.nc; do
#     # Check if the file exists to avoid errors in case of no matching files
#     if [ -f "$file" ]; then
#         # Use the 'mv' command to rename the file
#         # Replace "0831_ano.nc" with "0930_ano.nc" in the filename
#         mv "$file" "${file/0831_ano.nc/0930_ano.nc}"
#     fi
# done

# Loop through files ending with "0601" and rename them to "0501"
for file in "$DIR"/*0601*.nc; do
    # Check if the file exists to avoid errors in case of no matching files
    if [ -f "$file" ]; then
        # Use the 'mv' command to rename the file
        # Replace "0601" with "0501" in the filename
        mv "$file" "${file/0601/0501}"
    fi
done