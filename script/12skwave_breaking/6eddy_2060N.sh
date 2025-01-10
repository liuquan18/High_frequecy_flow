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
echo "Ensemble member ${member}"

eke_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/eke_daily_ano/r${member}i1p1f1/
eke_2060_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/eke_daily_ano_2060N/r${member}i1p1f1/

mkdir -p ${eke_2060_path}

find ${eke_path} -name "eke*_r${member}i1p1f1_gn_*.nc" | parallel --jobs 25 cdo -mermean -sellonlatbox,0,360,20,60 -sellevel,25000 {} ${eke_2060_path}{/}