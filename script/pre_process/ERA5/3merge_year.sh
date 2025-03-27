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

dir=$1
to_dir=$(echo "$dir" | sed 's/_rm_trend//')

mkdir -p $to_dir

export dir to_dir

merge_year(){
    year=$1
    echo "Merging year ${year}"
    files=$(find $dir -name "*${year}*.nc")
    cdo -r -O mergetime $files $to_dir/E5pl00_1D_daily_${year}-05-01_${year}-09-30.nc
}

export -f merge_year

parallel -j 5 merge_year ::: {1979..2024}