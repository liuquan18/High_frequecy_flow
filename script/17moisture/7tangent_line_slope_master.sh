#!/bin/bash
module load cdo
module load parallel
module load python3/unstable
conda activate air_sea 


for dec in {1850..2090..10}
do
    echo "Decade ${dec}"
    # run the python script
    sbatch 7tangent_line_slope_submitter.sh ${dec}
done