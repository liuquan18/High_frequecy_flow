#!/bin/bash
#SBATCH --job-name=trend
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=trend.%j.out


zg_sesonal_dir=/work/mh0033/m300883/Tel_MMLE/data/ERA5/zg/
monthly_files=($(find $zg_sesonal_dir -name "*.grb" -print))
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_monthly_stat/

# # seasonal cycle
# cdo -f nc -P 10 -setgridtype,regular -divc,9.80665 -ymonmean -selmon,5/9 -mergetime -apply,sellevel,50000 [ ${monthly_files[@]} ] ${to_dir}zg_50000_seasonal_cyc_05_09.nc


# cdo -f nc -O -P 8 -divc,9.80665 -sellonlatbox,-90,40,20,80 -setgridtype,regular -selmon,5/9 -mergetime -apply,-sellevel,50000 [ ${monthly_files[@]} ] ${to_dir}zg_50000_monthly_05_09.nc

# export zg_sesonal_dir monthly_files to_dir


month_pre_data=${to_dir}zg_50000_monthly_05_09.nc

export month_pre_data

trend(){

    mon=$1
    echo "Processing month $mon"
    afile=${to_dir}zg_50000_trend_${mon}_a.nc
    bfile=${to_dir}zg_50000_trend_${mon}_b.nc

    # monthly data pre-process
    # trend
    cdo -P 8 -trend -selmon,$mon $month_pre_data $afile $bfile


}


export -f trend

parallel --jobs 5 trend ::: {5..9}