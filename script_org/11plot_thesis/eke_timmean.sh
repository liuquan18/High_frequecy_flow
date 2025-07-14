#!/bin/bash
#SBATCH --job-name=eke_mean
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=46
#SBATCH --ntasks=46
#SBATCH --cpus-per-task=8
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=eke_mean.%j.out


module load cdo/2.5.0-gcc-11.2.0
module load parallel

eke_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5_allplev/eke_daily/
tmp_dir=/scratch/m/m300883/eke_daily/
mkdir -p $tmp_dir

out_file=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_monthly_stat/eke_50000_monthly_05_09.nc

# find all files in eke_dir
eke_files=($(find $eke_dir -name "*.nc" -print))


year_mean_500(){
    infile=$1
    tmpfile=${tmp_dir}$(basename $infile .nc)_tmp.nc

    # select 50000 hPa level and apply grid type
    cdo -r -f nc -O -P 8 -timmean -sellevel,50000 -setgridtype,regular $infile $tmpfile
    echo $tmpfile
}

export tmp_dir
export out_file
export -f year_mean_500

for file in "${eke_files[@]}"; do
    echo "Processing $file"
    while [ "$(jobs -p | wc -l)" -ge "$SLURM_NTASKS" ]; do
        sleep 2
    done
    srun --ntasks=1 --nodes=1 --cpus-per-task=$SLURM_CPUS_PER_TASK bash -c "year_mean_500 '$file'" &
done
wait


# Merge all processed files
eke_files=($(find $tmp_dir -name "*_tmp.nc" -print))
echo "Merging files: ${eke_files[@]}"
# Use cdo to merge and calculate the time mean
if [ -f "$out_file" ]; then
    rm -f "$out_file"
fi
echo "Output file: $out_file"


# Merge and calculate the time mean
cdo -r -O -P 8 -mergetime ${eke_files[@]} $out_file
# delete the tmp files
rm -f ${tmp_dir}*_tmp.nc
# cdo -r -O -P 8 -timmean -mergetime ${eke_files[@]} $out_file