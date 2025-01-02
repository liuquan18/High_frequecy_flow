#!/bin/bash
#SBATCH --job-name=dec
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=dec.%j.out


mpirun -n 4 python -u 3dec_statistics.py $1 # node, var
