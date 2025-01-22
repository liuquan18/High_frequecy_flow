#!/bin/bash
#SBATCH --job-name=std
#SBATCH --time=08:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=std.%j.out

module load parallel

var=$1  
basedir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/${var}_daily/



find ${basedir} -name "*.nc" | parallel python 7var_spatial_std.py {}

