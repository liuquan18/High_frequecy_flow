#!/bin/bash
module load cdo

# to data directory
cd /pool/data/ERA5/E5/pl/an/1H/129/

# merge files starting with "1980-06"
cdo -f nc -P 36 -mergetime -apply,-sellevel,50000 [ E5pl00_1H_1980-06* ] /work/mh0033/m300883/High_frequecy_flow/data/example_blocking_event/ERA5_1980-06.nc