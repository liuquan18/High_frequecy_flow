#!/bin/bash
#SBATCH --job-name=before_wb
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=5
#SBATCH --ntasks=5
#SBATCH --ntasks-per-node=1
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=before_wb.%j.out

var=$1 # eke or eke_high
mpirun -n 25 python -u 11eke_before_NAO.py $var
