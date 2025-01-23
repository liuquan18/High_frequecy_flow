#!/bin/bash
#SBATCH --job-name=merge_year
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=8
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=merge_year.%j.out
module load cdo
module load parallel
var=$1


daily_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/${var}/
tmp_dir=/scratch/m/m300883/ERA5/${var}/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/${var}_mergeyear/

export daily_dir tmp_dir to_dir var
mkdir -p $tmp_dir $to_dir

merge_year(){
    year=$1
    echo "Merging year ${year}"
    year_files=$(find ${daily_dir} -name "*.nc" | grep ${year})
    cdo -r -O -P 8 mergetime ${year_files} ${to_dir}E5pl00_1D_${var}_250hPa_daily_${year}-05-01_${year}-09-31.nc

    # rm tmp files
    rm ${year_files}
}

export -f merge_year


parallel --jobs 10 merge_year ::: {1979..2024}
