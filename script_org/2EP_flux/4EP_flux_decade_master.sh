#!/bin/bash

#for loop 1-50
for ens in {1..50}
do
    echo "Ensemble member ${ens}"
    # run the python script
    sbatch 4EP_flux_decade_submit.sh ${ens}
done