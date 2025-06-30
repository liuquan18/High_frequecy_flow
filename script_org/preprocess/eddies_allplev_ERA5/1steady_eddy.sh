#!/bin/bash
#SBATCH --job-name=steady
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=46
#SBATCH --ntasks=46
#SBATCH --cpus-per-task=8
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=steady.%j.out

module load cdo/2.5.0-gcc-11.2.0
module load parallel

var=$1
model=${2:-ERA5_allplev}

echo "Processing variable: ${var} for model: ${model}"


T_path=/work/mh0033/m300883/High_frequecy_flow/data/${model}/${var}_hat_daily/
T_mmean_path=/work/mh0033/m300883/High_frequecy_flow/data/${model}/${var}_monthly_mean/


Ts_path=/work/mh0033/m300883/High_frequecy_flow/data/${model}/${var}_steady_daily/


tmp_dir=/scratch/m/m300883/ERA5/${var}_steady/

if [ -d "${tmp_dir}" ]; then
    rm -rf "${tmp_dir}"
fi
mkdir -p "${Ts_path}" "${tmp_dir}"


export T_path Ts_path member tmp_dir var


# function to band filter
sub_zonmean(){
    infile=$1
    mmean_file=$2
    outfile=$3


    # zonal anomaly
    cdo -P 8 -O ymonsub ${infile} -enlarge,${mmean_file} -zonmean ${mmean_file} ${outfile}
}


export -f sub_zonmean


daily_files=$(find ${T_path} -name "*.nc" -print | tr '\n' ' ')
mean_file=$(find ${T_mmean_path} -name "*.nc" -print | head -n 1)



for file in ${daily_files[@]}; do
    echo "subtracting: $file"
    while [ "$(jobs -p | wc -l)" -ge "$SLURM_NTASKS" ]; do
        sleep 2
    done
    srun --ntasks=1 --nodes=1 --cpus-per-task=$SLURM_CPUS_PER_TASK bash -c "sub_zonmean '$file' '$mean_file'" &
done

wait  # Wait for all background pre_process jobs to finish


# remove the temporary files
rm -rf ${tmp_dir}