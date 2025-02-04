#!/bin/bash
#SBATCH --job-name=thermal_wind
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=thermal_wind.%j.out


mpirun -n 5 python -u 0thermal_wind_from_geostrophic_wind.py $1 # node
