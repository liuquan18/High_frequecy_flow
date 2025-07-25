#!/bin/bash
#SBATCH --job-name=heat_y
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=heat_y.%j.out

phase=$1 # phase
decade=$2 # decade
eddy=$3 # steady or transient
ano=$4 # anomaly

echo run $phase for $decade

python 8eddy_heat_meridional_time.py $phase $decade $eddy $ano
