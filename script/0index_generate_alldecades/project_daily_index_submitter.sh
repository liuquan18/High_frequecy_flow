#!/bin/bash
#SBATCH --job-name=ind_gen
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=ind_gen.%j.out


mpirun -n 10 python -u project_daily_index.py $1
