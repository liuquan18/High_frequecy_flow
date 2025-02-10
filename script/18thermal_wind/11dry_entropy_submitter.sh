#!/bin/bash
#SBATCH --job-name=sd
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=sd.%j.out


mpirun -n 10 python -u 11dry_entropy.py $1 # node
