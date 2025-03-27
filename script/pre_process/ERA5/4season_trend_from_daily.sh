#!/bin/bash
#SBATCH --job-name=trend_day
#SBATCH --time=03:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --cpus-per-task=5
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=trend_day.%j.out

module unload cdo

module load cdo/2.5.0-gcc-11.2.0
module load parallel

var=$1

to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/${var}_monthly_stat/

mkdir -p $to_dir

export var_daily_dir daily_files to_dir var

trend(){
    local mon=$1
    shift

    local var_daily_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/${var}_daily/

    local daily_files=($(find $var_daily_dir -name "*.nc" -print))

    echo "month averaging $mon"
    cdo -r -f nc -O -P 10 -monmean -mergetime -apply,selmon,$mon [ ${daily_files[@]} ] ${to_dir}${var}_monthly_${mon}.nc

    month_pre_data=${to_dir}${var}_monthly_${mon}.nc
    echo "Processing month $mon"
    afile=${to_dir}${var}_trend_${mon}_a.nc
    bfile=${to_dir}${var}_trend_${mon}_b.nc

    # monthly data pre-process
    # trend
    cdo -P 2 -trend $month_pre_data $afile $bfile
}


export -f trend

parallel --jobs 5 trend ::: {5..9}