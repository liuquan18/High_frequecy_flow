#!/bin/bash

var=$1 # eke, eke_high
#for loop 1-50
for ens in {1..50}
do
    echo "Ensemble member ${ens}"
    # run the python script
    sbatch 6eddy_mermean.sh ${ens} ${var} 40 60
    # ./1upvp.sh ${ens}
done