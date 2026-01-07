#!/bin/bash
#SBATCH --job-name=phase_speed
#SBATCH --time=06:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=phase_speed.%j.out



mpirun -n 2 python 0phase_speed_latitude.py $1 $2