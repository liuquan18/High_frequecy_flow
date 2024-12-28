#!/bin/bash


#for loop 1-50
for ens in {1..50}
do
    echo "Ensemble member ${ens}"
    # run the python script
    sbatch daily_anomaly_single_ensemble.sh ${ens}
done