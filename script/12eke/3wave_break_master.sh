#!/bin/bash

#for loop 1-50
for ens in {1..50}
do
    echo "Ensemble member ${ens}"
    # run the python script
    sbatch 3wave_break_submitter.sh ${ens}
done