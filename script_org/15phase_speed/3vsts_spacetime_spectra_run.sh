#!/bin/bash
#SBATCH --job-name=spacetime
#SBATCH --output=spacetime.%j.out
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=2
#SBATCH --time=02:00:00
#SBATCH --partition=compute
#SBATCH --mem=0
#SBATCH --account=mh0033
#SBATCH --mail-type=FAIL

# Load modules
module load python3/unstable
module load intel-oneapi-mpi/2021.5.0-intel-2021.5.0

# Activate conda
source ~/.bashrc
conda activate air_sea

# Set PMI library
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so

ens=$1
for decade in 1850 2090
do
    echo "Running spacetime spectra for decade ${decade} ensemble member ${ens}"
    srun --mpi=pmi2 python 3vsts_spacetime_spectra.py ${ens} ${decade} # ens # decade
done
