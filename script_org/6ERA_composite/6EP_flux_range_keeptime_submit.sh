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
eddy=$2 # steady or transient


python 6EP_flux_range_keeptime.py $phase $eddy 

