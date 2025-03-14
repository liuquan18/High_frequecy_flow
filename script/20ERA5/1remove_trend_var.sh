#!/bin/bash
#SBATCH --job-name=detrend
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=25
#SBATCH --cpus-per-task=10
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=detrend.%j.out

module load cdo
module load parallel

var=$1
var_num=$2

daily_dir=/pool/data/ERA5/E5/pl/an/1D/${var_num}/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/${var}_daily_rm_trend/
daily_pre_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/${var}_daily/

export daily_dir to_dir daily_pre_dir var
mkdir -p $to_dir $daily_pre_dir

Mayfiles=($(find $daily_dir -name "*.grb" -print | grep "\-05_${var_num}\.grb$"))
Junfiles=($(find $daily_dir -name "*.grb" -print | grep "\-06_${var_num}\.grb$"))
Julfiles=($(find $daily_dir -name "*.grb" -print | grep "\-07_${var_num}\.grb$"))
Augfiles=($(find $daily_dir -name "*.grb" -print | grep "\-08_${var_num}\.grb$"))
Sepfiles=($(find $daily_dir -name "*.grb" -print | grep "\-09_${var_num}\.grb$"))

daily_files=(${Mayfiles[@]} ${Junfiles[@]} ${Julfiles[@]} ${Augfiles[@]} ${Sepfiles[@]})

Remove_trend(){

    infile=$1
    echo Processing $(basename $infile)
    pre_file=${daily_pre_dir}$(basename $infile .grb).nc

    month=$(basename "$infile" | sed -E 's/.*_([0-9]{4})-([0-9]{2})_.*/\2/')
    afile=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/${var}_monthly_stat/${var}_1000_850hpa_trend_${month}_a.nc
    bfile=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/${var}_monthly_stat/${var}_1000_850hpa_trend_${month}_b.nc

    # daily data pre-process
    cdo -f nc -O -P 10 -setgridtype,regular -vertmean -sellevel,85000,87500,90000,92500,95000,97500,100000 $infile $pre_file

    # subtract trend from daily data
    cdo -O -P 10 -subtrend $pre_file $afile $bfile ${to_dir}$(basename $infile .grb)_rm_trend.nc

}

export -f Remove_trend

parallel --jobs 25 Remove_trend ::: ${daily_files[@]}