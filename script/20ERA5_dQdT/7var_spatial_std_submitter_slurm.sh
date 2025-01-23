#!/bin/bash
#SBATCH --job-name=slurm
#SBATCH --time=08:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=slurm.%j.out

module load parallel

var=$1

parallel --jobs 10 python 7var_spatial_std.py ::: $var ::: {0..3}

