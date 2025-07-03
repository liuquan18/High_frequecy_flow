#!/bin/bash
#SBATCH --job-name=proj
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=5
#SBATCH --ntasks=10
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=proj.%j.out

mpirun -n 50 python -u 2index_generate.py
