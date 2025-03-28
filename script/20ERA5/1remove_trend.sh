#!/bin/bash
#SBATCH --job-name=detrend
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=25
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=detrend.%j.out

module load cdo
module load parallel

daily_dir=/pool/data/ERA5/E5/pl/an/1D/129/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_daily_rm_trend/
daily_tmp_dir=/scratch/m/m300883/ERA5/zg_daily_pre/

export daily_dir to_dir daily_tmp_dir
mkdir -p $to_dir $daily_tmp_dir

Mayfiles=($(find $daily_dir -name "*.grb" -print | grep '\-05_129\.grb$'))
Junfiles=($(find $daily_dir -name "*.grb" -print | grep '\-06_129\.grb$'))
Julfiles=($(find $daily_dir -name "*.grb" -print | grep '\-07_129\.grb$'))
Augfiles=($(find $daily_dir -name "*.grb" -print | grep '\-08_129\.grb$'))
Sepfiles=($(find $daily_dir -name "*.grb" -print | grep '\-09_129\.grb$'))

daily_files=(${Mayfiles[@]} ${Junfiles[@]} ${Julfiles[@]} ${Augfiles[@]} ${Sepfiles[@]})

Remove_trend(){

    infile=$1
    tmpfile=${daily_tmp_dir}$(basename $infile .grb).nc

    month=$(basename "$infile" | sed -E 's/.*_([0-9]{4})-([0-9]{2})_.*/\2/')
    afile=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_monthly_stat/zg_50000_trend_${month}_a.nc
    bfile=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_monthly_stat/zg_50000_trend_${month}_b.nc

    # daily data pre-process
    cdo -f nc -O -P 8 -divc,9.80665 -sellevel,50000 -sellonlatbox,-90,40,20,80 -setgridtype,regular $infile $tmpfile

    # subtract trend from daily data
    cdo -O -P 8 -subtrend $tmpfile $afile $bfile ${to_dir}$(basename $infile .grb)_rm_trend.nc

}

export -f Remove_trend

parallel --jobs 25 Remove_trend ::: ${daily_files[@]}