#!/bin/bash
#SBATCH --job-name=EP_df
#SBATCH --time=06:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=450G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=EP_df.%j.out

eddy=$1 # steady or transient
div=$2 # div or non-div
phase=$3 # phase
plev=$4 # plev or plev2

python 7EP_flux_df.py $eddy $div $phase $plev

