#!/bin/bash
#SBATCH --job-name=eddy_sel
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=25
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=eddy_sel.%j.out

module load cdo
module load parallel

node=$1
member=$node
var=$2 # eke, eke_high
lat_min=${3:-20}  # Default to 20 if $3 is not provided
lat_max=${4:-60}  # Default to 60 if $4 is not provided
echo "Ensemble member ${member} lat range ${lat_min}N to ${lat_max}N"

eke_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_ano/r${member}i1p1f1/
eke_mermean_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_ano_${lat_min}${lat_max}N/r${member}i1p1f1/

mkdir -p ${eke_mermean_path}

# find ${eke_path} -name "eke*_r${member}i1p1f1_gn_*.nc" | parallel --jobs 25 cdo -mermean -sellonlatbox,0,360,${lat_min},${lat_max} -sellevel,25000 {} ${eke_mermean_path}{/}
find ${eke_path} -name "eke*_r${member}i1p1f1_gn_*.nc" | parallel --jobs 25 cdo -mermean -sellonlatbox,0,360,${lat_min},${lat_max} -vertmean -sellevel,100000,85000 {} ${eke_mermean_path}{/}