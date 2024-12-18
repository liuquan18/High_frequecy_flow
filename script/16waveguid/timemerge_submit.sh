#!/bin/bash
#SBATCH --job-name=mean
#SBATCH --time=04:00:00
#SBATCH --partition=compute
#SBATCH --nodes=5
#SBATCH --ntasks=20
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=mean.%j.out


mpirun -n 20 python -u timemerge.py $1
# python -u hello0index_generator.py $1 $2 $3