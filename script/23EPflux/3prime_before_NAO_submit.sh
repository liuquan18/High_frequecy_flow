#!/bin/bash
#SBATCH --job-name=before
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=before.%j.out

decade=$1
var=$2
name=$3
suffix=$4


echo " decade ${decade} for variable ${var}"

python 3prime_before_NAO_15_5_mean.py ${decade} ${var} ${name} ${suffix}