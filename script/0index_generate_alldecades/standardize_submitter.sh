#!/bin/bash
#SBATCH --job-name=ind_gen
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=ind_gen.%j.out


mpirun -n 5 python -u standardize_daily_index.py $1
