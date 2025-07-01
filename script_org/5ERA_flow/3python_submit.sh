#!/bin/bash
#SBATCH --job-name=python
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=23
#SBATCH --ntasks=46
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=python.%j.out

file=$1 # python file to run

mpirun -n 46 python -u $file
