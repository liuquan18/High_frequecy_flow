#!/bin/bash
#SBATCH --job-name=Evector
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=Evector.%j.out

phase=$1 # phase
decade=$2 # decade
eddy=$3 # steady or transient
ano=$4 # anomaly

echo run $phase for $decade

python 5E_vector_comp.py $phase $decade $eddy $ano

