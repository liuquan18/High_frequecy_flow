#!/bin/bash
#SBATCH --job-name=wb
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=wb.%j.out



mpirun -n 5 python 1wave_break_allisen.py $1