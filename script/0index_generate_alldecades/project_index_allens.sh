#!/bin/bash
source /etc/profile
module load cdo
module load parallel
module load python3/unstable
conda activate air_sea 

#for loop 1-50
for ens in {1..50}
do
    echo "Ensemble member ${ens}"
    # run the python script
    sbatch project_daily_index_submitter.sh ${ens}
done