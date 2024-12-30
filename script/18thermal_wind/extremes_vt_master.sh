#!/bin/bash
module load cdo
module load parallel
module load python3/unstable
conda activate air_sea 


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

var=$1
for ens in {1..50}
do
    echo "Ensemble member ${ens}"
    # run the python script
    sbatch extremes_vt_submitter.sh ${ens} 
done