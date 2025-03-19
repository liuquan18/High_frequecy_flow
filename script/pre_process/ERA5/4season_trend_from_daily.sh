#!/bin/bash
#SBATCH --job-name=trend
#SBATCH --time=01:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=10
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=trend.%j.out

# module load cdo 
module load parallel

var=$1

var_daily_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/${var}_daily/

daily_files=($(find $var_daily_dir -name "*.nc" -print))
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/${var}_monthly_stat/

mkdir -p $to_dir

export var_daily_dir daily_files to_dir var



trend(){

    mon=$1
    echo "month averaging $mon"
    cdo -r -f nc -O -P 10 -monmean -mergetime -apply,selmon,$mon [ ${daily_files[@]} ] ${to_dir}${var}_monthly_${mon}.nc

    month_pre_data=${to_dir}${var}_monthly_${mon}.nc
    echo "Processing month $mon"
    afile=${to_dir}${var}_trend_${mon}_a.nc
    bfile=${to_dir}${var}_trend_${mon}_b.nc

    # monthly data pre-process
    # trend
    cdo -P 10 -trend -selmon,$mon $month_pre_data $afile $bfile


}


export -f trend

parallel --jobs 5 trend ::: {05..09}