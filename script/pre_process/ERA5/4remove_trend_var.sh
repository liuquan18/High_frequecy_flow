#!/bin/bash
#SBATCH --job-name=detrend
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=10
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=detrend.%j.out

module load cdo/2.5.0-gcc-11.2.0
module load parallel
var=$1

var_daily_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/${var}_daily/

daily_files=($(find $var_daily_dir -name "*.nc" -print))

to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/${var}_monthly_stat/

tmp_dir=/scratch/m/m300883/${var}_tmp/

mkdir -p $to_dir $tmp_dir

export var_daily_dir daily_files to_dir var tmp_dir



Remove_trend(){

    local infile=$1
    local month=$2
    echo Processing $(basename $infile) in month $month

    afile=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/${var}_monthly_stat/${var}_trend_${month}_a.nc
    bfile=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/${var}_monthly_stat/${var}_trend_${month}_b.nc


    # subtract trend from daily data
    cdo -O -P 10 -subtrend -selmon,$month $infile $afile $bfile ${tmp_dir}$(basename $infile .nc)_${month}_rm_trend.nc

}

export -f Remove_trend

parallel --jobs 10 Remove_trend ::: ${daily_files[@]} ::: {5..9}