#!/bin/bash
#SBATCH --job-name=absvort
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=absvort.%j.out


mpirun -n 5 python -u 0abs_vorticity.py $1 # node
