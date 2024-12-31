#!/bin/bash
#SBATCH --job-name=hussat
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=hussat.%j.out


mpirun -n 5 python -u 2hussat_daily_cal.py $1 