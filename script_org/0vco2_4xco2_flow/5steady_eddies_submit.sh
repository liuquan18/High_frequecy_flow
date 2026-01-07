#!/bin/bash
#SBATCH --job-name=python
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=python.%j.out


simulation=$1 # simulation name
var=$2 # variable name

echo run 5steady_eddies.py of $simulation with variable $var
mpirun -n 4 python -u 5steady_eddies.py $simulation $var