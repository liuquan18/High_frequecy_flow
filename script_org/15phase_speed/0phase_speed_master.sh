#!/bin/bash
decade=$1
var1=$2
var2=$3
#for loop 1-50
for ens in {1..50}
do
    echo "Ensemble member ${ens} for decade ${decade}"
    # run the python script
    sbatch 0phase_speed_submit.sh ${ens} ${decade} ${var1} ${var2}
done