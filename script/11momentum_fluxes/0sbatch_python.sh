#!/bin/bash
#SBATCH --job-name=run_py
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=5
#SBATCH --ntasks=5
#SBATCH --ntasks-per-node=1
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=run_py.%j.out

script=$1
parameter=$2
python -u $script $parameter
