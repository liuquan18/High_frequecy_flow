#!/bin/bash
#SBATCH --job-name=extreme
#SBATCH --time=08:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=extreme.%j.out


mpirun -n 5 python -u OLR_extremes.py $1 # 0,1
# python -u hello0index_generator.py $1 $2 $3