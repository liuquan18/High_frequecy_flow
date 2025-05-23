#!/bin/bash
#SBATCH --job-name=2pv
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=2pv.%j.out



mpirun -n 5 python 2pv_isent.py $1