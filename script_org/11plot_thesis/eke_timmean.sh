#!/bin/bash
#SBATCH --job-name=eke_mean
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=eke_mean.%j.out


module load cdo/2.5.0-gcc-11.2.0
module load parallel

eke_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/eke_daily/
tmp_dir=/scratch/m/m300883/eke_daily/
mkdir -p $tmp_dir

out_file=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_monthly_stat/eke_50000_monthly_05_09.nc

# find all files in eke_dir
eke_files=($(find $eke_dir -name "*.nc" -print))

cdo -r -P 8 -timmean -mergetime -apply,sellevel,50000 [ "${eke_files[@]}" ] $out_file