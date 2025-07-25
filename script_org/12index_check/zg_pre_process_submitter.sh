#!/bin/bash
#SBATCH --job-name=selNA
#SBATCH --time=00:30:00
#SBATCH --partition=compute
#SBATCH --nodes=5
#SBATCH --ntasks=1250
#SBATCH --mem=0
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=selNA.%j.out

module load cdo
module load parallel

var=zg

base_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/zg_daily/
to_dir=/work/mh0033/m300883/High_frequecy_flow/data/MPI_GE_CMIP6_allplev/zg_NA_daily_ano/

# mkdir for all ensemble r${member}i1p1f1 under to_dir
for member in {1..50}; do
    mkdir -p ${to_dir}r${member}i1p1f1/
done



find ${base_dir} -name "${var}_day_MPI-ESM1-2-LR_r*i1p1f1_gn_*.nc" | parallel -j $SLURM_NTASKS srun --nodes=1 --ntasks=1 --cpus-per-task=10 zg_pre_process.sh