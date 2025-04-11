#!/bin/bash
#SBATCH --job-name=EP_isen
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=EP_isen.%j.out

phase=$1 # phase
decade=$2 # decade
isentrope=$3 # isentrope
ano=$4 # anomaly

echo run $phase for $decade

python 4EP_flux_isentropes.py $phase $decade $isentrope $ano
