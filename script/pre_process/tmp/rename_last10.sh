#!/bin/bash

# Directory containing the files
directory="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/zg_daily_global/zg_MJJAS_ano_last10/"

# Iterate over the matching files and rename them
for file in "${directory}"*20910601-21000831_ano.nc; 
do
    # Extract the base name of the file
    base_name=$(basename "$file")
    
    # Define the new file name
    new_file="${directory}${base_name/20910601-21000831/20910501-21000930}"
    
    # Rename the file
    mv "$file" "$new_file"
done

echo "Renaming completed."