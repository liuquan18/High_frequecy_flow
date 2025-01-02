#!/bin/bash
module load cdo
module load parallel
module load python3/unstable
conda activate air_sea 

var=$1
for dec in {1850..2090..10}
do
    echo "Decade ${dec}"
    # run the python script
    sbatch monmean_ensmean.sh ${dec} ${var}
done