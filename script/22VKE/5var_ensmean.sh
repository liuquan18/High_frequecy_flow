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

module load cdo/2.5.0-gcc-11.2.0

decade=$1
var=$2
echo ensemble mean for ${decade} ${var}

# base_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/upvp_daily_ano/
base_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily/

to_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_ensmean/

mkdir -p ${to_dir}

upvp_files=$(ls ${base_dir}r*i1p1f1/*${decade}*.nc)

# ensemble mean

cdo -O -P 20 -ensmean -apply,timmean [ ${upvp_files} ] ${to_dir}${var}_ensmean_${decade}.nc