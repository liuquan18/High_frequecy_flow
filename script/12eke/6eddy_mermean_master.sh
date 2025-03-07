#!/bin/bash

var=$1 # eke, eke_high
lat_min=${2:-20}  # Default to 20 if $2 is not provided
lat_max=${3:-60}  # Default to 60 if $3 is not provided
#for loop 1-50
for ens in {1..50}
do
    echo "Ensemble member ${ens}"
    # run the python script
    sbatch 6eddy_mermean.sh ${ens} ${var} ${lat_min} ${lat_max}
    # ./1upvp.sh ${ens}
done