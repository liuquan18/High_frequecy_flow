#!/bin/bash
#SBATCH --job-name=coherence
#SBATCH --time=03:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=coherence.%j.out

module load parallel
module load cdo

var1=$1
var2=$2
split_basin=$3
pixel_wise=$4

mpirun -np 5 python /work/mh0033/m300883/High_frequecy_flow/script/20ERA5_dQdT/9frequency_coherence.py \
    ${var1} ${var2} ${split_basin} ${pixel_wise}