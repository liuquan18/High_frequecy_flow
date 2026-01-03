#!/bin/bash
decade=$1
#for loop 1-50
for ens in {1..50}
do
    echo "Ensemble member ${ens} for decade ${decade}"
    # run the python script
    sbatch 1phase_speed_wind_run.sh ${ens} ${decade}
done