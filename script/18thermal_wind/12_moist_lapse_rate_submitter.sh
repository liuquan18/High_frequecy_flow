#!/bin/bash
#SBATCH --job-name=malr
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=malr.%j.out


mpirun -n 10 python -u 12moist_lapse_rate.py $1 # node
