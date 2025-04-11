#!/bin/bash
#SBATCH --job-name=python
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=python.%j.out

phase=$1 # phase
decade=$2 # decade

echo run $phase for $decade

python 7EP_flux_isentropes.py $phase $decade
