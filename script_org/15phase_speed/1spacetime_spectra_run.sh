#!/bin/bash
#SBATCH --job-name=wind_isent
#SBATCH --output=wind_isent.%j.out
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=1
#SBATCH --time=08:00:00
#SBATCH --partition=compute
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH --account=mh0033

# Load modules
module load python3/unstable
module load intel-oneapi-mpi/2021.5.0-intel-2021.5.0

# Activate conda
source ~/.bashrc
conda activate air_sea

# Set PMI library
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so

decade=$2

for year in $(seq $decade $((decade+9)))
do
    echo "Processing year ${year} for decade ${decade}s"
    # run the python script
    srun --mpi=pmi2 python 1compute_spacetime_spectra.py $1 ${year} # ens # year
done
