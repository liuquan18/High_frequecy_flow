#!/bin/bash
#SBATCH --job-name=wbfld
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=wbfld.%j.out


# Disable tqdm progress bars
export TQDM_DISABLE=1

mpirun -n 5 python 1lonlatbox_dec.py $1