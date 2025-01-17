#!/bin/bash

#for loop 1-50
# for var in tas hur
# do
# echo "Variable ${var}"

#     for ens in {1..50}
#     do
#         echo "Ensemble member ${ens}"
#         # run the python script
#         sbatch var_spatial_std_submitter.sh ${ens} ${var}
#     done

# done
var1=$1
var2=$2
split_basin=$3

for ens in {1..50..5}
do
    echo "Ensemble member ${ens}"
    # run the python script
    sbatch 5frequency_coherence_submit.sh ${ens} ${var1} ${var2} ${split_basin}
done