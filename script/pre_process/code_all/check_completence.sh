
#!/bin/bash

# Name of the folder containing the files
folder_name=$1

# Check if the folder exists
if [ ! -d "$folder_name" ]; then
    echo "Error: Folder '$folder_name' does not exist."
    exit 1
fi

# Counter for missing files
missing_files=0

# Loop through numbers 1 to 50
for i in {1..50}; do
    # Construct the filename pattern
    file_pattern="*_r${i}i1p1f1_gn_*.nc"
    
    # Check if a file matching the pattern exists
    matching_file=$(ls "$folder_name"/$file_pattern 2>/dev/null | head -n 1)
    
    if [ -z "$matching_file" ]; then
        # If no matching file found, construct an example of the expected filename
        example_filename=$(ls "$folder_name"/*.nc 2>/dev/null | head -n 1)
        if [ -n "$example_filename" ]; then
            base_name=$(basename "$example_filename")
            expected_filename="${base_name/_r*i1p1f1_gn_/_r${i}i1p1f1_gn_}"
            echo "Missing file: $expected_filename"
        else
            echo "Missing file matching pattern: $file_pattern"
        fi
        missing_files=$((missing_files + 1))
    fi
done

# Report the results
if [ $missing_files -eq 0 ]; then
    echo "All 50 files are present."
else
    echo "Missing $missing_files file(s)."
fi

# Exit with a status code indicating success (0) or failure (1)
[ $missing_files -eq 0 ] && exit 0 || exit 1