#!/bin/bash
#SBATCH --job-name=recon
#SBATCH --time=04:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=recon.%j.out



mpirun -n 10 python NA_zg_relate_OLR_reconstruct.py $1