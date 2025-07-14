#!/bin/bash
#SBATCH --job-name=zg_hat
#SBATCH --time=01:00:00
#SBATCH --partition=compute
#SBATCH --nodes=46
#SBATCH --ntasks=46
#SBATCH --cpus-per-task=8
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=zg_hat.%j.out


module load cdo/2.5.0-gcc-11.2.0
module load parallel

from_dir=/pool/data/ERA5/E5/pl/an/1M/129/
tmp_dir=/scratch/m/m300883/ERA5/zg_hat/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/ERA5/zg_monthly_state/

mkdir -p ${tmp_dir} ${to_dir}

export from_dir tmp_dir to_dir

steady_eddy(){
    dec=$1
    Tfile=$(find ${from_dir} -name "*${dec}*.grb")

    cdo -P 8 -O -timmean -selmon-selmonth,5,6,7,8,9 -sub ${Tfile} -enlarge,${Tfile} -zonmean ${Tfile} ${tmp_dir}/zg_hat_${dec}.nc

}

export -f steady_eddy

for dec in {1979..2024}; do
    echo "Processing $file"
    while [ "$(jobs -p | wc -l)" -ge "$SLURM_NTASKS" ]; do
        sleep 2
    done
    srun --ntasks=1 --nodes=1 --cpus-per-task=$SLURM_CPUS_PER_TASK bash -c "steady_eddy ${dec}"

done

wait

# Merge all processed files
zg_files=($(find ${tmp_dir} -name "zg_hat_*.nc" -print))
echo "Merging files: ${zg_files[@]}"
# Use cdo to merge and calculate the time mean
cdo -r -O -P 8 -timmean -mergetime ${zg_files[@]} ${to_dir}/zg_hat_monthly_mean.nc