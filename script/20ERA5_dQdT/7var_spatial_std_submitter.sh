#!/bin/bash
#SBATCH --job-name=std
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=std.%j.out


mpirun -n 1 python -u 7var_spatial_std.py $1 # var
