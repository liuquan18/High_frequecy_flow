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


for ens in {1..50..5}
do
    echo "Ensemble member ${ens}"
    # run the python script
    sbatch 12hus_tas_ratio_submit.sh ${ens}
done