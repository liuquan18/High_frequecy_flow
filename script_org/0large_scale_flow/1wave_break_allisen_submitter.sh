#!/bin/bash
#SBATCH --job-name=wb
#SBATCH --time=03:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=wb.%j.out



mpirun -n 3 python 1wave_break_allisen.py $1