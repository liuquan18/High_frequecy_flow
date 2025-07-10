#!/bin/bash
#SBATCH --job-name=upvp_index
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=3
#SBATCH --ntasks=3
#SBATCH --cpus-per-task=5
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=upvp_index.%j.out

ens=$1

echo "Ensemble member: $ens"

mpirun -n 5 python -u project_upcp_index.py $ens    
