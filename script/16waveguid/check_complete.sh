#!/bin/bash
period=$1
base_dir="/scratch/m/m300883/waveguide/$period"

# Loop through expected subfolder numbers
for num in $(seq 1 50); do
    subfolder="$base_dir/r${num}i1p1f1"
    # Check if subfolder exists
    if [ ! -d "$subfolder" ]; then
        echo "Missing subfolder: r${num}i1p1f1"
    else
        # Count the number of files in the subfolder
        file_count=$(find "$subfolder" -type f | wc -l)
        if [ "$file_count" -lt 153 ]; then
            echo "Subfolder r${num}i1p1f1 has $file_count files (expected 153)"
        fi
    fi
done