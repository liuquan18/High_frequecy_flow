#!/bin/bash
#SBATCH --job-name=mean
#SBATCH --time=04:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=mean.%j.out


mpirun -n 10 python -u band_mean.py $1
# python -u hello0index_generator.py $1 $2 $3