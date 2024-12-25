#!/bin/bash
#SBATCH --job-name=ano
#SBATCH --time=00:10:00
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=7
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=ano.%j.out

# subtract the ensemble mean of the monthly data from the daily data using cdo monsub
# by doing which a long-term trend and seasonal cycle are removed
module load cdo
module load parallel

# get the ensemble member from the command line
member=$1
echo "Ensemble member ${member}"

from_path=/scratch/m/m300883/zg_day_ano/r${member}i1p1f1
to_path=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6/daily/zg_MJJAS_ano_decade/r${member}i1p1f1/
tmp_path=/scratch/m/m300883/zg_day_ano_year/r${member}i1p1f1/

mkdir -p $to_path $tmp_path

export to_path tmp_path

# define function split
split() {
    infile=$1
    # Get the filename
    filename=$(basename $infile)
    echo "Processing $filename"

    name_prefix=${filename:0:-24}

    cdo -splityear $infile $tmp_path$name_prefix

}

export -f split

find $from_path -name "*.nc" | parallel --jobs 14 split

# define function merge, merge each decade from 1850 to 2100
merge() {
    start_year=$1
    end_year=$((start_year+9))

    echo "merging files from ${start_year} to ${end_year}"

    # Construct a regex pattern to match all years from start_year to end_year
    regex=""
    for year in $(seq $start_year $end_year); do
        if [ -z "$regex" ]; then
            regex="_${year}"
        else
            regex="${regex}|_${year}"
        fi
    done
    regex="${regex}\.nc"

    # Find files with name ending within start_year and end_year
    files=$(find $tmp_path -type f -name "*_r${member}i1p1f1_gn_*.nc" | grep -E "$regex")

    if [ -n "$files" ]; then
        outfile="${to_path}zg_day_MPI-ESM1-2-LR_r${member}i1p1f1_gn_${start_year}0501-${end_year}0930_ano.nc"
        cdo mergetime $files $outfile
        echo "Created $outfile"
    else
        echo "No files found for the decade ${start_year}-${end_year}"
    fi
}

export -f merge

# Loop through decades from 1850 to 2100
for year in $(seq 1850 10 2090); do
    merge $year
done
