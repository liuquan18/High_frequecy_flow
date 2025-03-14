#!/bin/bash
#SBATCH --job-name=pre_process
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=25
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=pre_process.%j.out
module load cdo
module load parallel
var=$1           # u       v   q (hus)  ta
var_num=$2       # 131   132    133     130

daily_dir=/pool/data/ERA5/E5/pl/an/1D/${var_num}/
tmp_dir=/scratch/m/m300883/ERA5_allplev/${var}_daily/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/${var}_daily/

export daily_dir tmp_dir to_dir var
mkdir -p $tmp_dir $to_dir

Mayfiles=($(find $daily_dir -name "*.grb" -print | grep "\-05_${var_num}\.grb$"))
Junfiles=($(find $daily_dir -name "*.grb" -print | grep "\-06_${var_num}\.grb$"))
Julfiles=($(find $daily_dir -name "*.grb" -print | grep "\-07_${var_num}\.grb$"))
Augfiles=($(find $daily_dir -name "*.grb" -print | grep "\-08_${var_num}\.grb$"))
Sepfiles=($(find $daily_dir -name "*.grb" -print | grep "\-09_${var_num}\.grb$"))

daily_files=(${Mayfiles[@]} ${Junfiles[@]} ${Julfiles[@]} ${Augfiles[@]} ${Sepfiles[@]})

pre_process(){
    infile=$1
    echo Processing $(basename $infile)
    tmpfile=${tmp_dir}$(basename $infile .grb).nc
    cdo -f nc -O -P 10 -setgridtype,regular -sellevel,20000,22500,25000,30000,35000,40000,45000,50000,55000,60000,65000,70000,75000,77500,80000,82500,85000,87500,90000,92500,95000,97500,100000 $infile $tmpfile

}

merge_year(){
    year=$1
    echo "Merging year ${year}"
    year_files=$(find ${tmp_dir} -name "*.nc" | grep ${year})
    cdo -O mergetime ${year_files} ${to_dir}E5pl00_1D_${var}_daily_${year}-05-01_${year}-09-31.nc
}

export -f pre_process 
export -f merge_year

parallel --jobs 25 pre_process ::: ${daily_files[@]}

parallel --jobs 10 merge_year ::: {1979..2024}
