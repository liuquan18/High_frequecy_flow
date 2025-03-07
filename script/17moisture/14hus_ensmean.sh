#!/bin/bash
#SBATCH --job-name=ensmean
#SBATCH --time=03:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=20
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=ensmean.%j.out

decade=$1

# base_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_daily_ano/
base_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/hus_daily_std/

to_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/0stat_results/

hus_files=$(ls ${base_dir}r*i1p1f1/*${decade}*.nc)

# ensemble mean

cdo -P 20 -ensmean [ ${hus_files} ] ${to_dir}hus_std_ensmean_${decade}.nc