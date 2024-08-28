#!/bin/bash
#SBATCH --job-name=wb
#SBATCH --time=04:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=20
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=wb.%j.out


mpirun -n 5 python -u wb_index_scherrer.py $1 # 0,1
