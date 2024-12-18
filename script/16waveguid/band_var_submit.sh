#!/bin/bash
#SBATCH --job-name=mean
#SBATCH --time=04:00:00
#SBATCH --partition=compute
#SBATCH --nodes=10
#SBATCH --ntasks=153
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=mean.%j.out


mpirun -n 153 python -u band_variance.py $1 $2 # period, node
