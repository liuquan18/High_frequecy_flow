#!/bin/bash
#SBATCH --job-name=heat_dy
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=heat_dy.%j.out



mpirun -n 5 python 9eddy_heat_dy_decade.py $1
