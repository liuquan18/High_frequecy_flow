#!/bin/bash
cd /work/mh0033/m300883/High_frequecy_flow/script/16waveguid
source /etc/profile
module load python3/unstable
conda activate air_sea


for task in {1..9}
do
    sbatch ./band_var_submit.sh first10 $task
    echo "Submitted first10 $task"
    sbatch ./band_var_submit.sh last10 $task
    echo "Submitted last10 $task"
done
