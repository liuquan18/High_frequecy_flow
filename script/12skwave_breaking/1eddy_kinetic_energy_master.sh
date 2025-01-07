#!/bin/bash

#for loop 1-50
for ens in {1..50}
do
    echo "Ensemble member ${ens}"
    # run the python script
    sbatch 1eddy_kinetic_energy.sh ${ens}
    # ./1upvp.sh ${ens}
done