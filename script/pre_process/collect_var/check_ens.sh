#/bin/bash
directory="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_daily_std"

# Loop through all files in the directory
find "$directory" -type f | while read -r file; do
    # Extract the subfolder name and the file name
    subfolder=$(basename "$(dirname "$file")")
    filename=$(basename "$file")

    # Extract the number after 'r' in the subfolder and the file name
    subfolder_r=$(echo "$subfolder" | grep -oP 'r\K[0-9]+')
    filename_r=$(echo "$filename" | grep -oP 'r\K[0-9]+')

    # Check if the numbers are different
    if [ "$subfolder_r" != "$filename_r" ]; then
        echo "$file"
    fi
done