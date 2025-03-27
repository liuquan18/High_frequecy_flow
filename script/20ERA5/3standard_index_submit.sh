#!/bin/bash
#SBATCH --job-name=std
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=5
#SBATCH --ntasks=30
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=std.%j.out

mpirun -n 30 python -u 3standard_index.py
