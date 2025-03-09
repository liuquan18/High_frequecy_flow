#!/bin/bash

#for loop 1-50
for ens in {1..50}
do
    # run the python script
    sbatch 1VKE.sh ${ens} 
    # ./1upvp.sh ${ens}
done