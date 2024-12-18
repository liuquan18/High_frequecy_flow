#!/bin/bash
source /etc/profile
module load cdo
module load parallel
module load python3/unstable
conda activate air_sea 

#for loop 1-50
for year in {1850..2100..10}
do
    echo "Decade ${year}"
    # run the python script
    sbatch standardize_submitter.sh ${year}
done