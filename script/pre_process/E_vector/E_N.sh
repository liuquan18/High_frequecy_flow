#!/bin/bash

# bandpass filter 2-12 days with cdo
module load cdo
module load parallel

period=$1 # first10, last10
frequency=$2 # prime, prime_veryhigh, prime_intermedia

# u prime and v prime path
uprime_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/ua_daily_global/ua_MJJAS_${period}_${frequency}/
vprime_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/va_daily_global/va_MJJAS_${period}_${frequency}/

to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/E_N_daily_global/E_N_MJJAS_${period}_${frequency}/
# mf: momentum fluxes

mkdir -p ${to_path}

export uprime_path vprime_path to_path

# function to calculate high frequency momentum fluxes
Momentum(){
    member=$1
    ufile=$(find ${uprime_path} -name ua_*r${member}i1p1f1_gn_*.nc)
    vfile=$(find ${vprime_path} -name va_*r${member}i1p1f1_gn_*.nc)
    # basename without .nc
    ufname=$(basename ${ufile%.nc})
    outfile=${to_path}E_N_${ufname:3}.nc

    cdo -O -P 10 -mul ${ufile} ${vfile} ${outfile}
}

export -f Momentum

# parallel Momentum for all members

parallel --jobs 10 Momentum ::: {1..50}

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
            Momentum ${i}

        else
            echo "Missing file matching pattern: $file_pattern"
        fi
    fi
done