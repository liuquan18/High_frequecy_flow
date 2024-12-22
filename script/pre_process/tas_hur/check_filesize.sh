#!/bin/bash
directory="/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_daily_std"
threshold_size=112838625

# Find files smaller than the threshold size and print their names
find "$directory" -type f -size -${threshold_size}c -print