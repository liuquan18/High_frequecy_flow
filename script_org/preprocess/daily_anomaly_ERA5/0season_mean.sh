#!/bin/bash
#SBATCH --job-name=trend
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=10
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=trend.%j.out

# module load cdo/2.5.0-gcc-11.2.0
module load parallel

var=$1
var_num=$2

var_month_dir=/pool/data/ERA5/E5/pl/an/1M/${var_num}/

monthly_files=($(find $var_month_dir -name "*.grb" -print))
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/${var}_monthly_mean/

mkdir -p $to_dir

export var_month_dir monthly_files to_dir var

# monthly data pre-process
cdo -r -f nc -O -P 10 -setgridtype,regular -yearmonmean -selmon,5/9 -selyear,1979/2024 -mergetime [ ${monthly_files[@]} ] ${to_dir}${var}_monthly_05_09.nc


