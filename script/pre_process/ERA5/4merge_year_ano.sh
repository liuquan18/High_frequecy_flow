#!/bin/bash
#SBATCH --job-name=merge
#SBATCH --time=01:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=5
#SBATCH --mem=200G
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=merge.%j.out

module load parallel

var=$1
dir=/scratch/m/m300883/${var}_tmp/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/${var}_daily_ano/
mkdir -p $to_dir

export dir to_dir var

merge_year(){
    year=$1
    echo "Merging year ${year}"
    files=$(find $dir -name "*${year}*.nc")
    cdo -r -O mergetime $files $to_dir/E5pl00_1D_daily_${year}-05-01_${year}-09-30.nc
}

export -f merge_year

parallel -j 5 merge_year ::: {1979..2024}