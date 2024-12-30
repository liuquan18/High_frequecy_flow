#!/bin/bash
#SBATCH --job-name=extreme
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=extreme.%j.out


mpirun -n 5 python -u extremes_vt.py $1 $2# node, var
