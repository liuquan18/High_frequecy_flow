#!/bin/bash
#SBATCH --job-name=wb_fldmean
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=wb_fldmean.%j.out



python wb_fldmean.py $1
