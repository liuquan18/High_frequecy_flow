#!/bin/bash
#SBATCH --job-name=stability_time
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=stability.%j.out


phase=$1 # phase
python 5effective_static_stability.py $phase