#!/bin/bash
#SBATCH --job-name=EP
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=EP.%j.out

phase=$1 # phase
decade=$2 # decade
isentrope=$3 # isentrope
eddy=$4 # steady or transient
ano=$5 # anomaly

echo run $phase for $decade

python 4EP_flux.py $phase $decade $isentrope $eddy $ano
