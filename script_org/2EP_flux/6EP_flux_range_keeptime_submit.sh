#!/bin/bash
#SBATCH --job-name=EP_time
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=EP_time.%j.out

phase=$1 # phase
decade=$2 # decade
eddy=$3 # steady or transient
ano=$4 # anomaly

echo run $phase for $decade

python 6EP_flux_range_keeptime.py $phase $decade $eddy $ano

