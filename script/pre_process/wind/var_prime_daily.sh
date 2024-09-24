#!/bin/bash

# bandpass filter 2-12 days with cdo
module load cdo
module load parallel

var=$1 # zg, ua, va
period=$2 # first10, last10

from_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_global/${var}_MJJAS_${period}/
to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_global/${var}_MJJAS_${period}_prime/
tmp_dir=/scratch/m/m300883/${var}/bandpass/


mkdir -p ${to_path} ${tmp_dir}

export from_path to_path tmp_dir var


# function to band filter
band_filter(){
    infile=$1
    # basename without .nc
    fname=$(basename ${infile%.nc})
    outfile=${to_path}${fname}.nc

    # split years
    cdo -P 10 -splityear -del29feb ${infile} ${tmp_dir}${fname}_year
    # band filter, keep 2-12 days 
    year_files=$(ls ${tmp_dir}${fname}_year*)
    cdo -O -P 10 -mergetime -apply,bandpass,30.5,182.5 [ ${year_files} ] ${outfile}
    # remove temporary files
    rm ${tmp_dir}${fname}_year*
}

export -f band_filter
# parallel band filter in to_dir
parallel --jobs 10 band_filter ::: ${from_path}*.nc

# check if all files are processed in ${to_path}
# Loop through numbers 1 to 50
for i in {1..50}; do
    # Construct the filename pattern
    file_pattern="*_r${i}i1p1f1_gn_*.nc"
    
    # Check if a file matching the pattern exists
    matching_file=$(ls "$to_path"/$file_pattern 2>/dev/null | head -n 1)
    
    if [ -z "$matching_file" ]; then
        # If no matching file found, construct an example of the expected filename
        example_filename=$(ls "$to_path"/*.nc 2>/dev/null | head -n 1)
        if [ -n "$example_filename" ]; then
            base_name=$(basename "$example_filename")
            expected_filename="${base_name/_r*i1p1f1_gn_/_r${i}i1p1f1_gn_}"
            echo "Missing file: $expected_filename"
            echo "regenerate without parallel"
            band_filter ${from_path}${expected_filename}

        else
            echo "Missing file matching pattern: $file_pattern"
        fi
    fi

done

