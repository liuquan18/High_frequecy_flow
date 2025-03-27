#!/bin/bash
#SBATCH --job-name=ivke
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=ivke.%j.out


mpirun -n 5 python -u 2IVKE.py $1 # node
