#!/bin/bash
#SBATCH --job-name=pre_process
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=25
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=pre_process.%j.out
module load cdo
module load parallel
var=$1
var_num=$2

daily_dir=/pool/data/ERA5/E5/pl/an/1D/${var_num}/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/${var}_daily/

export daily_dir to_dir var
mkdir -p $to_dir 

Mayfiles=($(find $daily_dir -name "*.grb" -print | grep "\-05_${var_num}\.grb$"))
Junfiles=($(find $daily_dir -name "*.grb" -print | grep "\-06_${var_num}\.grb$"))
Julfiles=($(find $daily_dir -name "*.grb" -print | grep "\-07_${var_num}\.grb$"))
Augfiles=($(find $daily_dir -name "*.grb" -print | grep "\-08_${var_num}\.grb$"))
Sepfiles=($(find $daily_dir -name "*.grb" -print | grep "\-09_${var_num}\.grb$"))

daily_files=(${Mayfiles[@]} ${Junfiles[@]} ${Julfiles[@]} ${Augfiles[@]} ${Sepfiles[@]})

pre_process(){
    infile=$1
    echo Processing $(basename $infile)
    outfile=${to_dir}$(basename $infile .grb).nc
    cdo -f nc -O -P 10 -setgridtype,regular -vertmean -sellevel,85000,87500,90000,92500,95000,97500,100000 $infile $outfile

}

export -f pre_process

parallel --jobs 25 pre_process ::: ${daily_files[@]}