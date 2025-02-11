#!/bin/bash
module load cdo
module load parallel
module load python3/unstable
conda activate air_sea 

for ens in {1..50}
do
    echo "Ensemble member ${ens}"
    # run the python script
    sbatch 1moist_thermal_wind_submitter.sh ${ens}
done