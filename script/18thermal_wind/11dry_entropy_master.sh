#!/bin/bash
module load cdo
module load parallel
module load python3/unstable
conda activate air_sea 



for ens in {1..50}
do
    echo "Ensemble member ${ens}"
    # run the python script
    sbatch 11dry_entropy_submitter.sh ${ens}
done