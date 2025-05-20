#!/bin/bash
#SBATCH --job-name=before
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --mem=0
#SBATCH --ntasks-per-node=1
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=before.%j.out

decade=$1
var=$2
name=$3
window=$4
suffix=$5


echo " decade ${decade} for variable ${var} before ${window}"

python 1flux_before_NAO.py ${decade} ${var} ${name} ${window} ${suffix}