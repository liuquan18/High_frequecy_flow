#!/bin/bash
#SBATCH --job-name=extreme
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=20
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=extreme.%j.out


mpirun -n 20 python -u extreme_extract.py $1 # 0,1
# python -u hello0index_generator.py $1 $2 $3