#!/bin/bash
#SBATCH --job-name=vertmean
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=25
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=vertmean.%j.out

module load cdo
module load parallel

# get the ensemble member from the command line
var=$1
echo "Ensemble member ${member} for variable ${var}"


# vt daily
vt_daily_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_ano/r*i1p1f1/
vt_daily_file=${var}_day_MPI-ESM1-2-LR_r*i1p1f1_gn_*.nc
daily_files=($(find $vt_daily_path -name $vt_daily_file -print))

for member in {1..50}; do
    save_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/${var}_daily_ano_lowlevel/r${member}i1p1f1/
    mkdir -p $save_dir
done




parallel --dryrun -j 25 cdo -P 8 -vertmean -sellevel,100000,85000 {} $save_dir{/.}_1000_850hpa.nc ::: ${daily_files[@]}

