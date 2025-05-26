#!/bin/bash
#SBATCH --job-name=trop
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=trop.%j.out

mpirun -n 10 python -u 2first_last_trop_standardize.py $1
