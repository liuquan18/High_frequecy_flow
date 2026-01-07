#!/bin/bash
#SBATCH --job-name=python
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=python.%j.out

file=$1 # python file to run
simulation=$2 # 

echo run $file of $simulation
mpirun -n 4 python -u $file $simulation