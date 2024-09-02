#!/bin/bash
#SBATCH --job-name=wb
#SBATCH --time=08:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=wb.%j.out


mpirun -n 2 python -u WB_events.py $1 # 0,1
